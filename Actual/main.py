from flask import Flask, render_template, jsonify, Response
import requests
from flask_wtf import FlaskForm
from wtforms import SelectField, widgets, RadioField, DateField 
from wtforms.fields.html5 import DateField
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import io
import numpy as np 
import matplotlib.pyplot as plt
import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "super tajny klic"


class MujFormular(FlaskForm):
    operator = SelectField("Operátor", choices=[("SK-TSO-0001", "eustream"),("BE-TSO-0001", "Fluxys Belgium"),("DE-TSO-0001", "Gascade"),("GCA", "GCA"),("PL-TSO-0001", "Gaz-System"),("Innogy GS", "Innogy GS"),("MND", "MND"),("CZ-TSO-0001", "Moravia GS"),("CZ-TSO-0001", "NET4GAS"),("DE-TSO-0009" ,"Open Grid Europe"),("DE-TSO-0003", "ONTRAS"),("DE-TSO-0016", "OPAL"),("Tarvisio", "Tarvisio"),("Ukrtransgaz", "Ukrtransgaz")])
    point = SelectField("IP", choices=[("Brandov STEGAL (CZ) / Stegal (DE)","Brandov STEGAL"),("Brandov-OPAL (DE)","Brandov OPAL"),("Waidhaus" ,"Waidhaus"),("Lanžhot" ,"Lanžhot"),("Hora Svaté Kateřiny (CZ) / Deutschneudorf (Sayda) (DE)","HSK/Deutschendorf"),("Olbernhau (DE) / Hora Svaté Kateřiny (CZ)","Olberhau/HSK"),("Kondratki","Kondratki"),("Mallnow","Mallnow")])
    
    indicator = RadioField("Indikátor", choices=[("Interruptible Available" ,"Interruptible Available"),("Interruptible Booked", "Interruptible Booked"),("Interruptible Total" ,"Interruptible Total"),("Firm Technical", "Firm Technical"),("Firm Booked", "Firm Booked"),("Firm Available", "Firm Available"),("Planned interruption of firm capacity", "Planned interruption of firm capacity"),("Unplanned interruption of firm capacity", "Unplanned interruption of firm capacity"),("Planned interruption of interruptible capacity", "Planned interruption of interruptible capacity"), ("Unplanned interruption of interruptible capacity", "Unplanned interruption of interruptible capacity")])
    date_from = DateField("Datum od", format='%Y-%m-%d')
    date_to = DateField("Datum do", format='%Y-%m-%d')


@app.route("/", methods = ["GET"])
def view():

    return render_template("introduction.html")

@app.route("/graf_E", methods = ["GET"])
def view1():
    return render_template("formular2.html", form = MujFormular())

@app.route("/graf_E", methods = ["POST"])
def index():
    form = MujFormular()
    operator = form.operator.data
    point= form.point.data
    
    indicator = form.indicator.data
    iso_date_from = form.date_from.data
    iso_date_to = form.date_to.data

    date_from = iso_date_from.strftime("%d-%m-%Y")
    date_to = iso_date_to.strftime("%d-%m-%Y")
    
    url_entry = f'https://transparency.entsog.eu/api/v1/operationaldatas?operatorKey={operator}&pointLabel={point}&indicator={indicator}&from={date_from}&to={date_to}&directionKey=entry&limit=-1'
    
    r_entry=requests.get(url_entry).json()
    
    url_exit = f'https://transparency.entsog.eu/api/v1/operationaldatas?operatorKey={operator}&pointLabel={point}&indicator={indicator}&from={date_from}&to={date_to}&directionKey=exit&limit=-1'
    
    r_exit=requests.get(url_exit).json()

    value_list_entry = list()
    
    for x in r_entry['operationaldatas']:
      hodnota_entry = x['value']
      value_list_entry.append(int(hodnota_entry))

    value_list_exit = list()

    for x in r_exit['operationaldatas']:
      hodnota_exit = x['value']
      value_list_exit.append(int(hodnota_exit))

  #jak ošetřit nulové hodnoty?
  #dalo by se u grafu vyklikávat indikátory a na základě toho zobrazovat?
  #jak udělat, aby se stránka posouvala


    if form.validate_on_submit():
        operator = form.operator.data
        point = form.point.data
        direction = form.direction.data
        date_from = form.date_from.data
        date_to = form.date_to.data
        vysledek = [value_list_entry, value_list_exit]
        return render_template("formular2.html", vysledek = vysledek, form = form, value_list_entry = value_list_entry, value_list_exit = value_list_exit)
    return render_template("formular2.html", form = form)

@app.route("/graf_I", methods = ["GET"])
def view2():
    return render_template("formular.html", form = MujFormular())

@app.route("/graf_I", methods = ["POST"])
def index2():
    form = MujFormular()
    operator = form.operator.data
    point= form.point.data
    direction= form.direction.data
    indicator = form.indicator.data
    iso_date_from = form.date_from.data
    iso_date_to = form.date_to.data

    date_from = iso_date_from.strftime("%d-%m-%Y")
    date_to = iso_date_to.strftime("%d-%m-%Y")
    
    url = f'https://transparency.entsog.eu/api/v1/operationaldatas?operatorKey={operator}&pointLabel={point}&indicator={indicator}&from={date_from}&to={date_to}&directionKey={direction}&limit=-1'
    
    r=requests.get(url).json()
        
    value_list = list()
    
    for x in r['operationaldatas']:
      hodnota = x['value']
      value_list.append(int(hodnota))

    if form.validate_on_submit():
        operator = form.operator.data
        point = form.point.data
        direction = form.direction.data
        date_from = form.date_from.data
        date_to = form.date_to.data
        vysledek = value_list
        return render_template("formular.html", vysledek = vysledek, form = form, value_list = value_list)
    return render_template("formular.html", form = form)
    
# Na adrese /plot zobrazí šablonu "plot.html", která obsahuje obrázek "plot.png"
@app.route("/plot", methods = ["GET"])
def plot():
    return render_template("plot.html")

# Když prohlížeč požádá o zobrazení obrázku plot.png, tak se zavolá tahle route,
# ve které my obrázek s grafem vygenerujeme
@app.route("/plot.png", methods = ["GET"])
def render_plot():
    # Vytvoří nový obrázek
    #fig = Figure()
    # Vytvoří v něm graf
    #axis = fig.add_subplot(1, 1, 1)
    # Vygeneruje náhodná data pro náš graf
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    # Nakreslí graf s těmito hodnotami
    #axis.plot(xs, ys)
    plt.plot(xs, ys)
    
    plt.fill_between(xs,ys, color = "skyblue", alpha = 0.4)
    #plt.show()
    # Převede graf na obrázek PNG a pošle ho zpátky prohlížeči
    output = io.BytesIO()
    #FigureCanvas(fig).print_png(output)
    plt.print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

