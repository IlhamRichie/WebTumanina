from flask import Blueprint, render_template, request, jsonify, session
from app.models.indobert import SentimentAnalyzer
from app import mysql
from datetime import datetime

import logging

logging.basicConfig(level=logging.DEBUG)
# Initialize blueprint
sentiment_bp = Blueprint('sentiment', __name__, url_prefix='/sentimen')

# Paths to the model and vectorizer
model_path = 'app/model/FinalModelSVM.pkl'
vectorizer_path = 'app/model/reviews.pkl'

# Initialize SentimentAnalyzer
analyzer = SentimentAnalyzer(model_path, vectorizer_path)

@sentiment_bp.route('/')
def index():
    # Fetch reviews from the database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_review, nama, tanggal, review, label FROM hasil_model ORDER BY id_hasil_model DESC")
    results = cursor.fetchall()
    cursor.close()

    # Process results (termasuk id untuk keperluan penghapusan)
    reviews = [{"id": row[0], "name": row[1], "date": row[2].strftime('%Y-%m-%d'), "text": row[3], "sentiment": row[4]} for row in results]

    # Calculate sentiment counts for the chart
    positive_count = sum(1 for review in reviews if review['sentiment'] == 'Positif')
    negative_count = sum(1 for review in reviews if review['sentiment'] == 'Negatif')

    return render_template(
        'sentiments.html',
        reviews=reviews,
        positive_count=positive_count,
        negative_count=negative_count
    )


@sentiment_bp.route('/add_review', methods=['POST'])
def add_review():
    data = request.json
    review_text = data.get('text', '').strip()
    name = data.get('name', 'Anonymous').strip()
    date = datetime.now().strftime('%Y-%m-%d')  # Automatically add today's date

    if not review_text:
        return jsonify({"error": "Review text cannot be empty"}), 400

    # Predict sentiment using the analyzer
    predicted_class = analyzer.predict_sentiment(review_text)  # Only one value is returned
    sentiment = "Positif" if predicted_class == 1 else "Negatif"

    try:
        # Save review and sentiment to the database
        cursor = mysql.connection.cursor()
        # Insert into input_review table
        cursor.execute(
            "INSERT INTO input_review (nama, tanggal, review) VALUES (%s, %s, %s)",
            (name, date, review_text)
        )
        mysql.connection.commit()

        # Get the last inserted review ID
        review_id = cursor.lastrowid

        # Insert into hasil_model table
        cursor.execute(
            "INSERT INTO hasil_model (id_review, nama, tanggal, review, label) VALUES (%s, %s, %s, %s, %s)",
            (review_id, name, date, review_text, sentiment)
        )
        mysql.connection.commit()
        cursor.close()

        # Return JSON response
        return jsonify({"name": name, "date": date, "text": review_text, "sentiment": sentiment})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@sentiment_bp.route('/delete_review', methods=['POST'])
def delete_review():
    data = request.json
    review_id = data.get('id')

    if not review_id:
        return jsonify({"error": "Review ID is required"}), 400

    try:
        # Hapus review dari tabel hasil_model dan input_review
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM hasil_model WHERE id_review = %s", (review_id,))
        cursor.execute("DELETE FROM input_review WHERE id_review = %s", (review_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": "Review deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sentiment_bp.route('/filter_reviews', methods=['POST'])
def filter_reviews():
    data = request.get_json()
    search = data.get('search', '')
    filter_value = data.get('filter', '')

    cursor = mysql.connection.cursor()
    
    # Query untuk filter dan pencarian
    query = """
        SELECT id_hasil_model AS id, nama, tanggal, review, label 
        FROM hasil_model 
        WHERE 1=1
    """
    params = []
    
    if search:
        query += " AND review LIKE %s"
        params.append(f"%{search}%")
    
    if filter_value:
        query += " AND label = %s"
        params.append(filter_value)
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()

    # Format hasil untuk dikirim ke frontend
    reviews = [
        {
            'id': row[0],
            'name': row[1],
            'date': row[2].strftime('%Y-%m-%d'),
            'text': row[3],
            'sentiment': row[4]
        }
        for row in results
    ]

    return jsonify({'reviews': reviews})
