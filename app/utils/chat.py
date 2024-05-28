from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import requests

client_file = "./key.json"
credentials = service_account.Credentials.from_service_account_file(client_file)
client = translate.Client(credentials=credentials)

def translate_text(text, target_language):
    try:
        translated = client.translate(text, target_language=target_language)
        return translated['translatedText']
    except Exception as e:
        print(f"Error translating text: {e}")
        return None
    
def generate_content(translated_text, api_key):
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": translated_text
                    }
                ]
            }
        ]
    }
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}'
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error in API response: {response.text}")
            return None
    except Exception as e:
        print(f"Error sending request: {e}")
        return None