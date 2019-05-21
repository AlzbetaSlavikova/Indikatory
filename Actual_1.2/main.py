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
    operator = SelectField("Operátor", choices=[("SK-TSO-0001", "eustream"),("BE-TSO-0001", "Fluxys Belgium"),("DE-TSO-0001", "Gascade"),("AT-TSO-0001", "Gas Connect Austria"),("PL-TSO-0001", "Gaz-System"),("CZ-TSO-0001", "Moravia GS"),("CZ-TSO-0001", "NET4GAS"),("DE-TSO-0009" ,"Open Grid Europe"),("DE-TSO-0003", "ONTRAS"),("DE-TSO-0016", "OPAL"),("IT-TSO-0001", "Snam Rete Gas"),("AT-TSO-0003","TAG"),("UA-TSO-0001", "Ukrtransgaz")])
    point = SelectField("IP", choices=[("Baumgarten","Baumgarten"),("Brandov STEGAL (CZ) / Stegal (DE)","Brandov STEGAL"),("Brandov-OPAL (DE)","Brandov OPAL"),("Waidhaus" ,"Waidhaus"),("Lanžhot" ,"Lanžhot"),("Hora Svaté Kateřiny (CZ) / Deutschneudorf (Sayda) (DE)","HSK/Deutschendorf"),("Oberkappel (OGE)","Oberkappel"),("Olbernhau (DE) / Hora Svaté Kateřiny (CZ)","Olberhau/HSK"),("Kondratki","Kondratki"),("Mallnow","Mallnow"),("Tarvisio (IT) / Arnoldstein (AT)","Tarvisio/Arnoldstein"), ("Uzhgorod (UA) - Velké Kapušany (SK)","Užhorod/Velké Kapušany")])
    
    indicator = MultiCheckboxField("Indikátor", choices=[("Interruptible Available" ,"Interruptible Available Capacity"),("Interruptible Booked", "Interruptible Booked Capacity"),("Interruptible Total" ,"Interruptible Total Capacity"),("Firm Technical", "Firm Technical Capacity"),("Firm Booked", "Firm Booked Capacity"),("Firm Available", "Firm Available Capacity"),("Planned interruption of firm capacity", "Planned interruption of firm capacity"),("Unplanned interruption of firm capacity", "Unplanned interruption of firm capacity"),("Planned interruption of interruptible capacity", "Planned interruption of interruptible capacity"), ("Unplanned interruption of interruptible capacity", "Unplanned interruption of interruptible capacity")])
    date_from = DateField("Datum od", format='%Y-%m-%d')
    date_to = DateField("Datum do", format='%Y-%m-%d')

class IFormular(FlaskForm):
    operator = SelectField("Operátor", choices=[("SK-TSO-0001", "eustream"),("BE-TSO-0001", "Fluxys Belgium"),("DE-TSO-0001", "Gascade"),("AT-TSO-0001", "Gas Connect Austria"),("PL-TSO-0001", "Gaz-System"),("CZ-TSO-0001", "Moravia GS"),("CZ-TSO-0001", "NET4GAS"),("DE-TSO-0009" ,"Open Grid Europe"),("DE-TSO-0003", "ONTRAS"),("DE-TSO-0016", "OPAL"),("IT-TSO-0001", "Snam Rete Gas"),("AT-TSO-0003","TAG"),("UA-TSO-0001", "Ukrtransgaz")])
    point = SelectField("IP", choices=[("Baumgarten","Baumgarten"),("Brandov STEGAL (CZ) / Stegal (DE)","Brandov STEGAL"),("Brandov-OPAL (DE)","Brandov OPAL"),("Waidhaus" ,"Waidhaus"),("Lanžhot" ,"Lanžhot"),("Hora Svaté Kateřiny (CZ) / Deutschneudorf (Sayda) (DE)","HSK/Deutschendorf"),("Oberkappel (OGE)","Oberkappel"),("Olbernhau (DE) / Hora Svaté Kateřiny (CZ)","Olberhau/HSK"),("Kondratki","Kondratki"),("Mallnow","Mallnow"),("Tarvisio (IT) / Arnoldstein (AT)","Tarvisio/Arnoldstein"), ("Uzhgorod (UA) - Velké Kapušany (SK)","Užhorod/Velké Kapušany")])
    direction = SelectField("Entry/Exit", choices=[("Entry", "Entry"),("Exit", "Exit")])
    indicator = MultiCheckboxField("Indikátor", choices=[("Interruptible Available" ,"Interruptible Available Capacity"),("Interruptible Booked", "Interruptible Booked Capacity"),("Interruptible Total" ,"Interruptible Total Capacity"),("Firm Technical", "Firm Technical Capacity"),("Firm Booked", "Firm Booked Capacity"),("Firm Available", "Firm Available Capacity"),("Planned interruption of firm capacity", "Planned interruption of firm capacity"),("Unplanned interruption of firm capacity", "Unplanned interruption of firm capacity"),("Planned interruption of interruptible capacity", "Planned interruption of interruptible capacity"), ("Unplanned interruption of interruptible capacity", "Unplanned interruption of interruptible capacity")])
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

    return render_template('chart.html', data_rows = zip(datumy, hodnoty_entry, hodnoty_exit))
 # data to plot
    n_groups = len(datumy)
    values_entry = hodnoty_entry
    values_exit = [-value for value in hodnoty_exit]

     # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 1
    opacity = 0.8

    rects1 = plt.bar(index, values_entry, bar_width,
    alpha=opacity,
    color='b',
    label='ENTRY')

    rects2 = plt.bar(index, values_exit, bar_width,
    alpha=opacity,
    color='g',
    label='EXIT')

    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('IP Exit-Entry')
    plt.xticks(index + bar_width, datumy)
    plt.legend()

    plt.tight_layout()
    #plt.show()
    # Převede graf na obrázek PNG a pošle ho zpátky prohlížeči
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    #plt.print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route("/plot.png", methods = ["GET"])
def render_plot_I():
    # import pro graf I (druhý)
    operator = request.args.get("operator")
    point = request.args.get("point")
    direction = request.args.get("direction")
    indicator = request.args.get("indicator")
    #indicator2 = request.args.get("indicator2") - tohle byl pokus o navázání víc API, když jsem to ještě měla rozdělený podle jednotlivých indikátorů do různých funkcí
    #indicator3 = request.args.get("indicator3")
    #indicator4 = request.args.get("indicator4")
    #indicator5 = request.args.get("indicator5")
    #indicator6 = request.args.get("indicator6")
    #indicator7 = request.args.get("indicator7")
    #indicator8 = request.args.get("indicator8")
    #indicator9 = request.args.get("indicator9")
    #indicator10 = request.args.get("indicator10")
    iso_date_from = datetime.strptime(request.args.get("date_from"), "%Y-%m-%d").date()
    iso_date_to = datetime.strptime(request.args.get("date_to"), "%Y-%m-%d").date()

    date_from = iso_date_from.strftime("%d-%m-%Y")
    date_to = iso_date_to.strftime("%d-%m-%Y")
    #tohle měla být zkouška navázání dvou indikátorů na už existující graf (zaškrtla jsem oba indikátory, které měly vlastní funkci) a z nich se měly vygenerovat dvě API, podobně jako EXIT a ENTRY výše...ale stejně mi to nefungovalo. Pokusila jsem se přepsat všechny entry/exit do hodnot 1 a 2 na zkoušku, ale nevím, jestli jsem ten graf správně pochopila
    url_1 = f'https://transparency.entsog.eu/api/v1/operationaldatas?operatorKey={operator}&pointLabel={point}&indicator={indicator}&from={date_from}&to={date_to}&directionKey={direction}&limit=-1'
    
    r_1=requests.get(url_1).json()
    
    url_2 = f'https://transparency.entsog.eu/api/v1/operationaldatas?operatorKey={operator}&pointLabel={point}&indicator={indicator2}&from={date_from}&to={date_to}&directionKey={direction}&limit=-1'
    
    r_2=requests.get(url_2).json()

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

    print(hodnoty_1)


# dohledá hodnotu pro každé datum v dané období - EXIT
    hodnoty_2 = []

    for datum in datumy:
        for hodnota in seznam_2:
            if datum >= hodnota['periodFrom'] and datum <= hodnota['periodTo']:
                hodnoty_2.append(hodnota['value'])
                break #ukončí podmínku pokud je splněna a vrátí se na začátek

    return render_template('chart2.html', data_rows = zip(datumy, hodnoty_1, hodnoty_2))
    # data to plot
    n_groups = len(datumy)
    values_1 = hodnoty_1
    values_2 = hodnoty_2

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 1
    opacity = 0.8

    rects1 = plt.bar(index, values_1, bar_width,
    alpha=opacity,
    color='b',
    label='ENTRY')

    rects2 = plt.bar(index, values_2, bar_width,
    alpha=opacity,
    color='g',
    label='EXIT')

    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('IP Exit-Entry')
    plt.xticks(index + bar_width, datumy)
    plt.legend()

    plt.tight_layout()
    #plt.show()
    # Převede graf na obrázek PNG a pošle ho zpátky prohlížeči
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    #plt.print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
    
