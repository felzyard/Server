from flask import Flask, url_for, render_template
from werkzeug.utils import redirect
from datetime import timedelta
from flask import request, session, jsonify

app=Flask(__name__)
app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)


@app.route('/')
def start():
    return redirect('home')

@app.route('/home')
def home():
    email_session = None
    first_nameR = None
    if 'email' in session:
        email_session= session['email']
        first_nameR = session['first_name']
    return render_template('homePage22.html',email_session=email_session, first_nameR=first_nameR)

@app.route('/contact')
def contact():
    email_session = None
    first_nameR = None
    if 'email' in session:
        email_session = session['email']
        first_nameR = session['first_name']
    return render_template('contactUs22.html',email_session=email_session, first_nameR=first_nameR)

@app.route('/assignment3_1')
def assignment31():
    email_session = None
    first_nameR = None

    user_name="arseny"
    introduction= "lets show you what <strong> <em> I like </em> </strong>"
    singers=['Ed Sheeran','Imagine Dragons','Billie Eillish', 'Eliad Nachum']
    if 'email' in session:
        email_session= session['email']
        first_nameR = session['first_name']
    return render_template('assignment3_1.html',user_name=user_name,introduction=introduction,singers=singers,email_session=email_session, first_nameR=first_nameR )



users = {   'user1': {'first_name':'Rachel', 'last_name':'Green', 'email':'rachelgreen@gmail.com','password':'456'},
            'user2': {'first_name':'Monica', 'last_name':'Geller', 'email':'monicageller@gmail.com','password':'789'},
            'user3': {'first_name':'Joey', 'last_name':'Tribbiani', 'email':'joeytribbiani@gmail.com','password':'1011'},
            'user4': {'first_name':'Chandler', 'last_name':'Bing', 'email':'chandlerbing@gmail.com','password':'1213'},
            'user5': {'first_name':'Phoebe', 'last_name':'Buffay', 'email':'phoebebuffay@gmail.com','password':'1415'}
        }
@app.route('/assignment3_2', methods=['GET','POST'])
def assignment32():
    email_session= None
    first_nameR = None

    if 'email' in session:
        email_session = session['email']
        first_nameR = session['first_name']
# handle with post method
    if request.method=="POST":
        email=request.form['email'].lower()
        password_check = request.form['password']
        if email in [user["email"] for user in users.values()]:
                session['email']= email
                for k, v in users.items():
                    if email == v["email"]:
                            session['first_name'] = v["first_name"]
                            last_name = v["last_name"]
                            password = v["password"]

                if password_check == password:
                    return render_template('assignment3_2.html', first_nameR=session['first_name'] ,last_nameR=last_name, passwordR=password, email_session=session['email'])

                else:
                    return render_template('assignment3_2.html',incorect_mass='wrong password')
        else:
            return render_template('assignment3_2.html', wrong_email='wrong email')
# handle with get method
    else:
        if 'email' in session:
            email_session=session['email']
            first_nameR= session['first_name']
# if we get input from search form
        if 'first_name' in request.args or 'last_name' in request.args or 'email' in request.args:
            first_name = request.args['first_name'].capitalize()
            last_name = request.args['last_name'].capitalize()
            email = request.args['email'].lower()
#If user presses submit button in the blank search form
            if first_name == '' and last_name == '' and email == '':
                return render_template('assignment3_2.html',
                               users=users, email_session=email_session, first_nameR=first_nameR )
# If user presses submit button with value in at least one of the inputes
            elif first_name != '' or last_name != '' or email != '':
                #value at first_name inpute
                if first_name in [user["first_name"] for user in users.values()]:
                    for k,v in users.items():
                        if first_name==v["first_name"]:
                            last_name=v["last_name"]
                            email=v["email"]

                    return render_template('assignment3_2.html',
                            first_name=first_name,last_name=last_name,email=email, email_session=email_session, first_nameR=first_nameR)
                # value at last_name inpute
                elif last_name in [user["last_name"] for user in users.values()]:
                    for k,v in users.items():
                        if last_name==v["last_name"]:
                            first_name=v["first_name"]
                            email=v["email"]

                    return render_template('assignment3_2.html',
                               first_name=first_name,last_name=last_name,email=email, email_session=email_session, first_nameR=first_nameR )
                # value at email inpute
                elif email in [user["email"] for user in users.values()]:
                    for k,v in users.items():
                        if email==v["email"]:
                            first_name=v["first_name"]
                            last_name=v["last_name"]

                    return render_template('assignment3_2.html',
                               first_name=first_name,last_name=last_name,email=email, email_session=email_session, first_nameR=first_nameR)
                # value that not match the dictionary (wrong value)
                else:
                    return render_template('assignment3_2.html',
                                      message= 'user not found', email_session=email_session, first_nameR=first_nameR)
        # if the user dont do anything
        else:
            return render_template('assignment3_2.html',email_session=email_session, first_nameR=first_nameR)


@app.route('/log_out')
def log_out():
    session.clear()
    return redirect(url_for('assignment32'))


if __name__=='__main__':
    app.run(debug=True)
