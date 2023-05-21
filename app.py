from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(30), unique=True)
    register_number = db.Column(db.String(30))
    password = db.Column(db.String(30))

    def _init_(self, name, email, register_number, password):
        self.name = name
        self.email = email
        self.register_number = register_number
        self.password = password
    
    def __repr__(self):
        return '<Name %r >' %self.id

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50))
    brandings = db.Column(db.String(50))
    authorized_signatory = db.Column(db.String(50))
    participants = db.Column(db.String(200))
    winners = db.Column(db.String(200))

    def _init_(self, event_name, brandings, authorized_signatory, participants, winners):
        self.event_name = event_name
        self.brandings = brandings
        self.authorized_signatory = authorized_signatory
        self.participants = participants
        self.winners = winners

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email).first()

        if user and password:
            return redirect('/landing/')
        
        return render_template('login.html')

    return render_template('login.html')

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        register_number = request.form['register-number']
        password = request.form['password']
        try:
            user = User(name=name, email=email, register_number=register_number, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect('/landing/')
        except:
            return "There was an error in adding your records in the database!"

    return render_template('signup.html')

@app.route('/landing/')
def landing():
    return render_template('landing.html')

@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        event_name = request.form['event_name']
        brandings = request.form['brandings']
        authorized_signatory = request.files['authorized_signatory']
        participants = request.form.getlist('participants')
        winners = request.form.getlist('winners')

        if authorized_signatory:
            filename = authorized_signatory.filename
            authorized_signatory.save('uploads/' + filename)
        else:
            filename = ''

        event = Event(event_name, brandings, filename, ', '.join(participants), ', '.join(winners))
        db.session.add(event)
        db.session.commit()

        return redirect('/landing/')

    return render_template('dashboard.html')

if __name__ == "_main_":
    with app.app_context():
        db.create_all()
    app.run(debug=True)