from app import mysql

class UserModel:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    @staticmethod
    def get_user_by_username(username):
        """
        Mengambil user berdasarkan username.
        """
        cursor = mysql.connection.cursor()
        query = "SELECT id, username, password, role FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        return user
