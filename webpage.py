from models.models import Services_List
from models.models import Service
from models.models import Endpoint
from models.models import Tag
from models.models import Similar
from models.models import Details
from models.models import Logs
from models.models import Filters
import labio
from flask import Flask, render_template, url_for

app = Flask(__name__)
labio.db.init()

@app.route('/')
def index():
    logs = Logs.query.all()
    return render_template('index.html', logs=logs)

@app.route('/services')
def services():
    svcs = Service.query.all()
    return render_template('services.html', svcs=svcs)

@app.route('/endpoints')
def endpoints():
    endps = Endpoint.query.all()
    return render_template('endpoints.html', endps=endps)

@app.route('/details')
def details():
    dets = Details.query.all()
    return render_template('details.html', dets=dets)

@app.route('/filters')
def filters():
    fils = Filters.query.all()
    return render_template('filters.html', fils=fils)
    