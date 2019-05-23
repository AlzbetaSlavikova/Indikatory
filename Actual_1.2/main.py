from flask import Flask, render_template, jsonify, Response, request
import requests
from flask_wtf import FlaskForm
from wtforms import SelectField, widgets, RadioField, DateField, SelectMultipleField
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
    operator = SelectField("Operátor", choices=[("SK-TSO-0001", "eustream"),("BE-TSO-0001", "Fluxys Belgium"),("DE-TSO-0001", "Gascade"),("AT-TSO-0001", "Gas Connect Austria"),("PL-TSO-0001", "Gaz-System"),("CZ-TSO-0001", "Moravia GS"),("CZ-TSO-0001", "NET4GAS"),("DE-TSO-0009" ,"Open Grid Europe"),("DE-TSO-0003", "ONTRAS"),("DE-TSO-0016", "OPAL"),("IT-TSO-0001", "Snam Rete Gas"),("AT-TSO-0003","TAG"),("UA-TSO-0001", "Ukrtransgaz"),("DE-TSO-0001","Gastransport")])
    point = SelectField("IP", choices=[("Baumgarten","Baumgarten"),("Brandov STEGAL (CZ) / Stegal (DE)","Brandov STEGAL"),("Brandov-OPAL (DE)","Brandov OPAL"),("Waidhaus" ,"Waidhaus"),("Lanžhot" ,"Lanžhot"),("Hora Svaté Kateřiny (CZ) / Deutschneudorf (Sayda) (DE)","HSK/Deutschendorf"),("Oberkappel (OGE)","Oberkappel"),("Olbernhau (DE) / Hora Svaté Kateřiny (CZ)","Olberhau/HSK"),("Kondratki","Kondratki"),("Mallnow","Mallnow"),("Tarvisio (IT) / Arnoldstein (AT)","Tarvisio/Arnoldstein"), ("Uzhgorod (UA) - Velké Kapušany (SK)","Užhorod/Velké Kapušany"),("VGS Moravia", "Moravia")])
    
    indicator = MultiCheckboxField("Indikátor", choices=[("Interruptible Available" ,"Interruptible Available Capacity"),("Interruptible Booked", "Interruptible Booked Capacity"),("Interruptible Total" ,"Interruptible Total Capacity"),("Firm Technical", "Firm Technical Capacity"),("Firm Booked", "Firm Booked Capacity"),("Firm Available", "Firm Available Capacity"),("Planned interruption of firm capacity", "Planned interruption of firm capacity"),("Unplanned interruption of firm capacity", "Unplanned interruption of firm capacity"),("Planned interruption of interruptible capacity", "Planned interruption of interruptible capacity"), ("Unplanned interruption of interruptible capacity", "Unplanned interruption of interruptible capacity")])
    date_from = DateField("Datum od", format='%Y-%m-%d')
    date_to = DateField("Datum do", format='%Y-%m-%d')

class IFormular(FlaskForm):
    operator = SelectField("Operátor", choices=[("SK-TSO-0001", "eustream"),("BE-TSO-0001", "Fluxys Belgium"),("DE-TSO-0001", "Gascade"),("AT-TSO-0001", "Gas Connect Austria"),("PL-TSO-0001", "Gaz-System"),("CZ-TSO-0001", "Moravia GS"),("CZ-TSO-0001", "NET4GAS"),("DE-TSO-0009" ,"Open Grid Europe"),("DE-TSO-0003", "ONTRAS"),("DE-TSO-0016", "OPAL"),("IT-TSO-0001", "Snam Rete Gas"),("AT-TSO-0003","TAG"),("UA-TSO-0001", "Ukrtransgaz")])
    point = SelectField("IP", choices=[("Baumgarten","Baumgarten"),("Brandov STEGAL (CZ) / Stegal (DE)","Brandov STEGAL"),("Brandov-OPAL (DE)","Brandov OPAL"),("Waidhaus" ,"Waidhaus"),("Lanžhot" ,"Lanžhot"),("Hora Svaté Kateřiny (CZ) / Deutschneudorf (Sayda) (DE)","HSK/Deutschendorf"),("Oberkappel (OGE)","Oberkappel"),("Olbernhau (DE) / Hora Svaté Kateřiny (CZ)","Olberhau/HSK"),("Kondratki","Kondratki"),("Mallnow","Mallnow"),("Tarvisio (IT) / Arnoldstein (AT)","Tarvisio/Arnoldstein"), ("Uzhgorod (UA) - Velké Kapušany (SK)","Užhorod/Velké Kapušany")])
    direction = SelectField("Entry/Exit", choices=[("Entry", "Entry"),("Exit", "Exit")])
    indicator = MultiCheckboxField("Indikátor", choices=[("Interruptible Available" ,"Interruptible Available Capacity"),("Interruptible Booked", "Interruptible Booked Capacity"),("Interruptible Total" ,"Interruptible Total Capacity"),("Firm Technical", "Firm Technical Capacity"),("Firm Booked", "Firm Booked Capacity"),("Firm Available", "Firm Available Capacity"),("Planned interruption of firm capacity", "Planned interruption of firm capacity"),("Unplanned interruption of firm capacity", "Unplanned interruption of firm capacity"),("Planned interruption of interruptible capacity", "Planned interruption of interruptible capacity"), ("Unplanned interruption of interruptible capacity", "Unplanned interruption of interruptible capacity")])
    indicator2 = SelectField("Indikátor2", choices=[("Firm Booked", "Firm Booked Capacity"),("","")])#pouze v případě, že by se indikátorům dávala zvlášť funkce!!
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
    
# Na adrese /plot zobrazí šablonu "plot.html", která obsahuje obrázek "plot.png"
@app.route("/plot", methods = ["GET"])
def plot():
    return render_template("plot.html")

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

    date_from = iso_date_from.strftime("%d-%m-%Y")
    date_to = iso_date_to.strftime("%d-%m-%Y")
    
    url_entry = f'https://transparency.entsog.eu/api/v1/operationaldatas?operatorKey={operator}&pointLabel={point}&indicator={indicator}&from={date_from}&to={date_to}&directionKey=entry&limit=-1'
    
    r_entry=requests.get(url_entry).json()
    
    url_exit = f'https://transparency.entsog.eu/api/v1/operationaldatas?operatorKey={operator}&pointLabel={point}&indicator={indicator}&from={date_from}&to={date_to}&directionKey=exit&limit=-1'
    
    r_exit=requests.get(url_exit).json()

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
# print(seznam_entry)


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
# print(seznam_exit)


# vytvoříme seznam všech datumů, které jsou v zadaném období, je možné použít pro oba API call
    
    start = iso_date_from
    end = iso_date_to

    delta = end - start

    datumy = []
    for i in range(delta.days + 1):
        dnes = start + timedelta(days=i)
        datumy.append(dnes)
#print(datumy)

# dohledá hodnotu pro každé datum v dané období - ENTRY
    hodnoty_entry = []

    for datum in datumy:
        for hodnota in seznam_entry:
            if datum >= hodnota['periodFrom'] and datum <= hodnota['periodTo']:
                hodnoty_entry.append(hodnota['value'])
                break #ukončí podmínku pokud je splněna a vrátí se na začátek

# print(hodnoty_entry)


# dohledá hodnotu pro každé datum v dané období - EXIT
    hodnoty_exit = []

    for datum in datumy:
        for hodnota in seznam_exit:
            if datum >= hodnota['periodFrom'] and datum <= hodnota['periodTo']:
                hodnoty_exit.append(hodnota['value'])
                break #ukončí podmínku pokud je splněna a vrátí se na začátek

    technical_capacity = []

    #for technical_capacity in technical_capacities:
    for hodnota in seznam_exit:
          if hodnota['operatorLabel'] == 'NET4GAS' and hodnota['pointLabel']== 'Waidhaus':
            technical_capacity.append('120000000')
            break


    return render_template('chart.html', data_rows = zip(datumy, hodnoty_entry, hodnoty_exit, technical_capacity))
 

@app.route("/plot.png", methods = ["GET"])
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
   
    for i in indicator:  
      url_1 = f'https://transparency.entsog.eu/api/v1/operationaldatas?operatorKey={operator}&pointLabel={point}&indicator={i}&from={date_from}&to={date_to}&directionKey={direction}&limit=-1'

      r_1=requests.get(url_1).json()
      print(indicator)

    #url_2 = f'https://transparency.entsog.eu/api/v1/operationaldatas?operatorKey={operator}&pointLabel={point}&indicator={indicator2}&from={date_from}&to={date_to}&directionKey={direction}&limit=-1'
    
    #r_2=requests.get(url_2).json()

      seznam_1 = []

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
        seznam_1.append(hodnoty)

  #  for index, req in enumerate(requests):
  #    method = req['method']
  #    path = req['path']
  #    body = req.get('body', None)

  #    with app.app_context(path, method=method, data = body):
   #     try:
    #      rv=app.preprocess_request()
     #     if rv is None:
      #      rv = app.dispatch_request() 
       # except Exception as e:
      #    rv = app. handle_user_exception(e)
       # response = app.make_response(rv)
    #    response = app.process_response(response)
    #  response.append({"status": response.status_code, "response": _read_response(response)})
   # return make_response(json.dumps(responses), 207, HEADERS)

      seznam_2 = []

      for x in r_2['operationaldatas']:
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
        seznam_2.append(hodnoty)

# vytvoříme seznam všech datumů, které jsou v zadaném období, je možné použít pro oba API call
    
      start = iso_date_from
      end = iso_date_to

      delta = end - start

      datumy = []
      for i in range(delta.days + 1):
        dnes = start + timedelta(days=i)
        datumy.append(dnes)

# dohledá hodnotu pro každé datum v dané období - ENTRY
      hodnoty_1 = []

      for datum in datumy:
        for hodnota in seznam_1:
            if datum >= hodnota['periodFrom'] and datum <= hodnota['periodTo']:
                hodnoty_1.append(hodnota['value'])
                break #ukončí podmínku pokud je splněna a vrátí se na začátek

    #print(hodnoty_1)


# dohledá hodnotu pro každé datum v dané období - EXIT
#      hodnoty_2 = []

#      for datum in datumy:
 #       for hodnota in seznam_2:
  #          if datum >= hodnota['periodFrom'] and datum <= hodnota['periodTo']:
   #             hodnoty_2.append(hodnota['value'])
    #            break #ukončí podmínku pokud je splněna a vrátí se na začátek

      return render_template('chart2.html', data_rows = zip(datumy, hodnoty_1))




    
