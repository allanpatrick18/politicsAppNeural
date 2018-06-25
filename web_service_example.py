# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file and it will check if the image contains a picture of Barack Obama.
# The result is returned as json. For example:
#
# $ curl -XPOST -F "file=@obama2.jpg" http://127.0.0.1:5001
#
# Returns:
#
# {
#  "face_found_in_image": true,
#  "is_picture_of_obama": true
# }
#
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

import face_recognition
from flask import Flask, jsonify, request, redirect

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

# Pre-calculated face encoding of Obama generated with face_recognition.face_encodings(img)
list_of_politics = []
list_of_politics_encoding = []
politics_name = [
    {
        'name': 'Valdir Rossoni',
        'file': 'politics/valdir_rossoni.jpg',
        'encode': []

    },
    {
        'name': 'João Arruda',
        'file': 'politics/joao_arruda.jpg',
        'encode': []
    },
    {
        'name': 'Takaiama',
        'file': 'politics/hidekazu_takayama.jpg',
        'encode': []
    },
    {
        'name': 'Christiane Yered',
        'file': 'politics/christiane_yared.jpg',
        'encode': []
    }

]

for name in politics_name:
    list_of_politics.append(face_recognition.load_image_file(
        name['file']))

i = 0
for politic in list_of_politics:
    politics_name[i]['encode'] = face_recognition.face_encodings(
        politic)[0]
    i += 1

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Is this a picture of Obama?</title>
    <h1>Upload a picture and see if it's a picture of Obama!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''

@app.route('/teste', methods=['GET', 'POST'])
def upload_image_teste():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)


def detect_faces_in_image(file_stream):
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)

    face_found = False
    is_one_politc = False

    if len(unknown_face_encodings) > 0:
        face_found = True
        # See if the first face in the uploaded image matches the known face of Obama
        for face_encode in politics_name:
            match_results = face_recognition.compare_faces(
                [face_encode['encode']],unknown_face_encodings[0])
            if match_results[0]:
                politic = face_encode
                is_one_politc = True
                break;

    # Return the result as json
    if is_one_politc is False:
        result = {
            "face_found_in_image": face_found,
            "is_picture_one_of_registred": is_one_politc
        }
    else:
        result = {
            "face_found_in_image": face_found,
            "is_picture_one_of_registred": is_one_politc,
            "politics_name": politic['name']
        }

    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
