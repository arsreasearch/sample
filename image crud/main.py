from flask import *  
import os
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
import cv2
import sys
from PIL import Image
import numpy as np 
from PIL import Image
import datetime



project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "image.db"))
UPLOAD_FOLDER = os.path.join('static', 'uploads')

app = Flask(__name__) 

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app) 
 
class Image(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)


###########################################################################

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/calc')
def calc():
    def get_frame():
        camera_port=0
        camera=cv2.VideoCapture(camera_port) 
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        while True:
            retval, img = camera.read() 
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x,y,w,h) in faces:
                # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0), 1)
                cv2.imwrite("img/img.jpg",gray[y:y+h,x:x+w])
                break
                camera.release()
                cv2.destroyAllWindows()

            
            imgencode=cv2.imencode('.jpg',img)[1]
            stringData=imgencode.tostring()
            yield (b'--frame\r\n'
                b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        del(camera)
    return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

    
# @app.route('/calc')
# def calc():
#      return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')


##########################################################################

@app.route('/upload')  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/success',  methods = ['POST'])  
def success():  
    imgs = None
    if request.method == 'POST':  
        f = request.files['file']  
        src = os.path.join(UPLOAD_FOLDER, f.filename)
        print(src)
        f.save(src)  
        img = Image(title=src)
        db.session.add(img)
        db.session.commit()
    imgs = Image.query.all()
    return render_template("gallery.html", imgs=imgs)

@app.route('/gallery')  
def gallery():  
    imgs = Image.query.all()
    return render_template("gallery.html", imgs=imgs)

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    src = Image.query.filter_by(title=title).first()
    db.session.delete(src)
    db.session.commit()
    os.remove(title) 
    return redirect("/gallery")
        
        
if __name__ == '__main__':  
    app.run(debug = True)  