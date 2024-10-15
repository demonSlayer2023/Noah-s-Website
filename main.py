import os
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename

app = Flask(__name__)
socketio = SocketIO(app)

# Configure the upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # Limit upload size to 16 MB


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if the file is in the request
        if 'image' not in request.files:
            return 'No file part'
        file = request.files['image']

        # If no file is selected
        if file.filename == '':
            return 'No selected file'

        # Save the file with a secure filename
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Save the file
        return f'File {filename} uploaded successfully!'

    return render_template('upload.html')


@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    print(f'Message from {username}: {message}')
    socketio.emit('message', {'username': username, 'message': message}, broadcast=True)


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])  # Ensure the upload directory exists
    socketio.run(app, debug=True)
