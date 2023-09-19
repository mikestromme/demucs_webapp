from flask import Flask, render_template, request, send_file, send_from_directory
import os
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        # Process the uploaded file with Demucs
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        demucs_command = f'demucs -n mdx_extra "{filename}"'
        subprocess.run(demucs_command, shell=True)
        # Provide download link for processed files (to be implemented)
        return "File uploaded and processed successfully!"
        # Provide download link for processed files
        processed_filename = file.filename.replace('.mp3', '_demucs.wav')  # Adjust file extension as needed
        return f'<a href="/download/{processed_filename}">Download Processed File</a>'

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('output', filename)

if __name__ == '__main__':
    app.run(debug=True)
