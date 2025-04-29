import psycopg2
import time
from flask import Flask
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app, version='1.0', title='Postgres API', description='A simple API to connect to Postgres', doc='/swagger/')

ns = api.namespace('students', description='Students operations')

def get_connection():
    conn = psycopg2.connect(
        host='db',
        port=5432,
        user='postgres',
        password='postgres',
        dbname='postgres'
    )
    return conn

@ns.route('/')
class AlunoList(Resource):
    def get(self):
        time.sleep(5)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );
        """)
        conn.commit()
        cursor.execute("INSERT INTO students (name) VALUES ('John Doe'),('Jane Doe'),('Doe John')")
        conn.commit()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        conn.close()
        return {"students": [{"id": student[0], "name": student[1]} for student in students]}