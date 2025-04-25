import cv2
import numpy as np
from fer import FER
from typing import Optional, Dict

class EmotionDetector:
    """
    Emotion detection system using FER (Facial Emotion Recognition).
    
    This class handles:
    - Face emotion detection in images
    - Emotion probability calculation
    - Dominant emotion determination
    
    Attributes:
        detector (FER): FER emotion detection model
    """
    def __init__(self):
        """Initialize the emotion detection system"""
        self.detector = FER()
    
    def detect_emotion(self, face_image: np.ndarray) -> Optional[Dict[str, float]]:
        """
        Detect emotions in a face image
        
        Args:
            face_image (numpy.ndarray): Face image in BGR format
        
        Returns:
            Optional[Dict[str, float]]: Dictionary of emotions and their probabilities,
                                      or None if detection failed
        """
        try:
            # Convert BGR to RGB
            face_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            
            # Detect emotions
            emotions = self.detector.detect_emotions(face_rgb)
            
            if not emotions:
                return None
            
            # Return the first face's emotions
            return emotions[0]['emotions']
        
        except Exception as e:
            print(f"Error in emotion detection: {e}")
            return None
    
    def get_dominant_emotion(self, emotions: Dict[str, float]) -> str:
        """
        Get the dominant emotion from emotion probabilities
        
        Args:
            emotions (Dict[str, float]): Dictionary of emotions and their probabilities
        
        Returns:
            str: Name of the dominant emotion
        """
        return max(emotions.items(), key=lambda x: x[1])[0] 