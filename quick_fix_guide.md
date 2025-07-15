# Quick Fix Guide for AI Doctor Project

## The Problem
Your project is failing because it needs a **GROQ API key** but you only have other API keys configured.

## The Solution

### Step 1: Get GROQ API Key
1. Go to [https://console.groq.com/](https://console.groq.com/)
2. Sign up or log in
3. Navigate to "API Keys" section
4. Create a new API key
5. Copy the key (starts with `gsk_`)

### Step 2: Update Your .env File
Replace `your_groq_api_key_here` with your actual GROQ API key:
```
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
```

### Step 3: Test Your Setup
```bash
python check_api_setup.py
```

### Step 4: Run Your Application
```bash
# Option 1: FastAPI Backend + Next.js Frontend
python main.py
# Then in another terminal:
cd frontend && npm run dev

# Option 2: Gradio Interface (simpler)
python gradio_app.py
```

## Why GROQ?
Your project uses GROQ for:
- **Image Analysis**: Analyzing skin conditions using vision models
- **Speech-to-Text**: Converting patient voice recordings to text
- **Text Generation**: Generating medical responses

## Current API Usage in Your Project:
- ✅ **GROQ**: Required (missing in your .env)
- ❌ **HuggingFace**: Not used in current code
- ❌ **AssemblyAI**: Not used in current code  
- ❌ **Roboflow**: Not used in current code

## Quick Test Commands:
```bash
# Check if everything is working
python check_api_setup.py

# Run the Gradio interface (easiest to test)
python gradio_app.py

# Run the full stack
python main.py  # Backend
cd frontend && npm run dev  # Frontend
```