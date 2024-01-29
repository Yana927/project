from datetime import datetime

from flask_bootstrap import Bootstrap4
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap4(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Event(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   date = db.Column(db.Date, nullable=False)
   name = db.Column(db.String(255), nullable=False)
   duration = db.Column(db.Integer, nullable=False)

   def __str__(self):
       return (
           f"Название: {self.name}\n"
           f"Дата: {self.date}\n"
           f"Продолжительность {self.duration}ч")

@app.route('/', methods=['POST'])
def add_event():
    date = datetime.strptime(request.form['eventDate'], '%Y-%m-%d').date()
    name = request.form['eventName']
    duration = int(request.form['eventDuration'])
    print(date, name, duration, sep='\n')
    event = Event(date=date, name=name, duration=duration)
    db.session.add(event)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return redirect('/events')


@app.route('/')
def index():
    return render_template('index.html', h1 = 'Главная страница')



@app.route('/detail')
def view_detail():
    events = Event.query.order_by(Event.date).all()
    return render_template('detail.html', h1 = 'События', events=events)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    