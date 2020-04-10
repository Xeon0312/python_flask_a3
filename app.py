from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from markupsafe import escape

app = Flask(__name__)
app.secret_key = b'xeon'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    if 'username' in session:
        sql = """
            SELECT *
            FROM users
            where username='{}'""".format(session['username'])
        results = db.engine.execute(text(sql))
        user = [{column: value for column, value in rowproxy.items()}
                for rowproxy in results][0]
        print(user["role"])
        return render_template('home.html', data={"username": session['username'], "role": user["role"]})
    else:
        return render_template('home.html', data={"msg": "You are not login"})


@app.route('/editmarks/<studentname>', methods=['GET', 'POST'])
def editMark(studentname):
    if 'username' in session:
        if request.method == 'POST':
            quiz1Mark = request.form['assignment1']
            quiz2Mark = request.form['assignment2']
            quiz3Mark = request.form['assignment3']
            midtermExamMark = request.form['midtermexam']
            finalExamMark = request.form['finalexam']
            lab = request.form['lab']
            # username = session['username']
            updateSQL = """UPDATE marks
				   SET assignment1 = '{}', assignment2 = '{}', assignment3 = '{}',midtermexam = '{}', finalexam = '{}', lab = '{}'
				   WHERE studentname = '{}'""".format(quiz1Mark, quiz2Mark, quiz3Mark, midtermExamMark, finalExamMark,
                                                      lab, studentname)
            db.engine.execute(text(updateSQL))
            return redirect(url_for('grades'))
        else:
            sql = """
            SELECT * FROM marks WHERE studentname = '{}'
            """.format(studentname)
            results = db.engine.execute(text(sql))
            student = [{column: value for column, value in rowproxy.items()}
                       for rowproxy in results][0]
            return render_template('editmarks.html', data={"username": session["username"], "student": student})
    else:
        redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.headers.get('User-Agent'))
    if request.method == 'POST':
        sql = """
			SELECT *
			FROM users
			"""
        results = db.engine.execute(text(sql))
        for result in results:
            if result['username'] == request.form['username']:
                if result['password'] == request.form['password']:
                    session['username'] = request.form['username']
                    sql1 = """
						SELECT *
						FROM marks
						where studentname='{}'""".format(request.form['username'])
                    results = db.engine.execute(text(sql1))
                    return redirect('/')
        return render_template('login.html', data={"msg": "Incorrect UserName/Password, please try again!"})
    elif 'username' in session:
        return redirect('/')
    else:
        return render_template('login.html', data={})


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if (request.form['password'] != request.form['password2']):
            return render_template('register.html', data={"msg": " Password dose't match! "})
        sql = """
			SELECT EXISTS(SELECT *
			FROM users WHERE username = '{}')
			""".format(request.form['username'])
        results = db.engine.execute(text(sql))
        # print(results.first())
        if (results.first()[0] == 1):
            return render_template('register.html', data={"msg": " Duplicate username! "})

        sql = """
			INSERT INTO users(username, password, role, class) VALUES ('{}', '{}', {}, '{}')
			""".format(request.form['username'], request.form['password'], request.form['role'], request.form['class'])
        results = db.engine.execute(text(sql))
        print(request.form['role'])
        if (request.form['role'] == '0'):
            sql = """
                INSERT INTO marks(studentname) VALUES ('{}')
                """.format(request.form['username'])
            results = db.engine.execute(text(sql))
        return redirect(url_for('login'))
    elif 'username' in session:

        return redirect('/')
    else:
        return render_template('register.html', data={})


@app.route('/mymarks', methods=['GET'])
def marks():
    if 'username' in session:
        sql = """
					SELECT assignment1, assignment2, assignment3, midtermexam, finalexam, lab
					FROM marks
					where studentname='{}'""".format(session['username'])
        results = db.engine.execute(text(sql))
        data = {"records": ([{column: value for column, value in rowproxy.items()}
                             for rowproxy in results][0]),
                "username": session['username']}
        # print(data)
        return render_template('marks.html', data=data)
    else:
        return render_template('home.html', data={"msg": "You are not login"})


@app.route('/remarking/<item>', methods=['POST'])
def remarking(item):
    if 'username' in session:
        sql = """
				INSERT INTO remarking(studentname, item, desc) VALUES('{}','{}','{}')
                    """.format(session['username'], escape(item), request.form['desc'])
        results = db.engine.execute(text(sql))
        return redirect(url_for('marks'))
    else:
        return render_template('home.html', data={"msg": "You are not login"})


@app.route('/remarking', methods=['GET'])
def getRemarking():
    if 'username' in session:
        sql = """
            SELECT *
            FROM users
            where username='{}'""".format(session['username'])
        results = db.engine.execute(text(sql))
        user = [{column: value for column, value in rowproxy.items()}
                for rowproxy in results][0]
        if (user['role'] != 1):
            return render_template('home.html', data={"msg": "unauthorized"})
        sql = """
            SELECT *
            FROM remarking
            """
        results = db.engine.execute(text(sql))
        requests = [{column: value for column, value in rowproxy.items()}
                    for rowproxy in results]
        print(requests)
        return render_template('requests.html', data={"username": session['username'], "requests": requests})

    else:
        return render_template('home.html', data={"msg": "You are not login"})


@app.route('/feedbacks', methods=['GET'])
def getFeedbacks():
    if 'username' in session:
        sql = """
            SELECT *
            FROM users
            where username='{}'""".format(session['username'])
        results = db.engine.execute(text(sql))
        user = [{column: value for column, value in rowproxy.items()}
                for rowproxy in results][0]
        if (user['role'] != 1):
            return render_template('home.html', data={"msg": "unauthorized"})
        sql = """
            SELECT *
            FROM feedback WHERE instructorname = '{}'
            """.format(session['username'])
        results = db.engine.execute(text(sql))
        feedbacks = [{column: value for column, value in rowproxy.items()}
                     for rowproxy in results]
        print(feedbacks)
        return render_template('feedbacks.html', data={"username": session['username'], "feedbacks": feedbacks})

    else:
        return render_template('home.html', data={"msg": "You are not login"})


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        instructorname = request.form['instructor']
        item1 = request.form['item1']
        item2 = request.form['item2']
        item3 = request.form['item3']
        item4 = request.form['item4']
        sql = """
				INSERT INTO feedback(instructorname, item1,item2,item3,item4) 
                VALUES ('{}','{}','{}','{}','{}')
                    """.format(instructorname, item1, item2, item3, item4)
        results = db.engine.execute(text(sql))
        return redirect(url_for('feedback'))
    elif 'username' in session:
        if 'error' in session:
            errMsg = session['error']
        else:
            errMsg = None
        session.pop('error', None)
        sql = """
				SELECT username FROM users WHERE role = 1
                    """
        results = db.engine.execute(text(sql))

        data = {
            "username": session['username'],
            "errMsg": errMsg,
            "instructors": [{column: value for column, value in rowproxy.items()}
                            for rowproxy in results]
        }
        # print(data)
        return render_template('Anon_Feedback.html', data=data)
    else:
        return render_template('home.html', data={"msg": "You are not login"})


@app.route('/grades', methods=['GET'])
def grades():
    if 'username' in session:
        sql = """
			SELECT *
			FROM users WHERE username = '{}'
			""".format(session['username'])
        results = db.engine.execute(text(sql))
        user = [{column: value for column, value in rowproxy.items()}
                for rowproxy in results][0]
        if (user['role'] != 1):
            return redirect('/')
        else:
            sql = """
			SELECT *
			FROM users U, marks M WHERE U.class = '{}' AND U.username = M.studentname
			""".format(user['class'])
        results = db.engine.execute(text(sql))
        students = [{column: value for column, value in rowproxy.items()}
                    for rowproxy in results]
        # print(students)
        return render_template('grades.html', data={"students": students, "username": session["username"]})
    else:
        return redirect('/')


@app.route('/<file>', methods=['GET'])
def lab(file):
    if 'username' in session:
        return render_template(str(file) + '.html', data={"username": session["username"]})
    else:
        return redirect(url_for('login'))


# @app.route('/team', methods=['GET'])
# def team():
#     if 'username' in session:
#         return render_template('team.html', data={"username": session["username"]})
#     else:
#         return redirect(url_for('login'))


# @app.route('/calendar', methods=['GET'])
# def calendar():
#     if 'username' in session:
#         return render_template('calendar.html', data={"username": session["username"]})
#     else:
#         return redirect(url_for('login'))

# @app.route('/calendar', methods=['GET'])
# def calendar():
#     if 'username' in session:
#         return render_template('calendar.html', data={"username": session["username"]})
#     else:
#         return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
