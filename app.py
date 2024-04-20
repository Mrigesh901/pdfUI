from flask import Flask, render_template, request, send_from_directory

import os

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/document')
def upload_document():
    return render_template('upload.html')

@app.route('/document/view', methods=['POST'])
def view_document():
    if 'file' not in request.files:
        return 'No file uploaded'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    return render_template('view_document.html', filename=filename)

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':  
    app.run(debug=True)
