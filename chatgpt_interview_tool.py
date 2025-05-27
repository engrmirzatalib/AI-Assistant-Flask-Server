import speech_recognition as sr
import openai
import os # Operating system modules for environment variables

# --- Configuration (OpenAI API Key Yahan Daalni Hai!) ---
# OpenAI API key: https://platform.openai.com/account/api-keys
# Ab API key seedhe code mein nahi hai. Yeh 'OPENAI_API_KEY' naam ke environment variable se read ki jayegi.
# Jab aap Render.com par deploy karoge, tab aapko yeh environment variable wahan set karna hoga.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if the API key is available
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY environment variable set nahi hai.")
    print("Kripya ise set karein ya Render.com par environment variables mein add karein.")
    # Exit or handle the error appropriately if the key is missing
    # For local testing, you can set it in your system's environment variables.
    # For Render.com, you will set it in their dashboard.

openai.api_key = OPENAI_API_KEY

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
            # Note: SpeechRecognition library Google API use karti hai yahan, OpenAI ki nahi
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

# --- AI Model for Answer Generation (ChatGPT / OpenAI ka Upyog) ---
def get_ai_answer(question):
    if not question:
        return "Koi sawaal nahi mila, jawaab nahi de sakta."
    try:
        # OpenAI chat completion API ka upyog
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", # Aap 'gpt-4o', 'gpt-4', ya koi aur available model bhi use kar sakte ho
            messages=[
                {"role": "system", "content": "You are an interview assistant. Provide concise and accurate answers to interview questions."},
                {"role": "user", "content": f"Interview Question: {question}"}
            ],
            max_tokens=150, # Jawaab ki lambai control karein
            temperature=0.7 # Creativity control karein
        )
        # Jawaab content nikalna
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content.strip()
        else:
            return "AI ko jawaab banane mein mushkil hui."

    except openai.APIError as e:
        return f"OpenAI API error aa gayi: {e}"
    except Exception as e:
        return f"Jawaab banate waqt koi error aa gayi: {e}"

# --- Main Program Loop ---
if __name__ == "__main__":
    print("ChatGPT Interview Assistant Listener Tool shuru ho gaya hai. Band karne ke liye Ctrl+C dabayein.")
    while True:
        question_text = listen_for_question()
        if question_text:
            print("\nAI jawaab bana raha hai...")
            answer_text = get_ai_answer(question_text)
            print("\n--- AI Se Sujhaya Gaya Jawaab (ChatGPT) ---")
            print(answer_text)
            print("-------------------------------------------\n")
        else:
            print("Dobara koshish karte hain...")
        print("Agla sawaal sunne ke liye taiyar...\n")
