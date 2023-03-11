from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import datetime
from sqlalchemy import Column, Integer, DateTime
from markupsafe import  escape
myapp =  Flask(__name__)  # give flask entry of your application

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
myapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
import os
from flask_sqlalchemy import SQLAlchemy

myapp.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db= SQLAlchemy(myapp)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    des= db.Column(db.String(100),unique=True, nullable=True)
    created_date =db.Column(DateTime, default=datetime.datetime.utcnow)
    img = db.Column(db.Text, unique=False, nullable=True)

    def __str__(self):
        return f"{self.name}"

@myapp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html')

@myapp.route('/', endpoint='student_db')
def students_index():
    students = Product.query.all()
    return render_template('product-tmp/index.html', students=students)


@myapp.route('/product/<id>', endpoint='student_details')
def student_info(id):
    student = Product.query.get_or_404(id)
    return render_template('product-tmp/show.html', student=student)

@myapp.route('/add', endpoint='addProduct')
def addNewProduct():
    return render_template('product-tmp/add.html')

@myapp.route('/saveData',   methods=['POST'])
def saveProduct():
    name = request.form.get('name')
    desc = request.form.get('des')
    image = request.files['file']
    # filename = secure_filename(image)
    
    # save = os.path.join(myapp.config['UPLOAD_FOLDER']
    # filename.save(save , filename))
    st1 = Product(title=f'{name}',des=f'{desc}' , img = '111')
    db.session.add(st1)
    db.session.commit()
    return redirect(url_for('student_db'))
    
@myapp.route('/product/update/<id>', endpoint='update')
def student_delete(id):
    student = Product.query.get_or_404(id)
    return render_template('product-tmp/update.html', student=student)
@myapp.route('/saveupdate', methods=['POST'])
def saveupdate():
    id = request.form.get('id')
    name = request.form.get('name')
    des = request.form.get('des')
    image = request.files['file']
    filename = secure_filename(image.filename)
    print('..................................')
    print(image)
    print('..................................')
    student = Product.query.filter_by(id=id).first()
    student.title = name
    student.des = des
    db.session.commit()
    return redirect(url_for('student_db'))

  

@myapp.route('/product/delete/<id>', endpoint='student_delete')
def student_delete(id):
    student = Product.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for("student_db"))
    
if __name__=='__main__':
    myapp.run(debug=True)

