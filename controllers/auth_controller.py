# app/controllers/auth_controller.py
import os
from flask import Blueprint, current_app, jsonify, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models.user_model import UserModel
from extensions import mysql
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup

auth_bp = Blueprint('auth', __name__, url_prefix='/admin')

# Set direktori upload gambar
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = UserModel.get_user_by_username(username)

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['role'] = user[3]  # Simpan role ke session
            flash("Login berhasil!", "success")
            
            if user[3] == 'super_admin':
                return redirect(url_for('auth.super_admin_dashboard'))
            else:
                return redirect(url_for('auth.dashboard'))
        else:
            flash("Username atau password salah.", "error")

    return render_template('login.html')


# app/controllers/auth_controller.py
@auth_bp.route('/dashboard')
def dashboard():
    cursor = mysql.connection.cursor()
    # Mengambil jumlah user
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    # Mengambil jumlah artikel
    cursor.execute("SELECT COUNT(*) FROM articles")
    article_count = cursor.fetchone()[0]

    # Menghitung sentimen
    cursor.execute("SELECT COUNT(*) FROM hasil_model WHERE label = 'Positif'")
    positive_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM hasil_model WHERE label = 'Negatif'")
    negative_count = cursor.fetchone()[0]
    
    cursor.close()
    
    return render_template(
        'dashboard.html',
        user_count=user_count,
        article_count=article_count,
        positive_count=positive_count,
        negative_count=negative_count
    )


# Daftar Users
@auth_bp.route('/users')
def users():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return render_template('users.html', users=users)

# Tambah User
# app/controllers/auth_controller.py
from werkzeug.security import generate_password_hash, check_password_hash

@auth_bp.route('/super_admin_dashboard')
def super_admin_dashboard():
    # Pastikan hanya super_admin yang bisa mengakses
    if session.get('role') != 'super_admin':
        flash("Anda tidak memiliki izin untuk mengakses halaman ini.", "error")
        return redirect(url_for('auth.dashboard'))

    # Misalnya, ambil data yang relevan untuk super_admin
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) AS total_articles FROM articles")
    total_articles = cursor.fetchone()[0]

    cursor.close()

    return render_template(
        'super_admin_dashboard.html',
        total_users=total_users,
        total_articles=total_articles
    )

# Route to add user (already hashing the password)
@auth_bp.route('/users/add', methods=['GET', 'POST'])
def add_user():
    # Pastikan hanya super_admin yang dapat mengakses
    if session.get('role') != 'super_admin':
        flash("Anda tidak memiliki izin untuk menambah pengguna.", "error")
        return redirect(url_for('auth.users'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']  # Ambil role dari form

        # Validasi role agar hanya 'admin' atau 'super_admin'
        if role not in ['admin', 'super_admin']:
            flash("Role tidak valid.", "error")
            return redirect(url_for('auth.add_user'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                       (username, hashed_password, role))
        mysql.connection.commit()
        cursor.close()

        flash('User berhasil ditambahkan!', 'success')
        return redirect(url_for('auth.users'))

    return render_template('add_user.html')

# Route to edit user
@auth_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    cursor = mysql.connection.cursor()
    
    # Fetch data user yang akan diedit
    cursor.execute("SELECT id, username, role FROM users WHERE id=%s", (user_id,))
    target_user = cursor.fetchone()
    
    # Pastikan user yang login tidak bisa mengedit super_admin jika bukan super_admin
    if session['role'] != 'super_admin' and target_user[2] == 'super_admin':
        flash("Anda tidak diizinkan untuk mengedit pengguna ini.", "error")
        return redirect(url_for('auth.users'))
    
    # Proses edit user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if password:  # Jika ada password baru
            hashed_password = generate_password_hash(password)
            cursor.execute(
                "UPDATE users SET username=%s, password=%s WHERE id=%s", 
                (username, hashed_password, user_id)
            )
        else:  # Jika tidak ada password baru
            cursor.execute(
                "UPDATE users SET username=%s WHERE id=%s", 
                (username, user_id)
            )
        
        mysql.connection.commit()
        cursor.close()
        
        flash('User berhasil diperbarui!', 'success')
        return redirect(url_for('auth.users'))

    cursor.close()
    return render_template('edit_user.html', user=target_user)


# Hapus User
@auth_bp.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    cursor = mysql.connection.cursor()

    # Ambil data user yang akan dihapus
    cursor.execute("SELECT id, role FROM users WHERE id=%s", (user_id,))
    target_user = cursor.fetchone()

    if not target_user:
        flash("Pengguna tidak ditemukan.", "error")
        return redirect(url_for('auth.users'))

    # Validasi hak akses
    if session['role'] != 'super_admin':
        if target_user[1] == 'super_admin' or (session['role'] == 'admin' and target_user[1] == 'admin'):
            flash("Anda tidak diizinkan untuk menghapus pengguna ini.", "error")
            return redirect(url_for('auth.users'))

    # Proses hapus user
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    mysql.connection.commit()
    cursor.close()

    flash('User berhasil dihapus!', 'success')
    return redirect(url_for('auth.users'))

# Tambah Artikel

@auth_bp.route('/artikel')
def artikel():
    search = request.args.get('search', '')
    sort = request.args.get('sort', '')

    query = "SELECT * FROM articles"
    filters = []

    if search:
        filters.append(f"title LIKE '%{search}%'")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    if sort == 'judul':
        query += " ORDER BY title"

    cursor = mysql.connection.cursor()
    cursor.execute(query)
    articles = cursor.fetchall()
    cursor.close()

    return render_template('artikel.html', articles=articles)

# Route untuk menambah artikel


@auth_bp.route('/artikel/add', methods=['GET', 'POST'])
def add_artikel():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        created_at = request.form['created_at']  # Ambil tanggal pembuatan dari form

        # Bersihkan konten HTML
        soup = BeautifulSoup(content, "html.parser")
        cleaned_content = soup.get_text()

        # Proses file gambar jika ada
        image_filename = None
        if 'image' in request.files and request.files['image'].filename != '':
            image = request.files['image']
            if image and allowed_file(image.filename):
                image_filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))

        # Simpan data artikel ke database
        cursor = mysql.connection.cursor()
        cursor.execute(
            """
            INSERT INTO articles (title, content, image, created_at) 
            VALUES (%s, %s, %s, %s)
            """,
            (title, cleaned_content, image_filename, created_at)
        )
        mysql.connection.commit()
        cursor.close()

        flash('Artikel berhasil ditambahkan!', 'success')
        return redirect(url_for('auth.artikel'))

    return render_template('add_artikel.html')

# Edit Artikel
@auth_bp.route('/artikel/edit/<int:artikel_id>', methods=['GET', 'POST'])
def edit_artikel(artikel_id):
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        created_at = request.form['created_at']  # Ambil tanggal dari form

        # Bersihkan konten HTML
        soup = BeautifulSoup(content, "html.parser")
        cleaned_content = soup.get_text()

        # Proses file gambar jika ada
        image_filename = None
        if 'image' in request.files and request.files['image'].filename != '':
            image = request.files['image']
            if image and allowed_file(image.filename):
                image_filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))

        if not image_filename:
            cursor.execute("SELECT image FROM articles WHERE id=%s", (artikel_id,))
            image_filename = cursor.fetchone()[0]

        # Update artikel di database termasuk tanggal
        cursor.execute(
            """
            UPDATE articles 
            SET title=%s, content=%s, image=%s, created_at=%s 
            WHERE id=%s
            """,
            (title, cleaned_content, image_filename, created_at, artikel_id)
        )
        mysql.connection.commit()
        cursor.close()

        flash('Artikel berhasil diperbarui!', 'success')
        return redirect(url_for('auth.artikel'))

    # Ambil data artikel dari database
    cursor.execute("SELECT id, title, content, image, created_at FROM articles WHERE id=%s", (artikel_id,))
    artikel = cursor.fetchone()
    cursor.close()

    return render_template('edit_artikel.html', artikel=artikel)

# Daftar Artikel
# Hapus Artikel
@auth_bp.route('/artikel/delete/<int:artikel_id>', methods=['POST'])
def delete_artikel(artikel_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM articles WHERE id=%s", (artikel_id,))
    mysql.connection.commit()
    cursor.close()
    
    flash('Artikel berhasil dihapus!', 'success')
    return redirect(url_for('auth.artikel'))

# app/controllers/auth_controller.py
@auth_bp.route('/upload_image', methods=['POST'])
def upload_image():
    if 'upload' in request.files:
        image = request.files['upload']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            url = url_for('static', filename='uploads/' + filename)
            return jsonify({"uploaded": True, "url": url})
    return jsonify({"uploaded": False, "error": {"message": "Gagal mengunggah gambar"}})




@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Anda telah logout.", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    # Ambil data JSON dari body request
    data = request.get_json()
    
    if not data or not all(k in data for k in ('username', 'password')):
        return jsonify({"error": "Username dan password harus diisi"}), 400

    username = data['username']
    password = data['password']
    
    # Cek user di database
    user = UserModel.get_user_by_username(username)

    if user and check_password_hash(user[2], password): 
        
        user_data = {
            "id": user[0],
            "username": user[1],
            "role": user[3]
        }
        return jsonify({"message": "Login berhasil", "user": user_data}), 200
    else:
        return jsonify({"error": "Username atau password salah"}), 401
