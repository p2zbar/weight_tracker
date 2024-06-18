from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weights.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'  # Changez cette clé pour une clé plus sécurisée
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    waist = db.Column(db.Float, nullable=False)
    arm = db.Column(db.Float, nullable=False)
    thigh = db.Column(db.Float, nullable=False)
    calf = db.Column(db.Float, nullable=False)
    chest = db.Column(db.Float, nullable=False)
    shoulder = db.Column(db.Float, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_tables():
    with app.app_context():
        db.create_all()
        # Ajouter un utilisateur par défaut
        if User.query.filter_by(username='p2r').first() is None:
            new_user = User(username='p2r', password='danylord')
            db.session.add(new_user)
            db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        date = request.form['date']
        weight = float(request.form['weight'])
        waist = float(request.form['waist'])
        arm = float(request.form['arm'])
        thigh = float(request.form['thigh'])
        calf = float(request.form['calf'])
        chest = float(request.form['chest'])
        shoulder = float(request.form['shoulder'])
        new_weight = Weight(date=datetime.strptime(date, '%Y-%m-%d'), weight=weight, waist=waist, arm=arm, thigh=thigh, calf=calf, chest=chest, shoulder=shoulder)
        db.session.add(new_weight)
        db.session.commit()
        return redirect(url_for('index'))
    weights = Weight.query.order_by(Weight.date).all()

    # Calculer la perte de poids totale
    if weights:
        total_weight_loss = weights[0].weight - weights[-1].weight
    else:
        total_weight_loss = 0

    # Préparation des données pour Plotly
    dates = [weight.date.strftime('%Y-%m-%d') for weight in weights]
    values = [weight.weight for weight in weights]
    waists = [weight.waist for weight in weights]
    arms = [weight.arm for weight in weights]
    thighs = [weight.thigh for weight in weights]
    calfs = [weight.calf for weight in weights]
    chests = [weight.chest for weight in weights]
    shoulders = [weight.shoulder for weight in weights]

    data = {
        'dates': dates,
        'values': values,
        'waists': waists,
        'arms': arms,
        'thighs': thighs,
        'calfs': calfs,
        'chests': chests,
        'shoulders': shoulders
    }

    return render_template('index.html', weights=weights, data=json.dumps(data), total_weight_loss=total_weight_loss)

@app.route('/edit/<int:weight_id>', methods=['GET', 'POST'])
@login_required
def edit(weight_id):
    weight = Weight.query.get_or_404(weight_id)
    if request.method == 'POST':
        weight.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        weight.weight = float(request.form['weight'])
        weight.waist = float(request.form['waist'])
        weight.arm = float(request.form['arm'])
        weight.thigh = float(request.form['thigh'])
        weight.calf = float(request.form['calf'])
        weight.chest = float(request.form['chest'])
        weight.shoulder = float(request.form['shoulder'])
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', weight=weight)

@app.route('/delete/<int:weight_id>', methods=['POST'])
@login_required
def delete(weight_id):
    weight = Weight.query.get_or_404(weight_id)
    db.session.delete(weight)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='0.0.0.0')
