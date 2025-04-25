# Face Recognition System

A real-time face recognition system with emotion detection and face capture capabilities.

## Features

- Real-time face detection and recognition
- Emotion detection
- Face capture and storage
- User management interface

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Webcam access

## Setup

Run PostgreSQL
```bash
docker run --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=face_recognition -p 5432:5432 -d postgres:latest
```

1. Clone the repository:
```bash
git clone https://github.com/ekkirinaldi/workshop-face-recognition
cd face-recognition-material
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start PostgreSQL using Docker:
```bash
docker-compose up -d
```

5. Initialize the database:
```bash
flask db upgrade
```

6. Set environment variables:
```bash
export FLASK_APP=app
export FLASK_ENV=development
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/face_recognition
```

7. Run the application:
```bash
flask run
```

## Usage

1. Access the main interface at `http://localhost:5000`
2. Access the admin interface at `http://localhost:5000/admin`
3. Add users and their face encodings through the admin interface
4. The main interface will automatically detect and recognize faces

## Docker Compose Configuration

The `docker-compose.yml` file sets up:
- PostgreSQL database
- Persistent volume for data storage
- Network configuration

## License

MIT License