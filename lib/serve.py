import os, os.path, hashlib, datetime
from flask import Flask, render_template, request, redirect, session
from lib.analyze import analyze

salt = b'dc55ceb6981339f2f629082ef75163cafb7525fc85d2ea7926f02fa1de7a528b'

app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = 'pythonExamproject'
image_ext = ['jpg', 'png']

def validate_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in image_ext

@app.route("/", methods=["GET","POST"])

def index():
    testing = False

    if not 'id' in session:
        ident = str(datetime.datetime.now())
        ssid = hashlib.pbkdf2_hmac('sha256', bytes(ident, 'raw_unicode_escape'), salt, 100000)
        session['id'] = ssid

    ssid = session['id']
    path = "tempuploads/" + str(ssid) + ".jpg"

    if os.path.exists(path):
        print("Image exists:", path)
        testing = True

    extensions = ""
    for ext in image_ext:
        extensions += "." + ext + ","

    extensions = extensions[0:-1]

    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']

        if file.filename == '':
            return redirect(request.url)

        if file and validate_extension(file.filename):
            if os.path.exists(path):
                return redirect(request.url)

            print("Recieving Image ...")
            file.save(path)
            testing = True


    return render_template("index.html", ext=extensions, testing=testing)

@app.route("/test", methods=["GET"])

def test():
    img = "tempuploads/" + str(session["id"]) + ".jpg"
    status = analyze(img)

    return status