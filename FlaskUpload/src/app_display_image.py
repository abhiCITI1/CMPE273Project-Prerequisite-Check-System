import os
from uuid import uuid4
import pyautogui


from flask import Flask, request, render_template, send_from_directory


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")

def index():
    return render_template("upload.html")


    

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
        return render_template("button.html")

      #return send_from_directory("images", filename, as_attachment=True)
        return render_template("complete_display_image.html", image_name=filename)
      



@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)






if __name__ == "__main__":
    app.run(port=4555, debug=True)
