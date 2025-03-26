import psycopg2, bcrypt #to query Postgres
from flask import Flask, request, session, jsonify, redirect, url_for, render_template #for frontend
from datetime import timedelta, datetime
from flask_cors import CORS
import matplotlib.pyplot as plt, mpld3
import numpy as np
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}, r"/api/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "DELETE"])
app.config['SECRET_KEY'] = 'crazysecretkey1234'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=3)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True  # Requires HTTPS

@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/socials')
def socials():
    return render_template('socials.html')

def get_db():
    conn = psycopg2.connect(
        host='localhost',
        database='word_count',
        user='postgres',
        password='Reading#4'
    )
    return conn

class Words:
    def __init__(self):
        pass

    def get_total_count(self, user_id):
        conn = None
        cursor = None
        try:
            conn = get_db()
            cursor = conn.cursor()

            query = 'SELECT SUM(total_words) FROM projects WHERE user_id=%s'
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            return {'total_words': result[0] or 0}
        except Exception as e:
            return {'error': str(e)}
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_total_graph(self, user_id):
        conn = None
        cursor = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            query = 'SELECT title, total_words FROM projects WHERE user_id=%s'
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            
            total_words = {}
            for row in rows:
                total_words[row[0]] = row[1]
            fig = json.dumps(total_words)
            return fig
        
        except Exception as e:
            return {'error': str(e)}
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        
    def get_project_count(self, project_id):
        conn = None
        cursor = None
        try:
            conn = get_db()
            cursor = conn.cursor()

            query = 'SELECT total_words FROM projects WHERE id=%s'
            cursor.execute(query, (project_id,))
            result = cursor.fetchone()
            return {'word_count': result[0]} if result else {'word_count': 0}
        except Exception as e:
            return {'error': str(e)}
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_all_words(self, user_id):
        conn = None
        cursor = None
        try:
            conn = get_db()
            cursor = conn.cursor()

            query = 'SELECT total_words, title FROM projects WHERE user_id=%s'
            cursor.execute(query, (user_id,))
            result = cursor.fetchall()
            return {"Project Totals:": result} if result else {'word_count': 0}
        except Exception as e:
            return {'error': str(e)}
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def get_word_log(self, project_id):
        conn = None
        cursor = None
        try:
            conn = get_db()
            cursor = conn.cursor()

            query = 'SELECT word_count, entry_date, comment FROM word_count WHERE project_id=%s'
            cursor.execute(query, (project_id,))
            result = cursor.fetchall()
            return [{'word_count': row[0], 'entry_date': row[1], 'comment': row[2]} for row in result] if result else []

        except Exception as e:
            return {'error': str(e)}
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_user_graph(self, user_id):  
        conn = None
        cursor = None 
        try:
            conn = get_db()
            cursor = conn.cursor()

            query = 'SELECT word_count FROM word_count WHERE user_id=%s'
            cursor.execute(query, (user_id,))
            word_count = cursor.fetchall()
            y_axis = np.array([row[0] for row in word_count])

            query1 = 'SELECT entry_date FROM word_count WHERE user_id=%s'
            cursor.execute(query1, (user_id,))
            entry_date = cursor.fetchall()
            x_axis = np.array([row[0] for row in entry_date])
            
            plt.plot(x_axis, y_axis)

            plt.xlabel('Time')

            plt.ylabel('Word Count')

            plt.title('Word Count Over Time')

            plt.show()
        except Exception as e:
            return {'error': str(e)}
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def add_project(self, user_id, title, description, genre, genre1, genre2):
        if user_id is None:
            return {'error': 'Invalid user ID'}
    
        try:
            conn = get_db()
            cursor = conn.cursor()

            cursor.execute('INSERT INTO projects (user_id, title, description, genre, genre1, genre2) VALUES (%s, %s, %s, %s, %s, %s)', (user_id, title, description, genre, genre1, genre2))
            conn.commit()
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()  # Close cursor
            conn.close()    # Close connection

    def remove_project(self, project_id):
        try:
            conn = get_db()
            cursor = conn.cursor()

            cursor.execute('DELETE FROM projects WHERE id=%s', (project_id,))
            conn.commit()
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()  # Close cursor
            conn.close()    # Close connection

    def remove_user(self, user_id):
        try:
            conn = get_db()
            cursor = conn.cursor()

            cursor.execute('DELETE FROM users WHERE id=%s', (user_id,))
            conn.commit()
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()  # Close cursor
            conn.close()    # Close connection

    def add_word_count(self, user_id, word_count, project_id, entry_date, comment):
        try: 
            conn = get_db()
            cursor = conn.cursor()

            cursor.execute('INSERT INTO word_count (user_id, word_count, project_id, entry_date, comment) VALUES (%s, %s, %s, %s, %s)', (user_id, word_count, project_id, entry_date, comment))

            cursor.execute('SELECT total_words FROM projects WHERE id=%s', (project_id,))
            total_words = cursor.fetchone()[0] or 0
            if word_count > 0:
                new_total = total_words + word_count
            else:
                new_total = max(0, total_words + word_count)

            cursor.execute('UPDATE projects SET total_words=%s WHERE id=%s', (new_total, project_id))
            conn.commit()
        except Exception as e:
            return {'error': str(e)}
        finally:
            cursor.close()  # Close cursor
            conn.close()    # Close connection

def add_user(username, plain_password, email):
    pass_hash = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM users WHERE email=%s', (email,))
        existing_email = cursor.fetchone()
        if existing_email:
            error_message = 'Email already associated with an account.'
            return {'error': error_message}
        
        cursor.execute('INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)', (username, pass_hash, email))

        conn.commit()  # Save changes
    except Exception as e:
        return {'error': str(e)}
    finally:
        cursor.close()  # Close cursor
        conn.close()    # Close connection

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        user_pwd = data.get('plain_password')
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('SELECT id, password_hash FROM users WHERE username=%s', (username,))
            user = cursor.fetchone()

            if user:
                print("User found:", user)
                hash_user = bytes(user[1])

                if bcrypt.checkpw(user_pwd.encode('utf-8'), hash_user):
                    print("Successfully logged in!")
                    session['user_id'] = user[0]
                    print("Session after assignment:", session)
                    session.permanent = True
                    return jsonify({"success": True, "user_id": user[0]})
            if not user:
                error_message = "No user exists"
                return jsonify ({'success': False,'error': error_message}), 400
            conn.commit()
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    current_user_id = session.get('user_id')
    if current_user_id is None:
        return redirect(url_for('login'))
    else:
        session.pop('user_id', None)
        return jsonify({'success': True, "message": "Successfully logged out."})

@app.route('/register', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('plain_password')
        email = data.get('email')
        result = add_user(username, password, email)
        if result and 'error' in result:
            return jsonify(result), 400
        return jsonify({"success": True})
    return render_template('register.html')

@app.route('/check_user', methods=['GET'])
def check_user():
    user_id = session.get('user_id')
    print("User ID in session:", user_id)
    if user_id:
        return jsonify({"user_id": user_id, "logged_in": True})
    return jsonify({"logged_in": False}), 401

W1 = Words()

@app.route('/user_home', methods=['GET'])
def user_home():
    user_id = request.args.get('user_id')
    '''
    current_user_id = session.get('user_id')
    if current_user_id is None:
        return redirect(url_for('login'))
        '''
    render_template('user_home.html')
    result = W1.get_total_graph(user_id,)

    if result is None:
        return jsonify({'Success': True})
    if result and 'error' in result:
        return jsonify({'success': False, 'message': result}), 400
    return jsonify({'success': True, 'chartData': result})

@app.route('/add_words', methods=['POST'])
def add_words():
    entry_date = datetime.now()
    current_user_id = session.get('user_id')
    if current_user_id is None:
        return redirect(url_for('login'))
    data = request.json
    result = W1.add_word_count(current_user_id, data['word_count'], data['project_id'], entry_date, data['comment'])
    if result and 'error' in result:
        return jsonify({'success': False, 'message': result}), 400
    return jsonify({'success': True, 'message': result}), 201

@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    current_user_id = session.get('user_id')
    if current_user_id is None:
        return redirect(url_for('login'))
    data = request.json
    result = W1.remove_user(data['id'],)
    if result and 'error' in result:
        return jsonify({'success': False, 'message': result}), 400
    return jsonify({'success': True, 'message': result}), 200

@app.route('/add_project', methods=['GET', 'POST'])
def create_project():
    current_user_id = session.get('user_id')
    '''
    if current_user_id is None:
        return redirect(url_for('login'))
        '''
    if request.method == 'POST':
        data = request.get_json()
        title = data.get['title']
        description = data.get['description']
        genre = data.get['genre']
        genre1 = data.get['genre1']
        genre2 = data.get['genre2']
        result = W1.add_project(current_user_id, title, description, genre, genre1, genre2)
        if result and 'error' in result:
            return jsonify({'success': False, 'message': result}), 400
        return jsonify({'success': True, 'message': result}), 201
    return render_template('add_project.html')
    
@app.route('/remove_project', methods=['DELETE'])
def delete_project():
    current_user_id = session.get('user_id')
    if current_user_id is None:
        return redirect(url_for('login'))
    data = request.json
    result = W1.remove_project(data['id'],)
    if result and 'error' in result:
        return jsonify({'success': False, 'message': result}), 400
    return jsonify({'success': True, 'message': result}), 200

@app.route('/get_total', methods=['POST'])
def get_total():
    current_user_id = session.get('user_id')
    if current_user_id is None:
        return redirect(url_for('login'))
    data = request.json
    result = W1.get_total_count(data['user_id'],)
    if result and 'error' in result:
        return jsonify({'success': False, 'message': result}), 400
    return jsonify({'success': True, 'message': result}), 200

@app.route('/project_count', methods=['POST'])
def project_count():
    current_user_id = session.get('user_id')
    if current_user_id is None:
        return redirect(url_for('login'))
    data = request.json
    result = W1.get_project_count(data['project_id'],)
    if result and 'error' in result:
        return jsonify({'success': False, 'message': result}), 400
    return jsonify({'success': True, 'message': result}), 200

@app.route('/all_words', methods=['POST'])
def all_words():
    current_user_id = session.get('user_id')
    if current_user_id is None:
        return redirect(url_for('login'))
    data = request.json
    result = W1.get_all_words(data['user_id'],)
    if result and 'error' in result:
        return jsonify({'success': False, 'message': result}), 400
    return jsonify({'success': True, 'message': result}), 200

@app.route('/word_log', methods=['POST'])
def word_log():
    current_user_id = session.get('user_id')
    if current_user_id is None:
        return redirect(url_for('login'))
    data = request.json
    result = W1.get_word_log(data['project_id'],)
    if result and 'error' in result:
        return jsonify({'success': False, 'message': result}), 400
    return jsonify({'success': True, 'message': result}), 200

@app.route('/get_line', methods=['POST'])
def get_line():
    current_user_id = session.get('user_id')
    if current_user_id is None:
        return redirect(url_for('login'))
    data = request.json
    result = W1.get_user_graph(data['user_id'],)
    if result and 'error' in result:
        return jsonify({'success': False, 'message': result}), 400
    return jsonify({'success': True, 'message': result}), 200

@app.route('/test_conn', methods=['GET'])
def test_conn():
    try:
        conn = get_db()
        conn.close()
        return jsonify(message='Database connection successful!'), 200
    except Exception as e:
        return jsonify(message='Database connection failed!', error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
