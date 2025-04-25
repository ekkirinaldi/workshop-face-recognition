from flask import Blueprint, render_template, jsonify, request, send_from_directory
import cv2
import numpy as np
import base64
import os
from .. import face_recognition_system
from ..models.database import db, User, FaceEncoding, FaceDump
from ..models.face_dumper import FaceDumper

main_bp = Blueprint('main', __name__)
face_dumper = FaceDumper()

@main_bp.route('/')
def index():
    """
    Render the main page with video stream for face recognition
    
    Returns:
        HTML template: Rendered index.html template
    """
    return render_template('index.html')

@main_bp.route('/uploads/<path:filename>')
def serve_upload(filename):
    """
    Serve uploaded files from the uploads directory
    
    Args:
        filename (str): Path to the file within uploads directory
    
    Returns:
        File response
    """
    # Check if the file is in the dumps directory
    if filename.startswith('dumps/'):
        uploads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads')
        return send_from_directory(uploads_dir, filename)
    else:
        uploads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads')
        return send_from_directory(uploads_dir, filename)

@main_bp.route('/api/recognize', methods=['POST'])
def recognize_face():
    """
    Recognize faces in the uploaded image and match them against stored faces
    
    This endpoint:
    1. Receives a base64 encoded image
    2. Detects faces in the image
    3. Generates embeddings for each face
    4. Compares against stored face encodings
    5. Returns recognition results
    
    Request:
        JSON with 'image' field containing base64 encoded image
    
    Returns:
        JSON response with:
        - faces: List of detected faces with recognition results
        - error: Error message if something went wrong
    """
    try:
        # Get image data from request
        image_data = request.json.get('image')
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Convert base64 to numpy array
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Process frame with face dumper
        dump_results = face_dumper.process_frame(image)
        
        # Get recognition results
        faces, boxes = face_recognition_system.detect_faces(image)
        
        if not faces:
            return jsonify({'faces': []})
        
        results = []
        # Get all users and their face encodings
        users = User.query.all()
        
        for face, box in zip(faces, boxes):
            # Get embedding for detected face
            embedding = face_recognition_system.get_face_embedding(face)
            if embedding is None:
                continue
            
            # Compare with stored faces
            best_match = None
            best_score = 0.0  # Convert to Python float
            
            for user in users:
                for stored_encoding in user.face_encodings:
                    stored_embedding = stored_encoding.get_encoding()
                    score = float(face_recognition_system.compare_faces(embedding, stored_embedding))  # Convert to Python float
                    
                    if score > best_score:
                        best_score = score
                        best_match = user
            
            # Convert numpy int values to Python int
            box = [int(x) for x in box]
            
            # Find matching dump result if any
            dump_result = next((r for r in dump_results if r['box'] == box), None)
            
            # Add result
            result = {
                'box': box,
                'recognized': bool(best_score > 0.6),  # Convert to Python bool
                'name': best_match.name if best_match and best_score > 0.6 else 'Unknown',
                'confidence': best_score,
                'emotion': dump_result['emotion'] if dump_result else None,
                'similarity': dump_result['similarity'] if dump_result else None
            }
            results.append(result)
        
        return jsonify({'faces': results})
    
    except Exception as e:
        print(f"Error in recognize_face: {str(e)}")
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/face-dumps', methods=['GET'])
def get_face_dumps():
    """
    Get the latest face dumps from the database
    
    Returns:
        JSON response with:
        - dumps: List of face dumps with user info
    """
    try:
        # Get the latest face dumps (last 10)
        face_dumps = FaceDump.query.order_by(FaceDump.created_at.desc()).limit(10).all()
        
        results = []
        for dump in face_dumps:
            user = User.query.get(dump.user_id)
            if user:
                results.append({
                    'user_id': user.id,
                    'name': user.name,
                    'emotion': dump.emotion,
                    'similarity': dump.similarity_score,
                    'timestamp': dump.created_at.strftime('%Y%m%d_%H%M%S_%f'),
                    'image_path': dump.face_image_path
                })
        
        return jsonify({'dumps': results})
    
    except Exception as e:
        print(f"Error getting face dumps: {str(e)}")
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/face-dumps', methods=['DELETE'])
def delete_all_face_dumps():
    """
    Delete all face dumps from the database and filesystem
    
    Returns:
        JSON response with success message or error
    """
    try:
        # Get all face dumps
        face_dumps = FaceDump.query.all()
        
        # Delete files from filesystem
        for dump in face_dumps:
            if os.path.exists(dump.face_image_path):
                os.remove(dump.face_image_path)
        
        # Delete from database
        FaceDump.query.delete()
        db.session.commit()
        
        return jsonify({'message': 'All face dumps deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting face dumps: {str(e)}")
        return jsonify({'error': str(e)}), 500 