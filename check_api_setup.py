#!/usr/bin/env python3
"""
Quick script to check if your API setup is working
"""

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def check_groq_api():
    """Check if GROQ API key is configured and working"""
    print("🔍 Checking GROQ API configuration...")
    
    groq_api_key = os.environ.get("GROQ_API_KEY")
    
    if not groq_api_key:
        print("❌ GROQ_API_KEY not found in .env file")
        print("Please add: GROQ_API_KEY=your_actual_key_here")
        return False
    
    if groq_api_key == "your_groq_api_key_here":
        print("❌ GROQ_API_KEY is still set to placeholder value")
        print("Please replace with your actual GROQ API key from https://console.groq.com/")
        return False
    
    try:
        from groq import Groq
        client = Groq(api_key=groq_api_key)
        
        # Test with a simple completion
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": "Hello, test message"}],
            model="llama-3.1-8b-instant"
        )
        
        print("✅ GROQ API is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ GROQ API error: {str(e)}")
        print("Please check your API key at https://console.groq.com/")
        return False

def check_image_analysis():
    """Test image analysis with a sample image"""
    print("\n🔍 Testing image analysis...")
    
    # Check if we have test images
    test_images = ["acne.jpg", "acne2.jpg", "skin_rash.jpg"]
    available_image = None
    
    for img in test_images:
        if os.path.exists(img):
            available_image = img
            break
    
    if not available_image:
        print("⚠️ No test images found, skipping image analysis test")
        return True
    
    try:
        from brain_of_the_doctor import encode_image, analyze_image_with_query
        
        encoded_image = encode_image(available_image)
        
        query = "What do you see in this medical image?"
        model = "meta-llama/llama-4-scout-17b-16e-instruct"
        
        result = analyze_image_with_query(query, model, encoded_image)
        print(f"✅ Image analysis working! Result preview: {result[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Image analysis error: {str(e)}")
        return False

def main():
    print("🚀 AI Doctor - API Configuration Check\n")
    
    # Check GROQ API
    groq_ok = check_groq_api()
    
    if groq_ok:
        # Test image analysis if GROQ is working
        image_ok = check_image_analysis()
        
        if image_ok:
            print("\n✅ All systems ready! You can now run:")
            print("   python main.py  (for FastAPI backend)")
            print("   python gradio_app.py  (for Gradio interface)")
        else:
            print("\n⚠️ Image analysis has issues, but basic API is working")
    else:
        print("\n❌ Please fix GROQ API configuration first")
        print("\nSteps to fix:")
        print("1. Go to https://console.groq.com/")
        print("2. Sign up/login and get your API key")
        print("3. Replace 'your_groq_api_key_here' in .env with your actual key")

if __name__ == "__main__":
    main()