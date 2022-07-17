from flask import Flask, url_for, render_template, Blueprint
from werkzeug.debug import console
from werkzeug.utils import redirect
from datetime import timedelta
from flask import request, session, jsonify
import mysql.connector
import requests


app=Flask(__name__)
app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)

#------init global variable
is_massage=False
massage='init'
# about blueprint definition
assignment_4 = Blueprint('assignment_4', __name__, static_folder='static', static_url_path='/assignment_4',
                  template_folder='templates')


# ------------------------------------------------- #
# ------------- DATABASE CONNECTION --------------- #
# ------------------------------------------------- #
def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='schema_users')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)
    #

    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value

# ------------------------------------------------- #
# ------------------------------------------------- #


# ------------------------------------------------- #
# ------------------- SELECT ---------------------- #
# ------------------------------------------------- #
@assignment_4.route('/assignment_4')
def users(is_massage=is_massage):
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    if (is_massage == True):
        is_massage = False
        return render_template('assignment_4.html', users=users_list,massage=massage)
    return render_template('assignment_4.html', users=users_list)



# ------------------------------------------------- #
# ------------------- assignment_4/users ---------- #
# ------------------------------------------------- #
@assignment_4.route('/assignment_4/users')
def users_json(user_restapi_id):
    if (user_restapi_id == -1):
        query = 'select * from users'
    else:
        query = "SELECT * FROM users WHERE id=%s;" % user_restapi_id
    users_list = interact_db(query, query_type='fetch')
    return_list = []
    if len(users_list) == 0:
        user_dict ={
            'error: user not found'
        }
        return_list.append(user_dict)
    else:
        for user in users_list:
            user_dict = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'id': user.id
                }
            return_list.append(user_dict)
    return jsonify(return_list)

# ------------------------------------------------- #
# ------------------------------------------------- #


# ------------------------------------------------- #
# -------------------- INSERT --------------------- #
# ------------------------------------------------- #
@assignment_4.route('/insert_user', methods=['POST'])
def insert_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    query = "INSERT INTO users(first_name,last_name, email, password) VALUES ('%s', '%s', '%s','%s');" %(first_name, last_name, email, password)
    interact_db(query=query, query_type='commit')
    is_massage = True
    message='You were successfully insert user'
    return redirect('/assignment_4')


# ------------------------------------------------- #
# ------------------------------------------------- #


# ------------------------------------------------- #
# -------------------- DELETE --------------------- #
# ------------------------------------------------- #
@assignment_4.route('/delete_user', methods=['POST'])
def delete_user_func():
    email = request.form['email']
    query = "DELETE FROM users WHERE email='%s';" % email
    # print(query)
    interact_db(query, query_type='commit')
    is_massage = True
    massage = 'You were successfully delete user'
    return redirect('/assignment_4')


# ------------------------------------------------- #
# ------------------------------------------------- #

# ------------------------------------------------- #
# -------------------- update --------------------- #
# ------------------------------------------------- #
@assignment_4.route('/update_user', methods=['POST'])
def update_user():
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']

    query = "update users set first_name='%s', last_name='%s', password='%s' " % (first_name,last_name,password)\
            +"WHERE email='%s';" % email
    interact_db(query, query_type='commit')
    is_massage = True
    massage = 'You were successfully update user'
    return redirect('/assignment_4')


# ------------------------------------------------- #
# ------------------------------------------------- #

# ------------------------------------------------- #
# -------------------- outer source --------------------- #
# ------------------------------------------------- #

@assignment_4.route('/assignment4/outer_source', methods=["POST", "GET"])
def outer_source():
    user_json = None

    if 'user_id' in request.values:
        user_id = request.form['user_id']
        res = requests.get(f'https://reqres.in/api/users/{user_id}')
        if res:
            user_json =  res.json()

    return render_template('outer_source.html', json_dict=user_json)


# ------------------------------------------------- #
# ------------------------------------------------- #

# ------------------------------------------------- #
# -------------------- restapi_users --------------------- #
# ------------------------------------------------- #




@assignment_4.route('/assignment4/restapi_users/<int:USER_ID>', defaults={'USER_ID': -1})
def get_user(USER_ID):
    return_dict=  users_json(USER_ID)

    return jsonify(return_dict)






