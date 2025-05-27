import requests
import speech_recognition as sr

# ✅ Step 1: Add your Groq API Key here
groq_api_key = "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"  # <-- yahan apni asli key paste karna

# ✅ Step 2: Function to call Groq LLaMA3
def ask_groq(question):
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data
    )

    answer = response.json()["choices"][0]["message"]["content"]
    return answer

# ✅ Step 3: Voice Input
r = sr.Recognizer()
with sr.Microphone() as source:
    print("🎤 Bolna start kar... AI sun raha hai...")
    audio = r.listen(source)

try:
    question = r.recognize_google(audio)
    print(f"\n❓ Tuney pucha: {question}")
    
    print("\n🤖 AI jawab soch raha hai...")
    answer = ask_groq(question)
    
    print("\n✅ AI ka jawab:\n", answer)

except sr.UnknownValueError:
    print("❌ Voice samajh nahi aayi.")
except Exception as e:
    print("⚠️ Error:", e)
