from datetime import datetime
import numpy as np
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    User model representing a person in the face recognition system.
    
    Attributes:
        id (int): Primary key
        name (str): User's name
        created_at (datetime): Timestamp when user was created
        updated_at (datetime): Timestamp when user was last updated
        face_encodings (relationship): One-to-many relationship with FaceEncoding
        face_dumps (relationship): One-to-many relationship with FaceDump
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    face_encodings = db.relationship('FaceEncoding', backref='user', lazy=True)
    face_dumps = db.relationship('FaceDump', backref='user', lazy=True)

    def __repr__(self):
        """String representation of the User object"""
        return f'<User {self.name}>'

class FaceEncoding(db.Model):
    """
    FaceEncoding model storing face embeddings for users.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to User
        encoding_vector (bytes): Binary storage of face embedding
        created_at (datetime): Timestamp when encoding was created
    """
    __tablename__ = 'face_encodings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    encoding_vector = db.Column(db.LargeBinary, nullable=False)  # Store face encoding as binary
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_encoding(self, encoding):
        """
        Convert numpy array face encoding to binary for database storage
        
        Args:
            encoding (numpy.ndarray): Face embedding vector
        """
        self.encoding_vector = encoding.tobytes()
    
    def get_encoding(self):
        """
        Convert binary face encoding back to numpy array
        
        Returns:
            numpy.ndarray: Face embedding vector
        """
        return np.frombuffer(self.encoding_vector, dtype=np.float32)

    def __repr__(self):
        """String representation of the FaceEncoding object"""
        return f'<FaceEncoding user_id={self.user_id}>'

class FaceDump(db.Model):
    """
    FaceDump model storing captured face data with emotion detection.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to User
        face_image_path (str): Path to stored face image
        bounding_box (str): JSON string of bounding box coordinates [x1, y1, x2, y2]
        emotion (str): Detected emotion
        similarity_score (float): Similarity score with original face
        created_at (datetime): Timestamp when dump was created
    """
    __tablename__ = 'face_dumps'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    face_image_path = db.Column(db.String(255), nullable=False)
    bounding_box = db.Column(db.String(100), nullable=False)  # JSON string of [x1, y1, x2, y2]
    emotion = db.Column(db.String(50), nullable=False)
    similarity_score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        """String representation of the FaceDump object"""
        return f'<FaceDump user_id={self.user_id} emotion={self.emotion}>' 