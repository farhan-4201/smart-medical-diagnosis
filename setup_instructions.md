# AI Doctor Setup Instructions

## Step 1: Get GROQ API Key

1. Go to [https://console.groq.com/](https://console.groq.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key

## Step 2: Configure Environment Variables

1. Open your `.env` file
2. Replace `your_groq_api_key_here` with your actual GROQ API key:
   ```
   GROQ_API_KEY=gsk_your_actual_groq_api_key_here
   ```

## Step 3: Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using pipenv
pipenv install
pipenv shell
```

## Step 4: Test Your Setup

```bash
python test_api_connection.py
```

## Step 5: Run the Application

### Option 1: Run Backend Only
```bash
python run_backend.py
```

### Option 2: Run Full Application
```bash
# Terminal 1 - Backend
python main.py

# Terminal 2 - Frontend (in frontend directory)
cd frontend
npm install
npm run dev
```

### Option 3: Run Gradio Interface
```bash
python gradio_app.py
```

## Troubleshooting

### Common Issues:

1. **"GROQ_API_KEY not found"**
   - Make sure you have added your API key to the `.env` file
   - Ensure there are no spaces around the `=` sign

2. **"Module not found" errors**
   - Run `pip install -r requirements.txt`
   - If using pipenv: `pipenv install`

3. **Audio issues**
   - Make sure you have installed system dependencies:
     - macOS: `brew install ffmpeg portaudio`
     - Ubuntu: `sudo apt install ffmpeg portaudio19-dev`
     - Windows: Follow the README instructions

4. **CORS errors in frontend**
   - Make sure the backend is running on port 8000
   - Check that the frontend is making requests to the correct URL

## API Endpoints

- `GET /` - Health check
- `POST /predict/` - Upload image for analysis

## Frontend URLs

- Development: http://localhost:3000
- Gradio Interface: http://localhost:7860 (when running gradio_app.py)