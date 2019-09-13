import mysql.connector
from mysql.connector import Error
import json
import random

conn = None 
def connect():
    global conn
    try:
        conn = mysql.connector.connect(host='localhost',database='YOUR_DB',user='YOUR_USER', password='YOUR_PASS')
        if conn.is_connected():
            cursor = conn.cursor()
            print("Connected to database!")
            return True
    except Error as e :
        print ("Fail to connect ", e)
        conn = None
        return False


def getUser(name, password):
    global conn
    if conn is not None:
        if conn.is_connected():
            statement = "select * from users;"
            cursor = conn.cursor()
            cursor.execute(statement)
            user = parse_single_response_as_json (cursor.fetchall(), cursor.description)
            return user

def getUserById(id):
    global conn
    if conn is not None:
        if conn.is_connected():
            statement = "select * from users where id = %s;"
            values = (id,)
            cursor = conn.cursor()
            cursor.execute(statement, values)
            user = parse_response_as_array_json_as_string (cursor.fetchall(), cursor.description)
            return user[0]


def login(name, password):
    global conn
    if conn is not None:
        if conn.is_connected():
            user = getUser(name, password)
            if user is not None:
                return user
            return None
        return None    

def getCategories():
    global conn
    if conn is not None:
        if conn.is_connected():
            statement = "select * from categories;"
            cursor = conn.cursor()
            cursor.execute(statement)
            categories = parse_response_as_array_json (cursor.fetchall(), cursor.description)
            return categories

def getCourseById(id):
    global conn
    if conn is not None:
        if conn.is_connected():
            statement = "select * from courses where id = %s;"
            values = (id,)
            cursor = conn.cursor()
            cursor.execute(statement, values)
            course = apply_courses_changes (cursor.fetchall(), cursor.description)
            return json.dumps(course[0])

def getCategoryById(id):
    global conn
    if conn is not None:
        if conn.is_connected():
            statement = "select * from categories where id = %s;"
            values = (id,)
            cursor = conn.cursor()
            cursor.execute(statement, values)
            category = parse_response_as_array_json_as_string (cursor.fetchall(), cursor.description)
            return category[0]

def getSessionsById(id):
    global conn
    if conn is not None:
        if conn.is_connected():
            statement = "select * from course_session where course_id = %s;"
            values = (id,)
            cursor = conn.cursor()
            cursor.execute(statement, values)
            category = parse_response_as_array_json_as_string (cursor.fetchall(), cursor.description)
            return category

def getCourseByCategoryId(id):
    global conn
    if conn is not None:
        if conn.is_connected():
            statement = "select * from courses where category_id = %s;"
            values = (id,)
            cursor = conn.cursor()
            cursor.execute(statement, values)
            courses = apply_category_courses_changes (cursor.fetchall(), cursor.description)
            return courses
        return None
    return None


def getCourseByHomeType(type):
    global conn
    if conn is not None:
        if conn.is_connected():
            statement = "select * from courses where home_category_type = %s;"
            values = (type,)
            cursor = conn.cursor()
            cursor.execute(statement, values)
            course = apply_courses_changes (cursor.fetchall(), cursor.description)
            return course

def getCourseByHomeTypeForUser(type):
    global conn
    if conn is not None:
        if conn.is_connected():
            statement = "select * from courses where home_category_type = %s;"
            values = (type,)
            cursor = conn.cursor()
            cursor.execute(statement, values)
            course = apply_courses_user_changes (cursor.fetchall(), cursor.description)
            return course

def getCourses():
    next_courses = getCourseByHomeType(0)
    in_progress_courses = getCourseByHomeType(1)
    recommended_courses = getCourseByHomeType(2)
    new_courses = getCourseByHomeType(3)
    home = {
        "next_courses" : next_courses,
        "in_progress_courses" : in_progress_courses,
        "recommended_courses" : recommended_courses,
        "new_courses" : new_courses 
         }
    return json.dumps(home)


def getMyLibrary():
    inclass = getCourseByHomeType(0)
    online = getCourseByHomeType(1)
    wishlist = getCourseByHomeType(2)

    library = {
        "inclass" : inclass,
        "online" : online,
        "wishlist" : wishlist        
         }
    return json.dumps(library)

def getUserData(user_id):
    user = getUserById(user_id)
    in_progress_courses = getCourseByHomeTypeForUser(1)
    recommended_courses = getCourseByHomeTypeForUser(2)

    data = {
        "user" : user,
        "in_progress_courses" : in_progress_courses,
        "completed_courses" : recommended_courses
    }
    return json.dumps(data)

#-------- utils ------#
def append_random_trainer():
    course1 = {
        "id": 0,
        "name": "Peter Anderson",
        "type": "TRAINER",
        "avatar_url": "https://icons-for-free.com/download-icon-game+go+play+pokemon+trainer+icon-1320186970555700448_512.png",
        "job_title": "Android Developer",
        "rating": 4.5
  }

    course2 =  {
        "id": 1,
        "name": "James Kolt",
        "type": "TRAINER",
        "avatar_url": "https://banner2.cleanpng.com/20180831/gbv/kisspng-personal-trainer-physical-fitness-exercise-fitness-cs-foundation-coaching-institute-study-guide-cours-5b892eab1f3241.3634097915357170351278.jpg",
        "job_title": "Python Developer ",
        "rating": 4.8
    }

    rand = random.randint(0, 1) 
    if rand == 1:
        return course1
    return course2

def loop_hours_data():
    for i in range(5 , 23) :
        init_hours_data(str(i), str(random.randrange(15)+5))

def init_hours_data(hour, count):
    global conn
    if conn is not None:
        if conn.is_connected():
            statement = "insert into city_hours(c_hour, c_count) values (%s, %s);"
            values = (hour, count)
            cursor = conn.cursor()
            cursor.execute(statement, values)
            conn.commit()
            cursor.close()


def parse_response_as_array_json(query, description):
    row_headers = [x[0] for x in description]
    json_array = []

    for item in query:
        json_array.append(dict(zip(row_headers,item)))

    return json.dumps(json_array)


def parse_response_as_array_json_as_string(query, description):
    row_headers = [x[0] for x in description]
    json_array = []

    for item in query:
        json_array.append(dict(zip(row_headers,item)))

    return json_array
    

def apply_courses_changes(query, description):
    row_headers = [x[0] for x in description]
    json_array = []

    for item in query:
        d = dict(zip(row_headers,item))
        category_id = d['category_id']
        d['trainer'] = append_random_trainer()
        d['category'] = getCategoryById(category_id)
        json_array.append(d)
    return json_array


def apply_courses_user_changes(query, description):
    row_headers = [x[0] for x in description]
    json_array = []

    for item in query:
        d = dict(zip(row_headers,item))
        category_id = d['category_id']
        coure_id = d['id']
        d['trainer'] = append_random_trainer()
        d['category'] = getCategoryById(category_id)
        d['sessions'] =  getSessionsById(coure_id)
        json_array.append(d) 
    return json_array

def apply_category_courses_changes(query, description):
    row_headers = [x[0] for x in description]
    json_array = []

    for item in query:
        d = dict(zip(row_headers,item))
        category_id = d['category_id']
        d['trainer'] = append_random_trainer()
        d['category'] = getCategoryById(category_id)
        json_array.append(d)
    return json.dumps(json_array)

def parse_single_response_as_json(query, description):
    row_headers = [x[0] for x in description]
    item = dict(zip(row_headers,query))
    return json.dumps(item)


def parse_single_response_as_string(query, description):
    row_headers = [x[0] for x in description]
    item = dict(zip(row_headers,query))
    return item


print(getCategoryById(0))