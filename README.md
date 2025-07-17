# AI Doctor 2.0 - Enhanced Medical Diagnosis Platform

AI Doctor 2.0 is a comprehensive medical diagnosis platform that uses advanced AI to analyze skin images and voice-recorded symptoms, providing instant medical insights and solutions. Built with FastAPI and modern web technologies, it features a professional medical-grade UI, drag-and-drop image upload, voice recording, and audio responses.

## Features

### 🔬 Medical Analysis
- **Image Analysis**: Upload skin images for instant AI-powered diagnosis
- **Voice Symptoms**: Record and transcribe symptoms using advanced speech-to-text
- **Comprehensive Reports**: Detailed diagnosis with confidence levels and treatment recommendations
- **Audio Responses**: Text-to-speech medical advice for accessibility

### 🎨 Modern Interface
- **Professional Medical UI**: Clean, modern design optimized for healthcare
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Drag & Drop Upload**: Intuitive file upload with preview
- **Real-time Feedback**: Loading states, progress indicators, and instant validation
- **PWA Support**: Install as a web app for offline capabilities

### 🔧 Technical Features
- **FastAPI Backend**: High-performance async API with automatic documentation
- **Modular Architecture**: Clean separation of concerns with services and models
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Health Monitoring**: Built-in health checks and system status monitoring
- **Security**: Input validation, file type checking, and secure file handling

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation and settings management
- **GROQ**: Advanced AI models for vision and speech processing
- **gTTS**: Google Text-to-Speech for audio responses
- **Jinja2**: Template engine for server-side rendering

### Frontend
- **Vanilla JavaScript**: Modern ES6+ with no framework dependencies
- **CSS3**: Custom CSS with CSS Grid, Flexbox, and animations
- **HTML5**: Semantic markup with accessibility features
- **Service Worker**: PWA capabilities for offline functionality

### AI & Processing
- **GROQ Vision Models**: Advanced image analysis for medical diagnosis
- **Whisper**: State-of-the-art speech-to-text transcription
- **Google TTS**: High-quality text-to-speech synthesis

## Getting Started

### Prerequisites
- Python 3.8 or higher
- GROQ API key (get from [console.groq.com](https://console.groq.com/))
- FFmpeg and PortAudio (for audio processing)

### Quick Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai-doctor-2.0
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

5. **Open your browser**:
   Navigate to [http://localhost:8000](http://localhost:8000)

### System Dependencies

#### macOS
```bash
brew install ffmpeg portaudio
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg portaudio19-dev
```

#### Windows
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Add FFmpeg to your system PATH
3. Install PortAudio from [portaudio.com](http://www.portaudio.com/download.html)

## Project Structure

```
ai-doctor-2.0/
├── app/
│   ├── api/                 # API endpoints
│   │   ├── diagnosis.py     # Medical diagnosis endpoints
│   │   └── health.py        # Health check endpoints
│   ├── core/                # Core application logic
│   │   ├── config.py        # Configuration settings
│   │   └── exceptions.py    # Custom exceptions
│   ├── models/              # Data models
│   │   └── schemas.py       # Pydantic models
│   ├── services/            # Business logic services
│   │   ├── ai_service.py    # AI processing service
│   │   ├── audio_service.py # Audio processing service
│   │   └── file_service.py  # File handling service
│   ├── static/              # Static assets
│   │   ├── css/            # Stylesheets
│   │   ├── js/             # JavaScript files
│   │   └── images/         # Images and icons
│   └── templates/           # HTML templates
├── tests/                   # Test files
├── docs/                    # Documentation
├── uploads/                 # Uploaded files (created automatically)
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── .env.example            # Environment variables template
```

## API Documentation

Once the application is running, visit:
- **Interactive API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative Docs**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check**: [http://localhost:8000/health/](http://localhost:8000/health/)

### Key Endpoints

- `POST /api/diagnosis/analyze` - Analyze medical image with optional symptoms
- `POST /api/diagnosis/audio-response` - Generate audio response from text
- `POST /api/diagnosis/transcribe` - Transcribe audio to text
- `GET /health/` - System health check
- `GET /api/info` - API information

## Usage Guide

### Basic Diagnosis
1. **Upload Image**: Drag and drop or click to select a medical image
2. **Add Symptoms** (Optional): Type or record your symptoms
3. **Get Diagnosis**: Click the analyze button for instant results
4. **Review Results**: View diagnosis, confidence level, and recommendations
5. **Listen to Response**: Play the audio version of the diagnosis

### Voice Features
- **Record Symptoms**: Use the microphone to record symptom descriptions
- **Audio Playback**: Listen to AI-generated medical advice
- **Transcription**: View text transcription of recorded audio

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | GROQ API key (required) | - |
| `APP_NAME` | Application name | AI Doctor |
| `DEBUG` | Enable debug mode | false |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |
| `MAX_FILE_SIZE` | Max upload size in bytes | 5242880 |
| `UPLOAD_DIR` | Upload directory | uploads |

### Model Configuration

- **Vision Model**: `meta-llama/llama-4-scout-17b-16e-instruct`
- **Speech-to-Text**: `whisper-large-v3`
- **Text-to-Speech**: Google TTS (gTTS)

## Development

### Running in Development Mode
```bash
# Enable debug mode in .env
DEBUG=true

# Run with auto-reload
python main.py
```

### Testing
```bash
# Run health check
python -c "import requests; print(requests.get('http://localhost:8000/health/').json())"

# Test API connection
python test_api_connection.py
```

### Code Quality
```bash
# Format code
black app/ main.py

# Lint code
flake8 app/ main.py

# Type checking
mypy app/ main.py
```

## Deployment

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

### Production Considerations
- Set `DEBUG=false` in production
- Use a reverse proxy (nginx) for static files
- Configure proper CORS origins
- Set up SSL/TLS certificates
- Monitor logs and health endpoints
- Implement rate limiting
- Use a production WSGI server

## Troubleshooting

### Common Issues

1. **GROQ API Key Error**
   - Ensure you have a valid API key from [console.groq.com](https://console.groq.com/)
   - Check that the key is properly set in your `.env` file

2. **Audio Recording Issues**
   - Verify microphone permissions in your browser
   - Check that PortAudio is properly installed
   - Ensure FFmpeg is available in your system PATH

3. **File Upload Problems**
   - Check file size limits (default 5MB)
   - Verify supported file formats (JPEG, PNG, WebP)
   - Ensure upload directory has write permissions

4. **Model Loading Errors**
   - Verify internet connection for model downloads
   - Check GROQ service status
   - Ensure sufficient system memory

### Getting Help

- Check the [health endpoint](http://localhost:8000/health/) for system status
- Review application logs for detailed error messages
- Test API connectivity with the provided test scripts

## Security & Privacy

- **Data Privacy**: Uploaded images are processed locally and deleted after analysis
- **No Data Storage**: No personal medical data is permanently stored
- **Secure Processing**: All file uploads are validated and sanitized
- **HTTPS Ready**: Designed for secure HTTPS deployment

## Medical Disclaimer

⚠️ **Important**: This AI diagnosis tool is for educational and informational purposes only. It does not replace professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider for medical concerns, especially for serious or urgent conditions.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **GROQ** for providing advanced AI models
- **FastAPI** for the excellent web framework
- **Google** for Text-to-Speech services
- **OpenAI** for Whisper speech recognition

---

**AI Doctor 2.0** - Empowering healthcare with artificial intelligence

© 2025 AI Doctor Team. All rights reserved.

# Project Setup Guide

This guide provides step-by-step instructions to set up your project environment, including the installation of FFmpeg and PortAudio across macOS, Linux, and Windows, as well as setting up a Python virtual environment using Pipenv, pip, or conda.

## Table of Contents

1. [Installing FFmpeg and PortAudio](#installing-ffmpeg-and-portaudio)
   - [macOS](#macos)
   - [Linux](#linux)
   - [Windows](#windows)
2. [Setting Up a Python Virtual Environment](#setting-up-a-python-virtual-environment)
   - [Using Pipenv](#using-pipenv)
   - [Using pip and venv](#using-pip-and-venv)
   - [Using Conda](#using-conda)
3. [Running the application](#project-phases-and-python-commands)

## Installing FFmpeg and PortAudio

### macOS

1. **Install Homebrew** (if not already installed):

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install FFmpeg and PortAudio:**

   ```bash
   brew install ffmpeg portaudio
   ```


### Linux
For Debian-based distributions (e.g., Ubuntu):

1. **Update the package list**

```
sudo apt update
```

2. **Install FFmpeg and PortAudio:**
```
sudo apt install ffmpeg portaudio19-dev
```

### Windows

#### Download FFmpeg:
1. Visit the official FFmpeg download page: [FFmpeg Downloads](https://ffmpeg.org/download.html)
2. Navigate to the Windows builds section and download the latest static build.

#### Extract and Set Up FFmpeg:
1. Extract the downloaded ZIP file to a folder (e.g., `C:\ffmpeg`).
2. Add the `bin` directory to your system's PATH:
   - Search for "Environment Variables" in the Start menu.
   - Click on "Edit the system environment variables."
   - In the System Properties window, click on "Environment Variables."
   - Under "System variables," select the "Path" variable and click "Edit."
   - Click "New" and add the path to the `bin` directory (e.g., `C:\ffmpeg\bin`).
   - Click "OK" to apply the changes.

#### Install PortAudio:
1. Download the PortAudio binaries from the official website: [PortAudio Downloads](http://www.portaudio.com/download.html)
2. Follow the installation instructions provided on the website.

---

## Setting Up a Python Virtual Environment

### Using Pipenv
1. **Install Pipenv (if not already installed):**  
```
pip install pipenv
```

2. **Install Dependencies with Pipenv:** 

```
pipenv install
```

3. **Activate the Virtual Environment:** 

```
pipenv shell
```

---

### Using `pip` and `venv`
#### Create a Virtual Environment:
```
python -m venv venv
```

#### Activate the Virtual Environment:
**macOS/Linux:**
```
source venv/bin/activate
```

**Windows:**
```
venv\Scripts\activate
```

#### Install Dependencies:
```
pip install -r requirements.txt
```

---

### Using Conda
#### Create a Conda Environment:
```
conda create --name myenv python=3.11
```

#### Activate the Conda Environment:
```
conda activate myenv
```

#### Install Dependencies:
```
pip install -r requirements.txt
```


# Project Phases and Python Commands

## Phase 1: Brain of the doctor
```
python brain_of_the_doctor.py
```

## Phase 2: Voice of the patient
```
python voice_of_the_patient.py
```

## Phase 3: Voice of the doctor
```
python voice_of_the_doctor.py
```

## Phase 4: Setup Gradio UI
```
python gradio_app.py
```

