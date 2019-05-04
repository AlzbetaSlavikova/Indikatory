# Importujeme
from flask import Flask, render_template, jsonify
import requests
from flask_wtf import FlaskForm
from wtforms import SelectField, widgets, DateField
from wtforms.fields.html5 import DateField


app = Flask(__name__)
# Musíme nastavit SECRET_KEY, pokud chceme používat CSRF
app.config["SECRET_KEY"] = "super tajny klic"


class MujFormular(FlaskForm):
    operator = SelectField("Operátor", choices=[("N4G" ,"N4G"),("OGE" ,"OGE")])
    point = SelectField("IP", choices=[("Waidhaus" ,"Waidhaus"),("Lanžhot" ,"Lanžhot")])
    date_from = DateField("Datum od", format='%Y-%m-%d')
    date_to = DateField("Datum do", format='%Y-%m-%d')

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
        date_from = form.date_from.data
        date_to = form.date_to.data
        vysledek = eval( 'x' )
        return render_template("formular.html", vysledek = vysledek, form = form)
    return render_template("formular.html", form = form)