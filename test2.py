from flask import Flask, render_template, Response, request, redirect, url_for, session, flash, jsonify
from camera import Video
import os
app= Flask(__name__)
app.secret_key = os.urandom(24)
app.config['STATIC_FOLDER'] = 'static'
users = {'Elon.m': '12345','Emilymarton': 'm.125'}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
            return render_template('logpage.html')
    return render_template('logpage.html')

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))
def gen(camera):
 while True:
    frame, authenticated = camera.get_frame()
   
    yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
@app.route('/video')
def video ():
   if 'username' in session: 
    return Response(gen(Video()),
    mimetype= 'multipart/x-mixed-replace; boundary= frame')
   return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
 app.run(debug=True)
