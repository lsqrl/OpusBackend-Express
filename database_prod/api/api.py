from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure the PostgreSQL database connection
user = os.getenv("POSTGRES_USERNAME")
password = os.getenv("POSTGRES_PASSWORD")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'account'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

# Route to fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    return jsonify(users_list)

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)
