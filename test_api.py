import requests
import json

# Aapka Flask server ka local address
# Yeh wahi address hai jo aapke 'ai_listener_flask.py' chalane par terminal mein dikh raha hai: http://127.0.0.1:5000
API_URL = "http://127.0.0.1:5000/ask"

def test_api():
    question_text = input("AI server ko sawaal bhejein (ya 'exit' type karein): ")
    if question_text.lower() == 'exit':
        return False

    payload = {"question": question_text}
    headers = {"Content-Type": "application/json"}

    try:
        # Flask server ko POST request bhej rahe hain
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # HTTP errors (jaise 404, 500) ke liye exception raise karega

        result = response.json()
        if "answer" in result:
            print("\n--- AI Server Se Jawaab ---")
            print(result["answer"])
            print("---------------------------\n")
        elif "error" in result:
            print("\n--- AI Server Error ---")
            print(result["error"])
            print("-------------------------\n")
        else:
            print("Server se unexpected response mila.")

    except requests.exceptions.ConnectionError:
        print("\nError: Server se connect nahi kar paya. Kya Flask server chal raha hai?")
        print(" सुनिश्चित करें कि 'ai_listener_flask.py' वाला server Terminal 1 में चल रहा है.")
    except requests.exceptions.RequestException as e:
        print(f"\nRequest error: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

    return True

if __name__ == "__main__":
    print("--- Flask API Server Tester ---")
    print("Note: Pehle 'ai_listener_flask.py' server ko chalana zaroori hai.")
    while test_api():
        pass
    print("Tester band kiya gaya.")