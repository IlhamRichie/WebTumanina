from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from MySQLdb.cursors import DictCursor
from extensions import mysql

diskusi_bp = Blueprint('diskusi', __name__, url_prefix='/discussions')

# Get all discussions or a specific discussion by ID
@diskusi_bp.route('/', methods=['GET'])
def get_discussions():
    try:
        discussion_id = request.args.get('id', None)
        cur = mysql.connection.cursor(DictCursor)

        if discussion_id:
            cur.execute("""
                SELECT d.*, u.username AS created_by, ua.username AS user_apk
                FROM discussions d
                LEFT JOIN users u ON d.user_id = u.id
                LEFT JOIN users_apk ua ON d.user_apk_id = ua.id
                WHERE d.id = %s
            """, (discussion_id,))
            discussion = cur.fetchone()

            if not discussion:
                cur.close()
                return jsonify({"message": "Discussion not found."}), 404

            # Fetch comments for this discussion
            cur.execute("""
                SELECT dc.*, ua.username AS commenter
                FROM discussion_comments dc
                LEFT JOIN users_apk ua ON dc.user_apk_id = ua.id
                WHERE dc.discussion_id = %s
                ORDER BY dc.created_at ASC
            """, (discussion_id,))
            comments = cur.fetchall()

            cur.close()
            discussion['comments'] = comments
            return jsonify(discussion)

        cur.execute("""
            SELECT d.*, u.username AS created_by, ua.username AS user_apk
            FROM discussions d
            LEFT JOIN users u ON d.user_id = u.id
            LEFT JOIN users_apk ua ON d.user_apk_id = ua.id
            ORDER BY d.created_at DESC
        """)
        discussions = cur.fetchall()
        cur.close()
        return jsonify(discussions)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add a new discussion
@diskusi_bp.route('/', methods=['POST'])
def add_discussion():
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        user_id = data.get('user_id')
        user_apk_id = data.get('user_apk_id')

        if not title or not content or not user_id or not user_apk_id:
            return jsonify({"message": "Missing required fields."}), 400

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO discussions (title, content, user_id, user_apk_id)
            VALUES (%s, %s, %s, %s)
        """, (title, content, user_id, user_apk_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Discussion added successfully."}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add a comment to a discussion
@diskusi_bp.route('/<int:discussion_id>/comments', methods=['POST'])
def add_comment(discussion_id):
    try:
        data = request.get_json()
        comment = data.get('comment')
        user_apk_id = data.get('user_apk_id')

        if not comment or not user_apk_id:
            return jsonify({"message": "Missing required fields."}), 400

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO discussion_comments (discussion_id, comment, user_apk_id)
            VALUES (%s, %s, %s)
        """, (discussion_id, comment, user_apk_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Comment added successfully."}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Update a comment
@diskusi_bp.route('/<int:discussion_id>/comments/<int:comment_id>', methods=['PUT'])
def update_comment(discussion_id, comment_id):
    try:
        data = request.get_json()
        comment = data.get('comment')

        if not comment:
            return jsonify({"message": "Comment is required."}), 400

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE discussion_comments
            SET comment = %s
            WHERE id = %s AND discussion_id = %s
        """, (comment, comment_id, discussion_id))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Comment updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update a discussion
@diskusi_bp.route('/<int:discussion_id>', methods=['PUT'])
def update_discussion(discussion_id):
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return jsonify({"message": "Missing required fields."}), 400

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE discussions
            SET title = %s, content = %s
            WHERE id = %s
        """, (title, content, discussion_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Discussion updated successfully."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a discussion
@diskusi_bp.route('/<int:discussion_id>', methods=['DELETE'])
def delete_discussion(discussion_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM discussions WHERE id = %s", (discussion_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Discussion deleted successfully."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Web route to render discussions page
@diskusi_bp.route('/manage', methods=['GET'])
def manage_discussions():
    try:
        cur = mysql.connection.cursor(DictCursor)
        # Ambil semua diskusi
        cur.execute("""
            SELECT 
                d.id, d.title, d.content, d.created_at, 
                u.username AS created_by, 
                ua.username AS user_apk_username
            FROM discussions d
            LEFT JOIN users u ON d.user_id = u.id
            LEFT JOIN users_apk ua ON d.user_apk_id = ua.id
            ORDER BY d.created_at DESC
        """)
        discussions = cur.fetchall()

        # Ambil komentar untuk setiap diskusi
        for discussion in discussions:
            cur.execute("""
                SELECT dc.comment, dc.created_at, ua.username AS commenter
                FROM discussion_comments dc
                LEFT JOIN users_apk ua ON dc.user_apk_id = ua.id
                WHERE dc.discussion_id = %s
                ORDER BY dc.created_at ASC
            """, (discussion['id'],))
            discussion['comments'] = cur.fetchall()

        cur.close()
        return render_template('discussions.html', discussions=discussions)
    except Exception as e:
        return str(e), 500

