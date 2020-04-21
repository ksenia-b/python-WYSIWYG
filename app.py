from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import bleach

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class EditorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    html = db.Column(db.Text)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cleaned_data = bleach.clean(request.form.get('editordata'), tags = bleach.sanitizer.ALLOWED_TAGS + ['div', 'br'])
        new_data = EditorData(html=cleaned_data)
        db.session.add(new_data)
        db.session.commit()
        print('Posted Data')

        return 'Posted Data' #redirect(url_for('index'))

    return render_template('index.html')


@app.route('/display/<int:id>')
def display(id):
    data = EditorData.query.get(id)
    print(data.html)
    return render_template('display.html', data=data.html)
