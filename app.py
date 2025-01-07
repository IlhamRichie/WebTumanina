import os
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from datetime import datetime
import tensorflow as tf
import pickle
import numpy as np
import json
from nltk.stem import WordNetLemmatizer

# Setup Flask app
app = Flask(__name__, template_folder='templates')
CORS(app)  # Enable CORS


# Secret key and database config
app.secret_key = 'atmins'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'admin_tumanina'

# Upload folder config
app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize MySQL
mysql = MySQL()
mysql.init_app(app)

# Load TensorFlow model and related files
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Optional: Disable oneDNN warnings
model = tf.keras.models.load_model('model\\chatbot_model.h5')
with open('model/words.pkl', 'rb') as f:
    words = pickle.load(f)
with open('model/classes.pkl', 'rb') as f:
    classes = pickle.load(f)
with open('model/sholatislam.json') as f:
    intents = json.load(f)

lemmatizer = WordNetLemmatizer()

def clean_up_sentence(sentence):
    sentence_words = sentence.split()
    return [lemmatizer.lemmatize(word.lower()) for word in sentence_words]

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)

# Filters
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%dT%H:%M'):
    if isinstance(value, datetime):
        return value.strftime(format)
    return value

# Routes
@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'response': "Data tidak valid. Harap kirim pesan dalam format JSON."})

        message = data.get('message', '')
        if not message:
            return jsonify({'response': "Pesan kosong. Harap masukkan teks pertanyaan."})

        # Predict class
        input_data = bow(message, words)
        res = model.predict(np.array([input_data]))[0]

        index = np.argmax(res)
        tag = classes[index]

        if res[index] < 0.5:  # Confidence threshold
            return jsonify({'response': "Maaf, saya tidak yakin dengan jawaban saya."})

        # Get response
        for intent in intents['intents']:
            if intent['tag'] == tag:
                response = np.random.choice(intent['responses'])
                return jsonify({'response': response})

        return jsonify({'response': "Maaf, saya tidak menemukan jawaban yang relevan."})
    except Exception as e:
        return jsonify({'response': f"Terjadi kesalahan: {str(e)}"})

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

