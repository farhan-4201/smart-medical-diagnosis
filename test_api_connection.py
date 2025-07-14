#!/usr/bin/env python3
"""
Test script to verify API connections and functionality
"""

from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

def test_groq_api():
    """Test GROQ API connection"""
    print("Testing GROQ API connection...")
    
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        print("❌ GROQ_API_KEY not found in environment variables")
        return False
    
    try:
        from groq import Groq
        client = Groq(api_key=groq_api_key)
        
        # Test with a simple text completion
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": "Hello, this is a test."}],
            model="llama-3.1-8b-instant"  # Using a simpler model for testing
        )
        
        print("✅ GROQ API connection successful")
        print(f"Response: {response.choices[0].message.content[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ GROQ API connection failed: {str(e)}")
        return False

def test_image_analysis():
    """Test image analysis functionality"""
    print("\nTesting image analysis...")
    
    # Check if test image exists
    test_images = ["acne.jpg", "acne2.jpg", "skin_rash.jpg"]
    test_image = None
    
    for img in test_images:
        if os.path.exists(img):
            test_image = img
            break
    
    if not test_image:
        print("❌ No test images found. Please ensure you have a test image in the project directory.")
        return False
    
    try:
        from brain_of_the_doctor import encode_image, analyze_image_with_query
        
        # Test image encoding
        encoded_image = encode_image(test_image)
        print(f"✅ Image encoding successful for {test_image}")
        
        # Test image analysis
        query = "What do you see in this image?"
        model = "llama-3.1-8b-instant"  # Using simpler model for testing
        
        result = analyze_image_with_query(query, model, encoded_image)
        print("✅ Image analysis successful")
        print(f"Analysis result: {result[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Image analysis failed: {str(e)}")
        return False

def test_audio_functionality():
    """Test audio functionality"""
    print("\nTesting audio functionality...")
    
    try:
        from voice_of_the_doctor import text_to_speech_with_gtts
        
        # Test text-to-speech
        test_text = "This is a test of the text to speech functionality."
        output_file = "test_audio.mp3"
        
        text_to_speech_with_gtts(test_text, output_file)
        
        if os.path.exists(output_file):
            print("✅ Text-to-speech functionality working")
            os.remove(output_file)  # Clean up
            return True
        else:
            print("❌ Text-to-speech failed to create audio file")
            return False
            
    except Exception as e:
        print(f"❌ Audio functionality failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🔍 Running API and functionality tests...\n")
    
    tests = [
        test_groq_api,
        test_image_analysis,
        test_audio_functionality
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} tests passed")
    
    if not all(results):
        print("\n🚨 Some tests failed. Please check the issues above and:")
        print("1. Ensure you have a valid GROQ_API_KEY in your .env file")
        print("2. Get your GROQ API key from: https://console.groq.com/")
        print("3. Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    else:
        print("\n✅ All tests passed! Your API configuration is working correctly.")

if __name__ == "__main__":
    main()