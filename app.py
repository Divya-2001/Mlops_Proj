from model import filter
from flask import Flask, flash, request, redirect, render_template, send_file
import os
import cv2
from PIL import Image
import base64
import io
from filters import *
# Images List ....
imagesList = []

# Storing Image
def storeImage(image, filterName):
    path = f"F:\MyProgramFiles\All Jupyter Files\Machine Learning\Car Number Plate Detector\storage\{filterName}.jpg"
    cv2.imwrite(path,image)

# Encoding Image
def encodeImage(image):
    filteredImage = Image.open(image)
    data = io.BytesIO()
    filteredImage.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())
    return encoded_img_data


# Adding In List ....
def addInList(filteredImage, filterName, idTag):
    # store image....
    storeImage(filteredImage, filterName)
    # encode image ....
    path = f"F:\MyProgramFiles\All Jupyter Files\Machine Learning\Car Number Plate Detector\storage\{filterName}.jpg"
    encoded_img_data = encodeImage(path)
    # add in list ....
    imagesList.append([encoded_img_data.decode('utf-8'), filterName, idTag])

app = Flask(__name__)

UPLOAD_FOLDER = 'storage/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/after', methods=['POST'])
def after():
    if 'file1' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file1']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    target = os.path.join(UPLOAD_FOLDER, '')
    # message = request.form['message']
    if not os.path.isdir(target):
        os.makedirs(target)
    if request.method == 'POST':
        file = request.files['file1']
        file_name = file.filename or ''
        destination = ''.join([target, file_name])
        file.save(destination)

        # clear list before refresh ....
        imagesList.clear()
        # object of filters class....
        filter = filters()

        # normal filter ....
        filteredImage = filter.normal(destination)
        addInList(filteredImage, "Normal", 1)

        # sharp, hdr, inverted, summer, winter, finalSketch]
        # Grey
        filteredImage = filter.greyscale(destination)
        addInList(filteredImage, "Grey", 2)

        # BrightMore
        filteredImage = filter.brightMore(destination)
        addInList(filteredImage, "More Bright", 3)

        # BrightLess
        filteredImage = filter.brightLess(destination)
        addInList(filteredImage, "Less Bright", 4)

        # Sharp
        filteredImage = filter.sharp(destination)
        addInList(filteredImage, "Sharp", 5)

        # HDR
        filteredImage = filter.HDREffect(destination)
        addInList(filteredImage, "HDR", 6)

        # Invert
        filteredImage = filter.invert(destination)
        addInList(filteredImage, "Invert", 7)

        # Summer
        filteredImage = filter.summer(destination)
        addInList(filteredImage, "Summer", 8)

        # Winter
        filteredImage = filter.winter(destination)
        addInList(filteredImage, "Winter", 9)

        # PencilSketch
        filteredImage = filter.pencilSketch(destination)
        addInList(filteredImage, "Pencil Sketch", 10)


        # Remove Images ....
        BASE_DIR = os.getcwd()
        dir = os.path.join(BASE_DIR, "storage")

        for root, dirs, files in os.walk(dir):
            for file in files:
                path = os.path.join(dir, file)
                os.remove(path)

        return render_template("after.html", imagesList=imagesList)



    # BASE_DIR = os.getcwd()
    # dir = os.path.join(BASE_DIR, "uploads")

    # for root, dirs, files in os.walk(dir):
    #     for file in files:
    #         path = os.path.join(dir, file)
    #         os.remove(path)
    # filename = "http://127.0.0.1:4568/storage/greyscale.jpg"
    # return render_template('after.html', filename = filename)
    # return send_file(out, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True, port=4568)
