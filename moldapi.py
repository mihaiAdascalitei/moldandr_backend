from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import DataBaseConnector as db

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db.connect()

@app.route('/get-categories', methods=['GET']) 
def get_categories():
    categories = db.getCategories()
    if categories is not None:
        return categories, 200
    return "No categories found", 404


@app.route('/login', methods=['POST'])
def login():
	data = request.get_json()
	name = data['name']
	password = data['password']
	user = db.login(name, password)
	if not user:
		return "No user found", 404
	return user


@app.route('/register', methods=['POST'])
def register():
	data = request.get_json()
	name = data['name']
	password = data['password']
	user = db.register(name, password)
	if not user:
		return "Registration failed", 401
	return user
	
@app.route('/get-home', methods=['GET'])
def get_courses_home():
	return db.getCourses(), 200

@app.route('/get-course-details', methods=['GET'])
def get_courses_by_id():
	param_id = request.args.get('course_id')
	course = db.getCourseById(param_id)
	if course :
		return course, 200
	return "No course found", 404


@app.route('/get-my-library', methods=['GET'])
def get_courses_library():
	return db.getMyLibrary(), 200

@app.route('/get-user-details', methods=['GET'])
def get_user():
	param_id = request.args.get('user_id')
	user = db.getUserData(param_id)
	if not isJsonObjEmpty(user):
		return user, 200
	return "User not found", 404

@app.route('/get-courses-by-category', methods=['GET'])
def get_courses_by_category():
	param_id = request.args.get('category_id')
	courses = db.getCourseByCategoryId(param_id)
	if not isJsonArrayEmpty(courses) or not courses:
		return courses, 200
	return "Courses by category not found", 404

def isJsonObjEmpty(obj):
	return obj == {}

def isJsonArrayEmpty(data):
	return data == []

if __name__ == '__main__':
    app.run(host="YOUR_API",port="YOUR_PORT") 


