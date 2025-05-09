import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()
        # Comment out the create_table call since the table already exists
        # self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS unknown_faces (
                id INT AUTO_INCREMENT PRIMARY KEY,
                image_path TEXT NOT NULL,
                detected_at DATETIME NOT NULL
            )
        ''')
        self.conn.commit()

    def log_unknown_face(self, file_path):
        self.cursor.execute('INSERT INTO unknown_faces (image_path, detected_at) VALUES (%s, NOW())', 
                            (file_path,))
        self.conn.commit()

    def log_weapon(self, incident_name, file_path):
        self.cursor.execute('INSERT INTO incident (incident_name, occurrence_datetime, image_file_location) VALUES (%s, NOW(), %s)',
                    (incident_name, file_path))
        self.conn.commit()

    def close(self):
        self.conn.close()
