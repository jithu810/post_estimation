

from turtle import right
from flask import Flask,render_template,request,make_response,jsonify,session,redirect,flash

from demo import ss
app = Flask(__name__)
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
import os
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'




@app.route('/',methods=['GET','POST'])
def Home():
    if request.method == 'POST':
        file = request.files['f']  
        if not request.files.get('f', None):
            return jsonify({'status':0,'message':'select file first'})
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        result=ss("output/"+filename)

        print(result)

        for i in result:
            if i[0]==0:
                nose={'x':i[1],'y':i[2]}
            if i[0]==2:
                left_sholder={'x':i[1],'y':i[2]}


        if result=="":
            return jsonify({'status':0,'message':'result empty'})
        else:
            return jsonify({'status':0,'message':'points','nose':nose,'left_sholder':left_sholder})
    return render_template("home.html")



@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)



if __name__=="__main__":
    app.run()
    app.run(debug=True)