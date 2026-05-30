import pyttsx3

def speak(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    
    # Configure speaking speed and volume
    engine.setProperty('rate', 170)    # Slightly slower pace sounds cleaner for espeak female voices
    engine.setProperty('volume', 1.0)  
    
    # Directly target the espeak female voice variant 
    # Options to try: 'english+f1', 'english+f2', 'english+f3', 'english+f4'
    engine.setProperty('voice', 'english+f2') 

    print(f"Daisy: {text}")
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak("Hello! This is Daisy. How can i help you.")
