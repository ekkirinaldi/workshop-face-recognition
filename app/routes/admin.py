from flask import Blueprint, render_template, request, jsonify
import cv2
import numpy as np
from .. import face_recognition_system
from ..models.database import db, User, FaceEncoding

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def index():
    """
    Render the admin interface for managing users and face encodings
    
    Returns:
        HTML template: Rendered admin/index.html template with list of users
    """
    users = User.query.all()
    return render_template('admin/index.html', users=users)

@admin_bp.route('/users', methods=['GET'])
def list_users():
    """
    Get list of all users with their face encoding counts
    
    Returns:
        JSON response with list of users containing:
        - id: User ID
        - name: User's name
        - face_count: Number of face encodings for the user
    """
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'name': user.name,
        'face_count': len(user.face_encodings)
    } for user in users])

@admin_bp.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user with optional face encoding
    
    This endpoint:
    1. Creates a new user with provided name
    2. Optionally processes face image if provided
    3. Generates and stores face encoding
    
    Request:
        Form data with:
        - name: User's name
        - face_image: Optional face image file
    
    Returns:
        JSON response with created user details or error message
    """
    try:
        name = request.form.get('name')
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        
        # Create new user
        user = User(name=name)
        db.session.add(user)
        
        # Process face image if provided
        if 'face_image' in request.files:
            image_file = request.files['face_image']
            # Read image file
            image_bytes = image_file.read()
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Detect face
            faces, _ = face_recognition_system.detect_faces(image)
            if not faces:
                return jsonify({'error': 'No face detected in image'}), 400
            
            # Get face embedding
            embedding = face_recognition_system.get_face_embedding(faces[0])
            if embedding is None:
                return jsonify({'error': 'Failed to generate face embedding'}), 400
            
            # Create face encoding
            face_encoding = FaceEncoding()
            face_encoding.set_encoding(embedding)
            user.face_encodings.append(face_encoding)
        
        db.session.commit()
        return jsonify({
            'id': user.id,
            'name': user.name,
            'face_count': len(user.face_encodings)
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>/faces', methods=['POST'])
def add_face(user_id):
    """
    Add a new face encoding to an existing user
    
    This endpoint:
    1. Finds the user by ID
    2. Processes the provided face image
    3. Generates and stores new face encoding
    
    Args:
        user_id (int): ID of the user to add face encoding to
    
    Request:
        Form data with face_image file
    
    Returns:
        JSON response with updated user details or error message
    """
    try:
        user = User.query.get_or_404(user_id)
        
        if 'face_image' not in request.files:
            return jsonify({'error': 'No face image provided'}), 400
        
        image_file = request.files['face_image']
        image_bytes = image_file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Detect face
        faces, _ = face_recognition_system.detect_faces(image)
        if not faces:
            return jsonify({'error': 'No face detected in image'}), 400
        
        # Get face embedding
        embedding = face_recognition_system.get_face_embedding(faces[0])
        if embedding is None:
            return jsonify({'error': 'Failed to generate face embedding'}), 400
        
        # Create face encoding
        face_encoding = FaceEncoding()
        face_encoding.set_encoding(embedding)
        user.face_encodings.append(face_encoding)
        
        db.session.commit()
        return jsonify({
            'id': user.id,
            'name': user.name,
            'face_count': len(user.face_encodings)
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user and all their associated face encodings
    
    Args:
        user_id (int): ID of the user to delete
    
    Returns:
        Empty response with 204 status code on success
        JSON error message on failure
    """
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 