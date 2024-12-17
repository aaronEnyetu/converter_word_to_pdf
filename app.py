from flask import Flask, render_template, request, send_file
import os
from docx2pdf import convert

app = Flask(__name__)

# Define the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'docx'}

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Convert DOCX to PDF
        output_pdf = os.path.join(app.config['UPLOAD_FOLDER'], f"{os.path.splitext(file.filename)[0]}.pdf")
        convert(filename, output_pdf)

        # Send the converted file to the user
        return send_file(output_pdf, as_attachment=True)

    return 'Invalid file format', 400

if __name__ == '__main__':
    app.run(debug=True)
