import openai
import speech_recognition as sr
import pyttsx3
import random


engine = pyttsx3.init()
openai.api_key = 'SHHHH'
personality_responses = {
    "greeting": ["Hey there! What's up?", "Hello! How's it going?", "Hi! What’s on your mind?"],
    "fallback": ["Hmm, that's interesting. Tell me more.", "I’m not sure I get it, but let’s roll with it!", "Oh really? Go on..."],
    "goodbye": ["See you later!", "Catch you later!", "Take care!"],
    "confused": ["I didn’t quite catch that. Can you say it again?", "Sorry, could you repeat that?", "Hmm, I’m not sure what you mean."]
}

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture speech and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for 'Osmo'...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-US')
        print(f"User said: {query}")
    except Exception as e:
        print("Sorry, I did not catch that.")
        return None

    return query

def chat_with_ai(prompt):
    """Send the user's prompt to the AI model and return the response."""
    response = openai.Completion.create(
        engine="text-davinci-003",  # try 4o Model
        prompt=f"You're a friendly and personable character named Osmo. Engage in a natural conversation with the user. {prompt}",
        max_tokens=150,
        temperature=0.8,  # Higher temperature for more creative responses
        top_p=0.9  # Adjust to increase response variety
    )
    return response.choices[0].text.strip()

def get_random_response(response_type):
    """Get a random response from the personality traits."""
    return random.choice(personality_responses[response_type])

def main():
    while True:
        # Listen for activatio "Osmo"
        user_input = listen()
        if user_input and "osmo" in user_input.lower():
            speak(get_random_response("greeting"))

            # Listen for the actual command 
            user_input = listen()
            if user_input:
                if "bye" in user_input.lower() or "goodbye" in user_input.lower():
                    speak(get_random_response("goodbye"))
                    break  # Break when "Goodbye" is said

                ai_response = chat_with_ai(user_input)
                
                if not ai_response.strip():
                    # If the AI response is empty or doesn't make sense, use a fallback response
                    # Part of documentation still need to dive into it
                    ai_response = get_random_response("fallback")
                
                print(f"Osmo: {ai_response}")
                speak(ai_response)
            else:
                speak(get_random_response("confused"))

if __name__ == "__main__":
    main()
