from flask import Flask, request, render_template, jsonify
from app.utils.stt import transcribe_audio
from app.utils.ftt import download_and_extract_text, upload_to_bucket
from app.utils.chat import generate_content, translate_text

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
  file = request.files['file']
  course = request.form['course']

  if file:
    file_path = f"/tmp/{file.filename}"
    file.save(file_path)

    upload_to_bucket(file_path, f"{course}/{file.filename}")
    text = download_and_extract_text(course)

    return jsonify({'text': text})
  
@app.route('/chat', methods=['POST'])
def chat():
  data = request.json
  lect_data = data.get('data')
  user_input = data.get('text') + "Энэ асуултанд дараах мэдээллийн сайтар уншиж ойлгоод, түүнд үндэслэн  хариулна уу. " + lect_data
  api_key = "AIzaSyCEwEdteDQYtxpTqMV9ftS5VJ69wdfsBWo"

  translated_text = translate_text(user_input, 'en')

  response_json = generate_content(translated_text, api_key)

  try:
    print(translated_text)
    response_text = response_json['candidates'][0]['content']['parts'][0]['text']
    translated_response = translate_text(response_text, 'mn')
    return jsonify({'response': translated_response})
  except KeyError as e:
    return jsonify({'error': f"Error parsing response: {e}"}) 