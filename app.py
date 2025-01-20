import datetime
import os
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
import tensorflow as tf
import pickle
import numpy as np
from MySQLdb.cursors import DictCursor
import json
from nltk.stem import WordNetLemmatizer
from controllers.auth_controller import auth_bp
from controllers.sentiment_controller import sentiment_bp

from models.user_model import UserModel

# Setup Flask app
app = Flask(__name__, template_folder='templates')
CORS(app)

# Secret key and database config
app.secret_key = 'atmins'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'admin_tumanina'

# Upload folder config
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.register_blueprint(auth_bp)
app.register_blueprint(sentiment_bp)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize MySQL
mysql = MySQL(app)

# Load TensorFlow model and related files
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
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
@app.route('/admin/login', methods=['GET', 'POST'])
def users_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        admin = cur.fetchone()
        if admin:
            return render_template('dashboard.html')
        else:
            return render_template('login.html', error="Login failed.")
    return render_template('login.html')

@app.route('/admin/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/')
def index():
    # Get the current page, default to 1 if not provided
    page = request.args.get('page', 1, type=int)
    
    # Number of articles per page
    per_page = 3

    # Initialize cursor
    cur = mysql.connection.cursor(DictCursor)

    # Get total articles count
    cur.execute("SELECT COUNT(*) AS count FROM articles")
    total_articles = cur.fetchone()['count']

    # Calculate the total number of pages
    total_pages = (total_articles // per_page) + (1 if total_articles % per_page else 0)

    # Get articles for the current page
    offset = (page - 1) * per_page
    cur.execute("SELECT id, title, content, image FROM articles ORDER BY created_at DESC LIMIT %s OFFSET %s", (per_page, offset))
    articles = cur.fetchall()

    # Close cursor
    cur.close()

    # Render template and pass articles and pagination data
    return render_template('landing.html', articles=articles, current_page=page, total_pages=total_pages)



@app.route('/article-detail/<int:id>')
def article_detail(id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("SELECT * FROM articles WHERE id = %s", (id,))
    article = cur.fetchone()
    cur.close()
    return render_template('article_detail.html', article=article)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        if not message:
            return jsonify({'response': "Empty message. Please enter a question."})

        input_data = bow(message, words)
        res = model.predict(np.array([input_data]))[0]
        index = np.argmax(res)
        tag = classes[index]

        if res[index] < 0.5:
            return jsonify({'response': "Sorry, I am not sure about the answer."})

        for intent in intents['intents']:
            if intent['tag'] == tag:
                response = np.random.choice(intent['responses'])
                return jsonify({'response': response})

        return jsonify({'response': "Sorry, I couldn't find an answer."})
    except Exception as e:
        return jsonify({'response': f"An error occurred: {str(e)}"})
    
@app.route('/video')
def video():
    return render_template('vidio_islam.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/perpus')
def perpus():
    return render_template('perpus.html')

# Endpoint untuk mendapatkan semua thread
@app.route('/api/threads', methods=['GET'])
def get_threads():
    try:
        cur = mysql.connection.cursor(DictCursor)
        cur.execute("""
            SELECT 
                t.id AS thread_id, 
                t.title, 
                t.content, 
                t.created_at, 
                u.username AS author_username 
            FROM 
                threads t
            JOIN 
                users_apk u ON t.author_id = u.id
            ORDER BY 
                t.created_at DESC
        """)
        threads = cur.fetchall()
        cur.close()
        return jsonify({'status': 'success', 'threads': threads}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Endpoint untuk membuat thread baru
@app.route('/api/threads', methods=['POST'])
def create_thread():
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        author_id = data.get('author_id')  # ID pengguna dari users_apk

        if not title or not content or not author_id:
            return jsonify({'status': 'error', 'message': 'All fields are required'}), 400

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO threads (title, content, author_id) 
            VALUES (%s, %s, %s)
        """, (title, content, author_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'status': 'success', 'message': 'Thread created successfully'}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Endpoint untuk mendapatkan semua komentar dari thread tertentu
@app.route('/api/threads/<int:thread_id>/comments', methods=['GET'])
def get_comments(thread_id):
    try:
        cur = mysql.connection.cursor(DictCursor)
        cur.execute("""
            SELECT 
                c.id AS comment_id, 
                c.content, 
                c.created_at, 
                u.username AS author_username, 
                c.parent_comment_id 
            FROM 
                comments c
            JOIN 
                users_apk u ON c.author_id = u.id
            WHERE 
                c.thread_id = %s
            ORDER BY 
                c.created_at ASC
        """, (thread_id,))
        comments = cur.fetchall()
        cur.close()
        return jsonify({'status': 'success', 'comments': comments}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Endpoint untuk menambahkan komentar pada thread tertentu
@app.route('/api/threads/<int:thread_id>/comments', methods=['POST'])
def add_comment(thread_id):
    try:
        data = request.get_json()
        content = data.get('content')
        author_id = data.get('author_id')  # ID pengguna dari users_apk
        parent_comment_id = data.get('parent_comment_id', None)  # Optional, untuk nested comment

        if not content or not author_id:
            return jsonify({'status': 'error', 'message': 'Content and author_id are required'}), 400

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO comments (thread_id, content, author_id, parent_comment_id) 
            VALUES (%s, %s, %s, %s)
        """, (thread_id, content, author_id, parent_comment_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'status': 'success', 'message': 'Comment added successfully'}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/threads/<int:thread_id>', methods=['PUT'])
def edit_thread(thread_id):
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return jsonify({'status': 'error', 'message': 'Title and content are required'}), 400

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE threads 
            SET title = %s, content = %s 
            WHERE id = %s
        """, (title, content, thread_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'status': 'success', 'message': 'Thread updated successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/threads/<int:thread_id>', methods=['DELETE'])
def delete_thread(thread_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM threads WHERE id = %s", (thread_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'status': 'success', 'message': 'Thread deleted successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/comments/<int:comment_id>', methods=['PUT'])
def edit_comment(comment_id):
    try:
        data = request.get_json()
        content = data.get('content')

        if not content:
            return jsonify({'status': 'error', 'message': 'Content is required'}), 400

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE comments 
            SET content = %s 
            WHERE id = %s
        """, (content, comment_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'status': 'success', 'message': 'Comment updated successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'status': 'success', 'message': 'Comment deleted successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
