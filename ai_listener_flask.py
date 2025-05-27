import requests
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Groq API Key Configuration ---
# Aapki asli Groq API key yahan daal di gayi hai.
# 'os.environ.get' wali line ko ab use nahi karenge.
GROQ_API_KEY = "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" # <-- Aapki Groq API key

if not GROQ_API_KEY:
    # Yeh error message tab dikhega jab yahan koi key nahi hogi.
    # Lekin ab kyunki aapki key yahan seedha paste ho gayi hai, ye error nahi aani chahiye.
    print("Error: GROQ_API_KEY is not set in the script.")
    exit()

# --- AI Model for Answer Generation (Groq / Llama3 ka Upyog) ---
def get_groq_answer(question):
    if not question:
        return "Koi sawaal nahi mila, jawaab nahi de sakta."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192", # Ya 'llama3-70b-8192' agar aapke paas access hai
        "messages": [
            {"role": "system", "content": "You are an interview assistant. Provide concise and accurate answers to interview questions."},
            {"role": "user", "content": f"Interview Question: {question}"}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }
    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        if data and data['choices'] and data['choices'][0]['message']['content']:
            # Yahan correction kiya gaya hai: .content ki jagah ['content']
            return data['choices'][0]['message']['content'].strip()
        else:
            return "Groq AI ko jawaab banane mein mushkil hui."
    except requests.exceptions.RequestException as e:
        return f"Groq API se connect nahi kar paya ya request error: {e}"
    except Exception as e:
        return f"Jawaab banate waqt koi error aa gayi: {e}"

# --- Flask API Endpoint ---
@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.json # Client (phone) se aane wala data (question)
    if not data or 'question' not in data:
        return jsonify({"error": "Invalid input. 'question' field is required."}), 400

    question = data['question']
    print(f"Received question from client: {question}")
    answer = get_groq_answer(question)
    print(f"Sending answer: {answer}")
    return jsonify({"answer": answer})

# --- Main Program (Server chalane ke liye) ---
if __name__ == '__main__':
    print("Flask API server shuru ho raha hai. Isko public karne ke liye deploy karna hoga.")
    app.run(host='0.0.0.0', port=5000, debug=True)
