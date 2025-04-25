import os
import json
import cv2
import numpy as np
from datetime import datetime
from typing import List, Tuple, Optional
from .face_recognition import FaceRecognitionSystem
from .emotion_detection import EmotionDetector
from .database import db, User, FaceDump

class FaceDumper:
    """
    Face dumping system that captures and stores face data at regular intervals.
    
    This class handles:
    - Regular face capture
    - Emotion detection
    - Data storage
    - Face matching
    
    Attributes:
        face_recognition (FaceRecognitionSystem): Face recognition system
        emotion_detector (EmotionDetector): Emotion detection system
        dump_interval (int): Interval between dumps in seconds
        last_dump_time (float): Timestamp of last dump
        dump_dir (str): Directory to store face images
    """
    def __init__(self, dump_interval: int = 5, dump_dir: str = 'uploads/dumps'):
        """
        Initialize the face dumper
        
        Args:
            dump_interval (int): Interval between dumps in seconds
            dump_dir (str): Directory to store face images
        """
        self.face_recognition = FaceRecognitionSystem()
        self.emotion_detector = EmotionDetector()
        self.dump_interval = dump_interval
        self.last_dump_time = 0
        self.dump_dir = dump_dir
        
        # Create dump directory if it doesn't exist
        os.makedirs(dump_dir, exist_ok=True)
    
    def should_dump(self) -> bool:
        """
        Check if it's time to dump face data
        
        Returns:
            bool: True if it's time to dump, False otherwise
        """
        current_time = datetime.now().timestamp()
        return current_time - self.last_dump_time >= self.dump_interval
    
    def process_frame(self, frame: np.ndarray) -> List[dict]:
        """
        Process a video frame and dump face data if needed
        
        Args:
            frame (numpy.ndarray): Video frame in BGR format
        
        Returns:
            List[dict]: List of processed face data
        """
        if not self.should_dump():
            return []
        
        # Detect faces
        faces, boxes = self.face_recognition.detect_faces(frame)
        if not faces:
            return []
        
        results = []
        for face, box in zip(faces, boxes):
            # Get face embedding
            embedding = self.face_recognition.get_face_embedding(face)
            if embedding is None:
                continue
            
            # Find matching user
            user, similarity = self._find_matching_user(embedding)
            if user is None:
                continue
            
            # Detect emotion
            emotions = self.emotion_detector.detect_emotion(face)
            if emotions is None:
                continue
            
            # Get dominant emotion
            dominant_emotion = self.emotion_detector.get_dominant_emotion(emotions)
            
            # Convert box coordinates to Python integers
            box = [int(x) for x in box]
            
            # Convert similarity score to Python float
            similarity = float(similarity)
            
            # Save face image
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = f"{user.id}_{timestamp}.jpg"
            filepath = os.path.join(self.dump_dir, filename)
            cv2.imwrite(filepath, face)
            
            # Create face dump
            face_dump = FaceDump(
                user_id=user.id,
                face_image_path=filepath,
                bounding_box=json.dumps(box),
                emotion=dominant_emotion,
                similarity_score=similarity
            )
            
            db.session.add(face_dump)
            db.session.commit()
            
            results.append({
                'user_id': user.id,
                'name': user.name,
                'box': box,
                'emotion': dominant_emotion,
                'similarity': similarity,
                'image_path': filepath
            })
        
        self.last_dump_time = datetime.now().timestamp()
        return results
    
    def _find_matching_user(self, embedding: np.ndarray) -> Tuple[Optional[User], float]:
        """
        Find the user that matches the face embedding
        
        Args:
            embedding (numpy.ndarray): Face embedding vector
        
        Returns:
            Tuple[Optional[User], float]: Matching user and similarity score
        """
        best_match = None
        best_score = 0.0
        
        for user in User.query.all():
            for stored_encoding in user.face_encodings:
                stored_embedding = stored_encoding.get_encoding()
                score = float(self.face_recognition.compare_faces(embedding, stored_embedding))  # Convert to Python float
                
                if score > best_score:
                    best_score = score
                    best_match = user
        
        return best_match, best_score 