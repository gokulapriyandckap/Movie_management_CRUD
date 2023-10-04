from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
import re
import datetime
import json
import hashlib
from bson import ObjectId

app = Flask(__name__)


client = MongoClient("mongodb://localhost:27017")
db = client.Movie_management_system
users = db.users
movies = db.Movies
vote = db.likes

jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = 'gokul@213'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=1)

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = hashlib.sha256(password.encode("utf-8")).hexdigest()

    def save_to_db(self):
        users.insert_one({"email": self.email, "password": self.password})

class Movie:
    def __init__(self, name, duration, director_name, user_id):
        self.name = name
        self.duration = duration
        self.director_name = director_name
        self.user_id = user_id

    def save_to_db(self):
        movies.insert_one({
            "name": self.name,
            "duration": self.duration,
            "director_name": self.director_name,
            "user_id": self.user_id
        })
        return 'movie Created Successfully'

class Vote:
    def __init__(self, movie_name, user_id, vote):
        self.movie_name = movie_name
        self.user_id = user_id
        self.vote = vote

    def save_to_db(self):
        likes.insert_one({
            "movie_name": self.movie_name,
            "user_id": self.user_id,
            "vote": self.vote
        })

# Your routes can be refactored to use these classes

@app.route("/", methods=["GET"])
def get_data():
    return 'Welcome To the Movie Management System'

@app.route("/register", methods=["POST"])
def create_user():
    email = request.json['email']
    password = request.json['password']

    # Validation logic...

    user = User(email, password) # instance
    user.save_to_db()
    return "User Created Successfully!"

@app.route('/login', methods=["POST"])
def login():
    email = request.json['email']
    password = request.json['password']

    # Authentication logic...
    user = users.find_one({"email": email})
    if user:
        user_id = user["_id"]
        return {"token": create_access_token(identity=str(user_id)), "status": "Success", "result": "Logged in Successfully"}
    else:
        return 'Credintials not found'

    # Token generation logic...


@app.route('/createmovie', methods=['POST'])
@jwt_required()
def createMovie():
    movieName = request.json['name']
    Duration = request.json['Duration']
    DirectorName = request.json['DirectorName']
    user_id = get_jwt_identity()

    movie = Movie(movieName,Duration,DirectorName,user_id)
    movie.save_to_db()
    return 'Movie Created Successfully!'

if __name__ == "__main__":
    app.run(debug=True)