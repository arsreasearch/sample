from flask import *  
import os

app = Flask(__name__)  
 
UPLOAD_FOLDER = 'uploads'


@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))  
        return render_template("success.html", name = f.filename) 


if __name__ == '__main__':  
    app.run(debug = True)  