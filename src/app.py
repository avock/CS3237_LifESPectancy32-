#app.py
from flask import Flask, json, request, jsonify, redirect, url_for
import os
import urllib.request
from werkzeug.utils import secure_filename
 
import cv2
from ML.opencv import compare_image
 
app = Flask(__name__, static_folder='../static')
 
app.secret_key = "caircocoders-ednalan"
 
UPLOAD_FOLDER = os.path.join('static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
TARGET_FILENAME = 'esp32_cam_image.jpeg'
 
def allowed_filetype(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/')
def main():
    return 'Homepage'
 
@app.route('/image/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'imageFile' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
 
    file = request.files['imageFile']
     
    errors = {}
    success = False
     
    if allowed_filetype(file.filename):
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        old_filename = "old_" + TARGET_FILENAME

        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], TARGET_FILENAME)):

            os.rename(os.path.join(app.config['UPLOAD_FOLDER'], TARGET_FILENAME),
                      os.path.join(app.config['UPLOAD_FOLDER'], old_filename))

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], TARGET_FILENAME))
        success = True
    else:
        errors[file.filename] = 'File type is not allowed'
 
    if success and not errors:
        
        image1 = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], old_filename))
        image2 = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], TARGET_FILENAME))
        
        if image1.shape != image2.shape:
            print("Images have different dimensions. They are not directly comparable.")
        else:
            results = True if compare_image(image1, image2) > 0.5 else False
        
        resp = jsonify({
            'message' : 'Files successfully uploaded',
            'is_different': f'{results}'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
 
@app.route('/image/download/<image_filename>')
def download_file(image_filename):
    filename = secure_filename(image_filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # TODO : To re-add check for file existence
    # if not os.path.exists(file_path):
    #     error_response = {'error': 'File not found'}
    #     return jsonify(error_response), 404

    static_image_url = url_for('static', filename=image_filename)
    return redirect(static_image_url)

@app.route('/<path:path>')
def fallback(path):
    return "Wrong Endpoint!"
 
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)