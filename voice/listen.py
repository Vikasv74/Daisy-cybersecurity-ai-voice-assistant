import speech_recognition as sr
import whisper
import os

def listen_to_user():
    recognizer = sr.Recognizer()
    
    print("[Daisy System] Loading Whisper Model... please wait...")
    # Using the base model for a good balance of speed and accuracy on a VM
    model = whisper.load_model("base")
    print("[Daisy System] Model loaded successfully!")

    with sr.Microphone() as source:
        print("\n[Daisy System] Adjusting for background noise... please be quiet.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("[Daisy System] Listening... Speak now!")
        audio = recognizer.listen(source)
        
    try:
        print("[Daisy System] Processing speech...")
        # Save temporary audio file for Whisper processing
        with open("temp_audio.wav", "wb") as f:
            f.write(audio.get_wav_data())
            
        # Transcribe audio using the Whisper model
        result = model.transcribe("temp_audio.wav")
        text = result["text"].strip()
        
        print(f"You said: {text}")
        
        # Clean up the temporary file
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")
            
        return text

    except Exception as e:
        print(f"[Daisy System] An error occurred: {e}")
        return None

if __name__ == "__main__":
    listen_to_user()
