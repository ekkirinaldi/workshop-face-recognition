# Face Recognition Workshop

A comprehensive face recognition system built with Python, Flask, and modern computer vision libraries. This project demonstrates how to implement a production-ready face detection and recognition system with a web interface, database integration, and scalable architecture.

## Features

### Core Functionality
- Real-time face detection using multiple methods (Haar Cascades, DNN)
- Face recognition using state-of-the-art algorithms
- Feature extraction and face encoding
- Face matching with configurable thresholds
- Confidence scoring for matches

### Web Interface
- User-friendly web interface for face recognition
- Real-time video streaming support
- Image upload and processing
- Results visualization
- User management system

### Database Integration
- PostgreSQL database for storing face encodings
- Efficient face encoding storage and retrieval
- User management and authentication
- Activity logging and monitoring

### Security Features
- Secure file handling and storage
- Data encryption for sensitive information
- Role-based access control
- Input validation and sanitization
- Secure API endpoints

### Performance Optimization
- Caching mechanisms for face encodings
- Batch processing capabilities
- Resource management and monitoring
- Horizontal scaling support
- Load balancing

## Tech Stack

### Backend
- Python 3.11
- Flask web framework
- OpenCV for image processing
- face_recognition library
- SQLAlchemy ORM

### Frontend
- HTML5/CSS3
- JavaScript
- Bootstrap for UI
- WebRTC for video streaming

### Database
- PostgreSQL

### Deployment
- Docker containerization
- Docker Compose for orchestration
- Nginx for reverse proxy
- Gunicorn for WSGI server

## Prerequisites

### System Requirements
- Python 3.11 or higher
- PostgreSQL 13 or higher
- Webcam for live video (optional)
- Modern web browser with WebRTC support

### Development Environment
- Virtual environment (venv)
- Git for version control
- Docker and Docker Compose
- Code editor (VS Code recommended)

## Installation and Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/ekkirinaldi/workshop-face-recognition.git
cd workshop-face-recognition
```

### Step 2: Create and Activate Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a `.env` file in the project root with the following content:
```bash
FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=postgresql:///face_recognition
SECRET_KEY=your-secret-key-here
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

### Step 5: Set Up PostgreSQL Database
```bash
# Install PostgreSQL if not already installed
# On macOS:
brew install postgresql
# On Ubuntu:
sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL service
# On macOS:
brew services start postgresql
# On Ubuntu:
sudo service postgresql start

# Create database
createdb face_recognition
```

### Step 6: Initialize the Database
```bash
# Make sure you're in the project root directory and virtual environment is activated
# Set PYTHONPATH to include the current directory
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the database initialization script
python scripts/init_db.py

# Verify the database was initialized correctly
psql face_recognition -c "\dt"
```

### Step 7: Set Up Redis
```bash
# Install Redis if not already installed
# On macOS:
brew install redis
# On Ubuntu:
sudo apt-get install redis-server

# Start Redis service
# On macOS:
brew services start redis
# On Ubuntu:
sudo service redis-server start
```

### Step 8: Create Required Directories
```bash
mkdir -p uploads logs
```

### Step 9: Start the Application
```bash
# Make sure you're in the project root directory and virtual environment is activated
python wsgi.py
```

### Step 10: Access the Application
- Open your web browser and navigate to http://localhost:5000
- You should see the face recognition interface
- Try uploading an image to test face detection

### Troubleshooting Common Issues

1. **Database Initialization Issues**
   - Ensure PostgreSQL is running: `brew services list | grep postgresql` (macOS) or `sudo service postgresql status` (Ubuntu)
   - Verify database exists: `createdb face_recognition`
   - Check PYTHONPATH: `echo $PYTHONPATH`
   - Ensure virtual environment is activated

2. **Application Startup Issues**
   - Verify all environment variables are set in `.env`
   - Check all required directories exist (`uploads`, `logs`)
   - Ensure all dependencies are installed: `pip list`
   - Check application logs in `logs/app.log`

## Running the Application

### Development Mode

1. **Start the Development Server**
   ```bash
   # Make sure you're in the project directory and virtual environment is activated
   python wsgi.py
   ```

2. **Access the Application**
   - Main interface: http://localhost:5000
   - Admin interface: http://localhost:5000/admin

3. **Verify Installation**
   - Open your browser and navigate to http://localhost:5000
   - You should see the face recognition interface
   - Try uploading an image to test face detection

### Production Mode (Docker)

1. **Build and Start Containers**
   ```bash
   docker-compose up --build
   ```

2. **Access the Application**
   - Main interface: http://localhost:5000
   - Admin interface: http://localhost:5000/admin

3. **Monitor Logs**
   ```bash
   docker-compose logs -f
   ```

## Database Management

### Initializing the Database
The `init_db.py` script sets up the database schema and initializes required tables. Here's how to use it:

1. **Make sure PostgreSQL is running**
   ```bash
   # Check PostgreSQL status
   # On macOS:
   brew services list | grep postgresql
   # On Ubuntu:
   sudo service postgresql status
   ```

2. **Run the initialization script**
   ```bash
   # From the project root directory
   PYTHONPATH=. python scripts/init_db.py
   ```

3. **Verify the database**
   ```bash
   # Connect to PostgreSQL
   psql face_recognition

   # List tables
   \dt

   # Exit PostgreSQL
   \q
   ```

### Database Backup and Restore

1. **Create a Backup**
   ```bash
   pg_dump face_recognition > backup.sql
   ```

2. **Restore from Backup**
   ```bash
   psql face_recognition < backup.sql
   ```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check DATABASE_URL in .env file
   - Ensure database exists: `createdb face_recognition`

2. **File Upload Issues**
   - Check UPLOAD_FOLDER permissions
   - Verify MAX_CONTENT_LENGTH setting
   - Ensure directory exists: `mkdir -p uploads`

4. **Face Recognition Errors**
   - Verify OpenCV installation
   - Check face_recognition library version
   - Test with sample images

### Logs
- Development logs: `logs/app.log`
- Docker logs: `docker-compose logs -f`
- System logs: Check system logs for service errors

## Project Structure

```
face-recognition-workshop/
├── app/
│   ├── models/
│   │   ├── face_recognition.py    # Face detection and recognition logic
│   │   ├── database.py           # Database models and operations
│   │   └── security.py           # Security and encryption
│   ├── routes/
│   │   ├── main.py              # Main application routes
│   │   ├── api.py               # API endpoints
│   │   └── admin.py             # Admin interface routes
│   ├── static/
│   │   ├── css/                 # Stylesheets
│   │   ├── js/                  # JavaScript files
│   │   └── images/              # Static images
│   ├── templates/
│   │   ├── base.html           # Base template
│   │   ├── index.html          # Main page
│   │   └── admin/              # Admin templates
│   ├── config.py               # Configuration settings
│   └── __init__.py             # Application factory
├── scripts/
│   ├── init_db.py             # Database initialization
│   └── backup.py              # Backup utilities
├── tests/
│   ├── test_face_recognition.py
│   ├── test_api.py
│   └── test_database.py
├── uploads/                   # User uploaded files
├── logs/                     # Application logs
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker services
└── README.md               # Project documentation
```

## API Documentation

### Face Recognition Endpoints

#### POST /api/recognize
Recognize faces in an uploaded image.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Parameters:
  - image: Image file (required)
  - threshold: Matching threshold (optional, default: 0.6)

**Response:**
```json
{
  "faces": [
    {
      "location": [x, y, width, height],
      "confidence": 0.95,
      "user_id": 123,
      "name": "John Doe"
    }
  ]
}
```

#### POST /api/faces
Add a new face encoding to the database.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Parameters:
  - image: Image file (required)
  - user_id: User ID (required)
  - name: User name (required)

### User Management Endpoints

#### GET /api/users
List all users.

#### POST /api/users
Create a new user.

#### GET /api/users/<id>
Get user details.

#### PUT /api/users/<id>
Update user information.

#### DELETE /api/users/<id>
Delete a user.

## Security Considerations

### Data Protection
- Face encodings are encrypted before storage
- Secure file handling with unique filenames
- Input validation and sanitization
- Rate limiting on API endpoints

### Access Control
- Role-based access control (RBAC)
- JWT token authentication
- Session management
- API key authentication

### Best Practices
- Regular security audits
- Dependency updates
- Error logging
- Backup procedures

## Performance Optimization

### Caching
- Redis caching for face encodings
- LRU cache for frequently accessed data
- Response caching for API endpoints

### Resource Management
- Connection pooling for database
- Batch processing for multiple faces
- Resource monitoring and limits
- Load balancing configuration

### Scaling
- Horizontal scaling with Docker
- Database replication
- Redis clustering
- Load balancer configuration

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenCV for computer vision capabilities
- face_recognition library for face detection and recognition
- Flask community for the web framework
- PostgreSQL for the database system
- Redis for caching and task queue 