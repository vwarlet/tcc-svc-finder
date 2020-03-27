from models.models import Endpoints_List
from models.models import Endpoint
from models.models import Details
from models.models import Logs
import requests, json, labio

labio.db.init()

end_record = Endpoint()
for end in Endpoints_List.query.all():
    response = requests.get(end.url+'.json')
    Endpoints = response.json()
    if 'rest_method' in Endpoints:
        Endpoints = Endpoints['rest_method']
    elif 'soap_operation' in Endpoints:
        Endpoints = Endpoints['soap_operation']
    else: print('erro! não possui métodos rest ou soap')
    end_record = Endpoint()
    end_record.id = end.id
    end_record.url = end.url
    end_record.name = Endpoints['name']
    if 'endpoint_label' in Endpoints:
        end_record.label = Endpoints['endpoint_label']
    else: 
        end_record.label = '-'
    end_record.description = Endpoints['description']   
    if end_record.description == None or end_record.description == '':
        end_record.description = 'No Description' 
    if 'utl_template' in Endpoints:
        end_record.template = Endpoints['url_template']
    else:
        end_record.template = '-'
    for inputs in Endpoints['inputs']:  
        end_record.parameters = inputs['name']
    end_record.service_id = end.service_id
    end_record.service_name = end.service_name
    end_record.merge()
    end_record.session.commit()
end_record.session.commit()