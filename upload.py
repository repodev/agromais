import os, hashlib, time
from flask import Flask, request, redirect, url_for,flash,session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'teste'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        if ('file' not in request.files):
            flash('No file part')
            return "not"
        file = request.files['file']
        if file and allowed_file(file.filename):
            

            filename = secure_filename(file.filename)
            filename_novo = filename.split(".")[1]
            gera_tempo = str(time.time())
            gera_nome = hashlib.sha256(gera_tempo.encode()).hexdigest()
            novo_nome = gera_nome[0:20]+"."+filename_novo
            print(novo_nome)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], novo_nome))
            return redirect(url_for('index'))
            
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)