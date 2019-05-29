from flask import Flask, render_template, jsonify, Response, request
import requests
from flask_wtf import FlaskForm
from wtforms import SelectField, widgets, RadioField, DateField, SelectMultipleField, FieldList, FormField
from wtforms.fields.html5 import DateField
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import io
import numpy as np 
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

app = Flask(__name__)

app.config["SECRET_KEY"] = "super tajny klic"

class MultiCheckboxField(SelectMultipleField):
  widget= widgets.ListWidget(prefix_label=False)
  option_widget= widgets.CheckboxInput()

class EFormular(FlaskForm):
    operator = SelectField("Operátor", choices=[("SK-TSO-0001", "eustream"),("DE-TSO-0001", "Gascade"),("AT-TSO-0001", "Gas Connect Austria"),("PL-TSO-0001", "Gaz-System"),("CZ-TSO-0001", "NET4GAS"),("DE-TSO-0009" ,"Open Grid Europe"),("DE-TSO-0003", "ONTRAS"),("DE-TSO-0016", "OPAL"),("IT-TSO-0001", "Snam Rete Gas"),("AT-TSO-0003","TAG"),("UA-TSO-0001", "Ukrtransgaz"),("DE-TSO-0001","Gastransport")])
    point = SelectField("IP", choices=[("Baumgarten","Baumgarten"),("Brandov STEGAL (CZ) / Stegal (DE)","Brandov STEGAL"),("Brandov-OPAL (DE)","Brandov OPAL"),("Waidhaus" ,"Waidhaus"),("Lanžhot" ,"Lanžhot"),("Hora Svaté Kateřiny (CZ) / Deutschneudorf (Sayda) (DE)","HSK/Deutschendorf"),("Olbernhau (DE) / Hora Svaté Kateřiny (CZ)","Olberhau/HSK"),("Kondratki","Kondratki"),("Mallnow","Mallnow"),("Tarvisio (IT) / Arnoldstein (AT)","Tarvisio/Arnoldstein"), ("Uzhgorod (UA) - Velké Kapušany (SK)","Užhorod/Velké Kapušany"),("VGS Moravia", "Moravia"),("Cieszyn (PL) / Český Těšín (CZ)","Český Těšín")])
    indicator = MultiCheckboxField("Indikátor", choices=[("Interruptible Available" ,"Přerušitelná dostupná kapacita"),("Interruptible Booked", "Přerušitelná zasmluvněná kapacita"),("Interruptible Total" ,"Přerušitelná celková kapacita"),("Firm Technical", "Pevná technická kapacita"),("Firm Booked", "Pevná zasmluvněná kapacita"),("Firm Available", "Pevná dostupná kapacita"),("Planned interruption of firm capacity", "Plánované přerušení pevné kapacity"),("Unplanned interruption of firm capacity", "Neplánované přerušení pevné kapacity"),("Planned interruption of interruptible capacity", "Plánované přerušení přerušitelné kapacity"), ("Unplanned interruption of interruptible capacity", "Neplánované přerušení přerušitelné kapacity")])
    date_from = DateField("Datum od", format='%Y-%m-%d')
    date_to = DateField("Datum do", format='%Y-%m-%d')

class OperatorsForm(FlaskForm):
    operators = FieldList(FormField(EFormular), min_entries=1)

class IFormular(FlaskForm):
    operator = SelectField("Operátor", choices=[("SK-TSO-0001", "eustream"),("DE-TSO-0001", "Gascade"),("AT-TSO-0001", "Gas Connect Austria"),("PL-TSO-0001", "Gaz-System"),("CZ-TSO-0001", "NET4GAS"),("DE-TSO-0009" ,"Open Grid Europe"),("DE-TSO-0003", "ONTRAS"),("DE-TSO-0016", "OPAL"),("IT-TSO-0001", "Snam Rete Gas"),("AT-TSO-0003","TAG"),("UA-TSO-0001", "Ukrtransgaz")])
    point = SelectField("IP", choices=[("Baumgarten","Baumgarten"),("Brandov STEGAL (CZ) / Stegal (DE)","Brandov STEGAL"),("Brandov-OPAL (DE)","Brandov OPAL"),("Waidhaus" ,"Waidhaus"),("Lanžhot" ,"Lanžhot"),("Hora Svaté Kateřiny (CZ) / Deutschneudorf (Sayda) (DE)","HSK/Deutschendorf"),("Olbernhau (DE) / Hora Svaté Kateřiny (CZ)","Olberhau/HSK"),("Kondratki","Kondratki"),("Mallnow","Mallnow"),("Tarvisio (IT) / Arnoldstein (AT)","Tarvisio/Arnoldstein"), ("Uzhgorod (UA) - Velké Kapušany (SK)","Užhorod/Velké Kapušany"),("VGS Moravia", "Moravia"),("Cieszyn (PL) / Český Těšín (CZ)","Český Těšín")])
    direction = SelectField("Entry/Exit", choices=[("entry", "Entry"),("exit", "Exit")])
    indicator = MultiCheckboxField("Indikátor", choices=[("Interruptible Available" ,"Přerušitelná dostupná kapacita"),("Interruptible Booked", "Přerušitelná zasmluvněná kapacita"),("Interruptible Total" ,"Přerušitelná celková kapacita"),("Firm Technical", "Pevná technická kapacita"),("Firm Booked", "Pevná zasmluvněná kapacita"),("Firm Available", "Pevná dostupná kapacita"),("Planned interruption of firm capacity", "Plánované přerušení pevné kapacity"),("Unplanned interruption of firm capacity", "Neplánované přerušení pevné kapacity"),("Planned interruption of interruptible capacity", "Plánované přerušení přerušitelné kapacity"), ("Unplanned interruption of interruptible capacity", "Neplánované přerušení přerušitelné kapacity")])
    date_from = DateField("Datum od", format='%Y-%m-%d')
    date_to = DateField("Datum do", format='%Y-%m-%d')

@app.route("/", methods = ["GET"])
def view():

    return render_template("introduction.html")

@app.route("/graf_E", methods = ["GET"])
def view1():
    return render_template("formular1.html", form = EFormular())

@app.route("/graf_E", methods = ["POST"])
def index():
    form = EFormular()

    return render_template("formular1.html", form = form)

@app.route("/graf_I", methods = ["GET"])
def view2():
    return render_template("formular2.html", form = IFormular())

@app.route("/graf_I", methods = ["POST"])
def index2():
    form = IFormular()

    return render_template("formular2.html", form = form)

@app.route("/plot", methods = ["GET"])
def plot():
    return render_template("plot.html")  

@app.route("/plot2", methods = ["GET"])
def plot2():
    return render_template("plot2.html")
# Když prohlížeč požádá o zobrazení obrázku plot.png, tak se zavolá tahle route,
# ve které my obrázek s grafem vygenerujeme

@app.route("/plot.png", methods = ["GET"])
def render_plot():
    # import pro graf
    operator = request.args.get("operator")
    point = request.args.get("point")
    indicator = request.args.get("indicator")
    iso_date_from = datetime.strptime(request.args.get("date_from"), "%Y-%m-%d").date()
    iso_date_to = datetime.strptime(request.args.get("date_to"), "%Y-%m-%d").date()

    for x in operator:
      if operator == 'eustream':
        choices in point == ("Baumgarten","Baumgarten"),("Brandov STEGAL (CZ) / Stegal (DE)","Brandov STEGAL")

    date_from = iso_date_from.strftime("%d-%m-%Y")
    date_to = iso_date_to.strftime("%d-%m-%Y")
    
    url_entry = f'https://transparency.entsog.eu/api/v1/operationaldatas?operatorKey={operator}&pointLabel={point}&indicator={indicator}&from={date_from}&to={date_to}&directionKey=entry&limit=-1'
    
    response_1 = requests.get(url_entry)
    if response_1.status_code == 200: #pro případ, že API nevrátí žádnou hodnotu, resp. chybu - opakuje se níže
    
      r_entry = response_1.json()
      seznam_entry = []

      for x in r_entry['operationaldatas']:
        periodFrom = datetime.strptime(x['periodFrom'], '%Y-%m-%dT%H:%M:%S%z')
        periodFrom_new = periodFrom.date()
        periodTo = datetime.strptime(x['periodTo'], '%Y-%m-%dT%H:%M:%S%z')
        periodTo_new = periodTo.date()
        hodnoty = {
            "value": x['value'],
            "periodFrom": periodFrom_new,
            "periodTo": periodTo_new,
            "operatorLabel": x['operatorLabel'],
            "interruptionType": x['interruptionType'],
            "indicator": x['indicator'],
            "directionKey": x['directionKey'],
            "pointLabel": x['pointLabel'],
            "pointKey": x['pointKey']}
        seznam_entry.append(hodnoty)

    url_exit = f'https://transparency.entsog.eu/api/v1/operationaldatas?operatorKey={operator}&pointLabel={point}&indicator={indicator}&from={date_from}&to={date_to}&directionKey=exit&limit=-1'

    response_2 = requests.get(url_exit)  
    if response_2.status_code == 200:
            
      r_exit = response_2.json()
      seznam_exit = []

      for x in r_exit['operationaldatas']:
        periodFrom = datetime.strptime(x['periodFrom'], '%Y-%m-%dT%H:%M:%S%z')
        periodFrom_new = periodFrom.date()
        periodTo = datetime.strptime(x['periodTo'], '%Y-%m-%dT%H:%M:%S%z')
        periodTo_new = periodTo.date()
        hodnoty = {
            "value": x['value'],
            "periodFrom": periodFrom_new,
            "periodTo": periodTo_new,
            "operatorLabel": x['operatorLabel'],
            "interruptionType": x['interruptionType'],
            "indicator": x['indicator'],
            "directionKey": x['directionKey'],
            "pointLabel": x['pointLabel'],
            "pointKey": x['pointKey']
            }
        seznam_exit.append(hodnoty)

# vytvoříme seznam všech datumů, které jsou v zadaném období, je možné použít pro oba API call
    
    start = iso_date_from
    end = iso_date_to

    delta = end - start

    datumy = []
    for i in range(delta.days + 1):
      dnes = start + timedelta(days=i)
      datumy.append(dnes)

# dohledá hodnotu pro každé datum v daném období - ENTRY
    hodnoty_entry = []
    if response_1.status_code == 200:
      for datum in datumy:
        for hodnota in seznam_entry:
          if datum >= hodnota['periodFrom'] and datum <= hodnota['periodTo']:
              hodnoty_entry.append(hodnota['value'])
              break #ukončí podmínku pokud je splněna a vrátí se na začátek
    else:
      hodnoty_entry.append('0')

# dohledá hodnotu pro každé datum v dané období - EXIT
    hodnoty_exit = []
    if response_2.status_code == 200:
      for datum in datumy:
        for hodnota in seznam_exit:
          if datum >= hodnota['periodFrom'] and datum <= hodnota['periodTo']:
              hodnoty_exit.append(hodnota['value'])
              break #ukončí podmínku pokud je splněna a vrátí se na začátek
    else:
      hodnoty_exit.append('0')

  #seznam technických kapacit - pevné po celý rok  
    technical = [
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Lanžhot','directionKey':'entry','value':1640413000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Lanžhot','directionKey':'exit', 'value':-913680000},
      {'operatorKey':'SK-TSO-0001','pointLabel':'Lanžhot','directionKey':'entry','value':696800000},
      {'operatorKey':'SK-TSO-0001','pointLabel':'Lanžhot','directionKey':'exit','value':-400400000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Waidhaus','directionKey':'entry','value':120000000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Waidhaus','directionKey':'exit','value':-1071742000},
      {'operatorKey':'DE-TSO-0009','pointLabel':'Waidhaus','directionKey':'entry','value':906900000},
      {'operatorKey':'DE-TSO-0009','pointLabel':'Waidhaus','directionKey':'exit','value':0},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Olbernhau (DE) / Hora Svaté Kateřiny (CZ)','directionKey':'entry','value':367000000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Olbernhau (DE) / Hora Svaté Kateřiny (CZ)','directionKey':'exit','value':0},
      {'operatorKey':'DE-TSO-0001','pointLabel':'Olbernhau (DE) / Hora Svaté Kateřiny (CZ)','directionKey':'entry','value':367000000},
      {'operatorKey':'DE-TSO-0001','pointLabel':'Olbernhau (DE) / Hora Svaté Kateřiny (CZ)','directionKey':'exit','value':-325090000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Brandov STEGAL (CZ) / Stegal (DE)','directionKey':'entry','value':0},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Brandov STEGAL (CZ) / Stegal (DE)','directionKey':'exit','value':-290136000},
      {'operatorKey':'DE-TSO-0001','pointLabel':'Brandov STEGAL (CZ) / Stegal (DE)','directionKey':'entry','value':302670000},
      {'operatorKey':'DE-TSO-0001','pointLabel':'Brandov STEGAL (CZ) / Stegal (DE)','directionKey':'exit','value':0},
      {'operatorKey':'DE-TSO-0001','pointLabel':'Mallnow','directionKey':'entry','value':931500000},
      {'operatorKey':'DE-TSO-0001','pointLabel':'Mallnow','directionKey':'exit','value':0},
      {'operatorKey':'PL-TSO-0001','pointLabel':'Kondratki','directionKey':'entry','value':1024300000},
      {'operatorKey':'PL-TSO-0001','pointLabel':'Kondratki','directionKey':'exit','value':0},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Moravia','directionKey':'entry','value':53675000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Moravia','directionKey':'exit','value':-89270000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Cieszyn (PL) / Český Těšín (CZ)','directionKey':'entry','value':0},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Cieszyn (PL) / Český Těšín (CZ)','directionKey':'exit','value':-28052000},
      {'operatorKey':'PL-TSO-0001','pointLabel':'Cieszyn (PL) / Český Těšín (CZ)','directionKey':'entry','value':0},
      {'operatorKey':'PL-TSO-0001','pointLabel':'Cieszyn (PL) / Český Těšín (CZ)','directionKey':'exit','value':0},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Hora Svaté Kateřiny (CZ) / Deutschneudorf (Sayda) (DE)','directionKey':'entry','value':150900000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Hora Svaté Kateřiny (CZ) / Deutschneudorf (Sayda) (DE)','directionKey':'exit','value':-197530000},
      {'operatorKey':'DE-TSO-0003','pointLabel':'Hora Svaté Kateřiny (CZ) / Deutschneudorf (Sayda) (DE)','directionKey':'entry','value':197500000},
      {'operatorKey':'DE-TSO-0003','pointLabel':'Hora Svaté Kateřiny (CZ) / Deutschneudorf (Sayda) (DE)','directionKey':'exit','value':-135300000},
      {'operatorKey':'AT-TSO-0001','pointLabel':'Baumgarten','directionKey':'entry','value':477768000},
      {'operatorKey':'AT-TSO-0001','pointLabel':'Baumgarten','directionKey':'exit','value':-246528000},
      {'operatorKey':'SK-TSO-0001','pointLabel':'Baumgarten','directionKey':'entry','value':247520000},
      {'operatorKey':'SK-TSO-0001','pointLabel':'Baumgarten','directionKey':'exit','value':-1570400000},
      {'operatorKey':'AT-TSO-0003','pointLabel':'Baumgarten','directionKey':'entry','value':1436064000},
      {'operatorKey':'AT-TSO-0003','pointLabel':'Baumgarten','directionKey':'exit','value':0},
      {'operatorKey':'SK-TSO-0001','pointLabel':'Uzhgorod (UA) - Velké Kapušany (SK)','directionKey':'entry','value':2028000000},
      {'operatorKey':'SK-TSO-0001','pointLabel':'Uzhgorod (UA) - Velké Kapušany (SK)','directionKey':'exit','value':0},
      {'operatorKey':'UA-TSO-0001','pointLabel':'Uzhgorod (UA) - Velké Kapušany (SK)','directionKey':'entry','value':0},
      {'operatorKey':'UA-TSO-0001','pointLabel':'Uzhgorod (UA) - Velké Kapušany (SK)','directionKey':'exit','value':-2080000000},
      {'operatorKey':'IT-TSO-0001','pointLabel':'Tarvisio (IT) / Arnoldstein (AT)','directionKey':'entry','value':1158796000},
      {'operatorKey':'IT-TSO-0001','pointLabel':'Tarvisio (IT) / Arnoldstein (AT)','directionKey':'exit','value':0},
      {'operatorKey':'AT-TSO-0003','pointLabel':'Tarvisio (IT) / Arnoldstein (AT)','directionKey':'entry','value':0},
      {'operatorKey':'AT-TSO-0003','pointLabel':'Tarvisio (IT) / Arnoldstein (AT)','directionKey':'exit','value':-1200359000},
      {'operatorKey':'DE-TSO-0016','pointLabel':'Brandov-OPAL (DE)','directionKey':'entry','value':0},
      {'operatorKey':'DE-TSO-0016','pointLabel':'Brandov-OPAL (DE)','directionKey':'exit','value':-761498000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Brandov-OPAL (DE)','directionKey':'entry','value':1104838000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Brandov-OPAL (DE)','directionKey':'exit','value':0}
        ]      

    technical_capacity_exit = []
    for datum in datumy:
      for i in technical: 
        if i['operatorKey'] == operator and i['pointLabel'] == point and i['directionKey'] == 'exit':
            technical_capacity_exit.append(i['value'])
   
    technical_capacity_entry = []
    #if response_1.status_code == 200 or response_2.status_code == 200 or response_1.status_code == 404 or response_2.status_code == 404:
    for datum in datumy:
        for i in technical: 
          if i['operatorKey'] == operator and i['pointLabel'] == point and i['directionKey'] == 'entry':
            technical_capacity_entry.append(i['value'])

          

    return render_template('chart.html', data_rows = zip(datumy, hodnoty_entry, hodnoty_exit, technical_capacity_exit,  technical_capacity_entry))
 

@app.route("/plot2.png", methods = ["GET"])
def render_plot_I():
    # import pro graf I (druhý)
    operator = request.args.get("operator")
    point = request.args.get("point")
    direction = request.args.get("direction")
    indicator = request.args.get("indicator")

    iso_date_from = datetime.strptime(request.args.get("date_from"), "%Y-%m-%d").date()
    iso_date_to = datetime.strptime(request.args.get("date_to"), "%Y-%m-%d").date()

    date_from = iso_date_from.strftime("%d-%m-%Y")
    date_to = iso_date_to.strftime("%d-%m-%Y")
   
    #for i in indicator:  
    url_1 = f'https://transparency.entsog.eu/api/v1/operationaldatas?operatorKey={operator}&pointLabel={point}&indicator={indicator}&from={date_from}&to={date_to}&directionKey={direction}&limit=-1'

    r_1=requests.get(url_1).json()
      
    seznam = []

    for x in r_1['operationaldatas']:
        periodFrom = datetime.strptime(x['periodFrom'], '%Y-%m-%dT%H:%M:%S%z')
        periodFrom_new = periodFrom.date()
        periodTo = datetime.strptime(x['periodTo'], '%Y-%m-%dT%H:%M:%S%z')
        periodTo_new = periodTo.date()
        hodnoty = {
            "value": x['value'],
            "periodFrom": periodFrom_new,
            "periodTo": periodTo_new,
            "operatorLabel": x['operatorLabel'],
            "interruptionType": x['interruptionType'],
            "indicator": x['indicator'],
            "directionKey": x['directionKey'],
            "pointLabel": x['pointLabel'],
            "pointKey": x['pointKey']}
        seznam.append(hodnoty)

# vytvoříme seznam všech datumů, které jsou v zadaném období, je možné použít pro oba API call
    
    start = iso_date_from
    end = iso_date_to

    delta = end - start

    datumy = []
    for i in range(delta.days + 1):
      dnes = start + timedelta(days=i)
      datumy.append(dnes)

# dohledá hodnotu pro každé datum v dané období - ENTRY
    hodnoty = []
    if response_1.status_code == 200:
      for datum in datumy:
        for hodnota in seznam:
          if datum >= hodnota['periodFrom'] and datum <= hodnota['periodTo']:
                hodnoty.append(hodnota['value'])
                break #ukončí podmínku pokud je splněna a vrátí se na začátek
    else:
      hodnoty.append('0')

    #seznam technických kapacit - pevné po celý rok  
    technical = [
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Lanžhot','directionKey':'entry','value':1640413000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Lanžhot','directionKey':'exit', 'value':-913680000},
      {'operatorKey':'SK-TSO-0001','pointLabel':'Lanžhot','directionKey':'entry','value':696800000},
      {'operatorKey':'SK-TSO-0001','pointLabel':'Lanžhot','directionKey':'exit','value':-400400000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Waidhaus','directionKey':'entry','value':120000000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Waidhaus','directionKey':'exit','value':-1071742000},
      {'operatorKey':'DE-TSO-0009','pointLabel':'Waidhaus','directionKey':'entry','value':906900000},
      {'operatorKey':'DE-TSO-0009','pointLabel':'Waidhaus','directionKey':'exit','value':0},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Olbernhau (DE) / Hora Svaté Kateřiny (CZ)','directionKey':'entry','value':367000000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Olbernhau (DE) / Hora Svaté Kateřiny (CZ)','directionKey':'exit','value':0},
      {'operatorKey':'DE-TSO-0001','pointLabel':'Olbernhau (DE) / Hora Svaté Kateřiny (CZ)','directionKey':'entry','value':367000000},
      {'operatorKey':'DE-TSO-0001','pointLabel':'Olbernhau (DE) / Hora Svaté Kateřiny (CZ)','directionKey':'exit','value':-325090000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Brandov STEGAL (CZ) / Stegal (DE)','directionKey':'entry','value':0},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Brandov STEGAL (CZ) / Stegal (DE)','directionKey':'exit','value':-290136000},
      {'operatorKey':'DE-TSO-0001','pointLabel':'Brandov STEGAL (CZ) / Stegal (DE)','directionKey':'entry','value':302670000},
      {'operatorKey':'DE-TSO-0001','pointLabel':'Brandov STEGAL (CZ) / Stegal (DE)','directionKey':'exit','value':0},
      {'operatorKey':'DE-TSO-0001','pointLabel':'Mallnow','directionKey':'entry','value':931500000},
      {'operatorKey':'DE-TSO-0001','pointLabel':'Mallnow','directionKey':'exit','value':0},
      {'operatorKey':'PL-TSO-0001','pointLabel':'Kondratki','directionKey':'entry','value':1024300000},
      {'operatorKey':'PL-TSO-0001','pointLabel':'Kondratki','directionKey':'exit','value':0},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Moravia','directionKey':'entry','value':53675000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Moravia','directionKey':'exit','value':-89270000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Cieszyn (PL) / Český Těšín (CZ)','directionKey':'entry','value':0},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Cieszyn (PL) / Český Těšín (CZ)','directionKey':'exit','value':-28052000},
      {'operatorKey':'PL-TSO-0001','pointLabel':'Cieszyn (PL) / Český Těšín (CZ)','directionKey':'entry','value':0},
      {'operatorKey':'PL-TSO-0001','pointLabel':'Cieszyn (PL) / Český Těšín (CZ)','directionKey':'exit','value':0},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Hora Svaté Kateřiny (CZ) / Deutschneudorf (Sayda) (DE)','directionKey':'entry','value':150900000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Hora Svaté Kateřiny (CZ) / Deutschneudorf (Sayda) (DE)','directionKey':'exit','value':-197530000},
      {'operatorKey':'DE-TSO-0003','pointLabel':'Hora Svaté Kateřiny (CZ) / Deutschneudorf (Sayda) (DE)','directionKey':'entry','value':197500000},
      {'operatorKey':'DE-TSO-0003','pointLabel':'Hora Svaté Kateřiny (CZ) / Deutschneudorf (Sayda) (DE)','directionKey':'exit','value':-135300000},
      {'operatorKey':'AT-TSO-0001','pointLabel':'Baumgarten','directionKey':'entry','value':477768000},
      {'operatorKey':'AT-TSO-0001','pointLabel':'Baumgarten','directionKey':'exit','value':-246528000},
      {'operatorKey':'SK-TSO-0001','pointLabel':'Baumgarten','directionKey':'entry','value':247520000},
      {'operatorKey':'SK-TSO-0001','pointLabel':'Baumgarten','directionKey':'exit','value':-1570400000},
      {'operatorKey':'AT-TSO-0003','pointLabel':'Baumgarten','directionKey':'entry','value':1436064000},
      {'operatorKey':'AT-TSO-0003','pointLabel':'Baumgarten','directionKey':'exit','value':0},
      {'operatorKey':'SK-TSO-0001','pointLabel':'Uzhgorod (UA) - Velké Kapušany (SK)','directionKey':'entry','value':2028000000},
      {'operatorKey':'SK-TSO-0001','pointLabel':'Uzhgorod (UA) - Velké Kapušany (SK)','directionKey':'exit','value':0},
      {'operatorKey':'UA-TSO-0001','pointLabel':'Uzhgorod (UA) - Velké Kapušany (SK)','directionKey':'entry','value':0},
      {'operatorKey':'UA-TSO-0001','pointLabel':'Uzhgorod (UA) - Velké Kapušany (SK)','directionKey':'exit','value':-2080000000},
      {'operatorKey':'IT-TSO-0001','pointLabel':'Tarvisio (IT) / Arnoldstein (AT)','directionKey':'entry','value':1158796000},
      {'operatorKey':'IT-TSO-0001','pointLabel':'Tarvisio (IT) / Arnoldstein (AT)','directionKey':'exit','value':0},
      {'operatorKey':'AT-TSO-0003','pointLabel':'Tarvisio (IT) / Arnoldstein (AT)','directionKey':'entry','value':0},
      {'operatorKey':'AT-TSO-0003','pointLabel':'Tarvisio (IT) / Arnoldstein (AT)','directionKey':'exit','value':-1200359000},
      {'operatorKey':'DE-TSO-0016','pointLabel':'Brandov-OPAL (DE)','directionKey':'entry','value':0},
      {'operatorKey':'DE-TSO-0016','pointLabel':'Brandov-OPAL (DE)','directionKey':'exit','value':-761498000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Brandov-OPAL (DE)','directionKey':'entry','value':1104838000},
      {'operatorKey':'CZ-TSO-0001','pointLabel':'Brandov-OPAL (DE)','directionKey':'exit','value':0}
        ]       

    technical_capacity = []
    #if response_1.status_code == 200 or response_2.status_code == 200 or response_1.status_code == 404 or response_2.status_code == 404:
    for datum in datumy:
        for i in technical: 
          if i['operatorKey'] == operator and i['pointLabel'] == point and i['directionKey'] == direction:
            technical_capacity.append(i['value'])


    return render_template('chart2.html', data_rows = zip(datumy, hodnoty, technical_capacity))




    
