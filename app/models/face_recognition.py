import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
import cv2
import numpy as np
from PIL import Image
from typing import List, Tuple, Optional

class FaceRecognitionSystem:
    """
    Face recognition system using MTCNN for face detection and FaceNet for face recognition.
    
    This class handles:
    - Face detection in images
    - Face embedding generation
    - Face comparison and matching
    
    Attributes:
        device (str): Device to run models on ('cuda' or 'cpu')
        mtcnn (MTCNN): Face detection model
        facenet (InceptionResnetV1): Face recognition model
    """
    def __init__(self, device='cuda' if torch.cuda.is_available() else 'cpu'):
        """
        Initialize the face recognition system
        
        Args:
            device (str): Device to run models on ('cuda' or 'cpu')
        """
        self.device = device
        
        # Initialize the MTCNN for face detection
        self.mtcnn = MTCNN(
            keep_all=True,
            device=device,
            selection_method='probability',
            image_size=160
        )
        
        # Initialize the FaceNet model for face recognition
        self.facenet = InceptionResnetV1(
            pretrained='vggface2',
            device=device
        ).eval()
    
    def detect_faces(self, image: np.ndarray) -> Tuple[List[np.ndarray], List[List[int]]]:
        """
        Detect faces in an image and return their bounding boxes
        
        Args:
            image (numpy.ndarray): Input image in BGR format with shape (H, W, C)
        
        Returns:
            Tuple containing:
            - List of face images (numpy.ndarray)
            - List of bounding boxes [x1, y1, x2, y2]
        """
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(image_rgb)
        
        # Detect faces
        boxes, probs = self.mtcnn.detect(pil_image)
        
        if boxes is None:
            return [], []
        
        faces = []
        valid_boxes = []
        
        for box in boxes:
            x1, y1, x2, y2 = [int(b) for b in box]
            face = image[y1:y2, x1:x2]
            if face.size > 0:  # Check if face crop is valid
                faces.append(face)
                valid_boxes.append([x1, y1, x2, y2])
        
        return faces, valid_boxes
    
    def get_face_embedding(self, face_image: np.ndarray) -> Optional[np.ndarray]:
        """
        Generate embedding for a face image using FaceNet
        
        Args:
            face_image (numpy.ndarray): Face image in BGR format
        
        Returns:
            Optional[numpy.ndarray]: Face embedding vector of shape (512,) or None if error
        """
        try:
            # Convert BGR to RGB
            face_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image and resize
            face_pil = Image.fromarray(face_rgb).resize((160, 160))
            
            # Convert to tensor
            face_tensor = torch.from_numpy(np.array(face_pil)).float()
            # Change from (H, W, C) to (C, H, W)
            face_tensor = face_tensor.permute(2, 0, 1)
            # Add batch dimension
            face_tensor = face_tensor.unsqueeze(0)
            # Normalize
            face_tensor = face_tensor / 255.0
            
            # Move to device
            face_tensor = face_tensor.to(self.device)
            
            # Get embedding
            with torch.no_grad():
                embedding = self.facenet(face_tensor).squeeze().cpu().numpy()
            
            return embedding
        except Exception as e:
            print(f"Error generating face embedding: {e}")
            return None
    
    def compare_faces(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compare two face embeddings and return similarity score using cosine similarity
        
        Args:
            embedding1 (numpy.ndarray): First face embedding vector
            embedding2 (numpy.ndarray): Second face embedding vector
        
        Returns:
            float: Similarity score between 0 and 1 (1 means identical faces)
        """
        # Normalize embeddings
        embedding1 = embedding1 / np.linalg.norm(embedding1)
        embedding2 = embedding2 / np.linalg.norm(embedding2)
        
        # Calculate cosine similarity
        similarity = np.dot(embedding1, embedding2)
        
        return similarity 