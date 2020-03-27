from models.models import Services_List
from models.models import Service
from models.models import Details
from models.models import Logs
import requests, json, labio

labio.db.init()

for svc in Services_List.query.all():
    response = requests.get(svc.url+'.json')
    services = response.json()
    services = services['service']
    svc_record = Service()
    svc_record.id = svc.id
    svc_record.entrypoint = svc.url
    svc_record.name = services['name']
    svc_record.description = services['description']   
    if svc_record.description == None or svc_record.description == '':
        svc_record.description = 'No Description' 
    for deployment in services['deployments']:  
        svc_record.base_url = deployment['endpoint']
    for variant in services['variants']:
        svc_record.doc_url = variant['documentation_url']
    svc_record.merge()
    svc_record.session.commit()
svc_record.session.commit()
