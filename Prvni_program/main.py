# Importujeme
from flask import Flask, render_template, jsonify
import requests
from flask_wtf import FlaskForm
from wtforms import SelectField, widgets, DateField
from wtforms.fields.html5 import DateField
from flask_sqlalchemy import SQLAlchemy
import sqlite3


app = Flask(__name__)

   

app.config["SECRET_KEY"] = "super tajny klic"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///points.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Vytvoření databáze pro pevné hodnoty
db = SQLAlchemy(app)

class Points(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    label = db.Column(db.String(200), unique=True, nullable=False)

class MujFormular(FlaskForm):
    operator = SelectField("Operator", choices=[("N4G" ,"N4G"),("OGE" ,"OGE")])
    point = SelectField("IP", choices=[("Waidhaus" ,"Waidhaus"),("Lanžhot" ,"Lanžhot")])
    direction = SelectField("Direction", choices=[("entry" ,"entry"),("exit" ,"exit")])
    indicator = SelectField("Indicator", choices=[("Capacity" ,"Capacity"),("Interruptions" ,"Interruptions")])
    date_from = DateField("Date from", format='%Y-%m-%d')
    date_to = DateField("Date to", format='%Y-%m-%d')

@app.route("/", methods = ["GET", "POST"])
def index():
    form = MujFormular()
    point='Waidhaus'
    url = f'https://transparency.entsog.eu/api/v1/operationaldatas?PointLabel={point}&from=31-03-2019&to=31-12-2019&directionKey=entry'
    
    r=requests.get(url).json()
    x= {r['operationaldatas'][0]['value']}

    points = {
      'pointLabel': point,
      'value' : r['operationaldatas'][0]['value']
    }

    if form.validate_on_submit():
        operator = form.operator.data
        point = form.point.data
        direction = form.direction.data
        date_from = form.date_from.data
        date_to = form.date_to.data
        vysledek = eval( 'x' )
        return render_template("formular.html", vysledek = vysledek, form = form)
    return render_template("formular.html", form = form)