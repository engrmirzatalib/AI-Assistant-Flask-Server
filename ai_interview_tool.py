import speech_recognition as sr
import google.generativeai as genai
import os

# --- Configuration (API Key Yahan Daalni Hai!) ---
# Google Gemini API key: https://aistudio.google.com/app/apikey
# Yahan apni asli API key paste karni hai double quotes ke andar.
# Example: API_KEY = "AIzaSyC..."
API_KEY = "AIzaSyBnUe8PfgZOWY62U33POQBaSTSnLt4B7l0" # <-- Yeh line dhyaan se change karni hai!

genai.configure(api_key=API_KEY)

# --- Speech-to-Text Setup ---
r = sr.Recognizer()

def listen_for_question():
    with sr.Microphone() as source:
        print("Bolne ke liye taiyar hoon... sawaal poochiye!")
        r.adjust_for_ambient_noise(source) # Aas-paas ke shor ko adjust karein
        try:
            # Sawaal sunne ke liye 5 second ka timeout, phrase limit 10 seconds
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Sawaal process kar raha hoon...")
            # Google Web Speech API se audio ko text mein badlein
            # en-IN = English (India), aap apni bhasha bhi set kar sakte ho
            question = r.recognize_google(audio, language="en-IN")
            print(f"Aapne poocha: {question}")
            return question
        except sr.UnknownValueError:
            print("Sawaal samajh nahi paya. Dobara koshish karein.")
            return None
        except sr.RequestError as e:
            print(f"Google Speech Recognition service se connect nahi kar paya; {e}")
            print("Internet connection ya API limit check karein.")
            return None
        except Exception as e:
            print(f"Sawaal sunte waqt koi error aa gayi: {e}")
            return None

# --- AI Model for Answer Generation (Gemini ka Upyog) ---
def get_ai_answer(question):
    if not question:
        return "Koi sawaal nahi mila, jawaab nahi de sakta."
    try:
        # 'gemini-pro' model use kar rahe hain
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        # AI ko batate hain ki woh interview assistant hai aur concise answer de
        response = model.generate_content(
            f"Aap ek interview assistant hain. Is interview question ka chota aur sahi jawaab dein:\n\nSawaal: {question}\n\nJawaab:",
            generation_config=genai.types.GenerationConfig(temperature=0.7) # Temperature se creativity control hoti hai
        )
        return response.text
    except Exception as e:
        return f"Jawaab banate waqt error aa gayi: {e}"

# --- Main Program Loop ---
if __name__ == "__main__":
    print("AI Interview Assistant Listener Tool shuru ho gaya hai. Band karne ke liye Ctrl+C dabayein.")
    while True:
        question_text = listen_for_question()
        if question_text:
            print("\nAI jawaab bana raha hai...")
            answer_text = get_ai_answer(question_text)
            print("\n--- AI Se Sujhaya Gaya Jawaab ---")
            print(answer_text)
            print("-----------------------------------\n")
            # Ye line aapko agla sawaal sunne se pehle Enter dabane ke liye rokegi.
            # Agar aap bina roke agla sawaal sunna chahte ho toh is line ko comment kar do (# laga do)
            # input("Agla sawaal sunne ke liye Enter dabayein...")
        else:
            print("Dobara koshish karte hain...")
        print("Agla sawaal sunne ke liye taiyar...\n")