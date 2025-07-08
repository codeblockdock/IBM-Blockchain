from flask import Flask, request, render_template, redirect, flash
from blockchain import Blockchain
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'secret123'
blockchain = Blockchain()

def hash_file(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            file_hash = hash_file(path)

            if 'verify' in request.form:
                for block in blockchain.chain:
                    if block.data == file_hash:
                        flash("Document is VERIFIED! Hash found on blockchain.", "success")
                        break
                else:
                    flash("Document is NOT verified. Hash not found.", "danger")
            else:
                blockchain.add_block(file_hash)
                flash("Document hash added to blockchain successfully.", "info")
            os.remove(path)
    return render_template('index.html', chain=blockchain.chain)

if __name__ == '__main__':
    app.run(debug=True)
