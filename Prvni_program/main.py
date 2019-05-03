# Importujeme
from flask import Flask, render_template, jsonify
import requests
from flask_wtf import FlaskForm
from wtforms import SelectField, widgets



app = Flask(__name__)
# Musíme nastavit SECRET_KEY, pokud chceme používat CSRF
app.config["SECRET_KEY"] = "super tajny klic"



class MujFormular(FlaskForm):
    operator = SelectField("Operátor", choices=[("N4G" ,"N4G"),("OGE" ,"OGE")])
    point = SelectField("IP", choices=[("Waidhaus" ,"Waidhaus"),("Lanžhot" ,"Lanžhot")])


@app.route("/", methods = ["GET", "POST"])
def index():
    form = MujFormular()
    url = 'https://transparency.entsog.eu/api/v1/operationaldatas?PointLabel={}&from=31-03-2019&to=31-12-2019&directionKey=entry'
    point='Waidhaus'
    r=requests.get(url.format(point)).json()
    x= {r['operationaldatas'][0]['value']}

    points = {
      'pointLabel': point,
      'value' : r['operationaldatas'][0]['value']
    }

    if form.validate_on_submit():
        operator = form.operator.data
        point = form.point.data
        vysledek = eval( 'x' )
        return render_template("formular.html", vysledek = vysledek, form = form)
    return render_template("formular.html", form = form)