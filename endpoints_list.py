from models.models import Service
from models.models import Endpoints_List
from models.models import Details
from models.models import Logs
import requests, labio, re
import labio
import re    # para pegar apenas os números de uma url (id)
from bs4 import BeautifulSoup

labio.db.init()
end_record = Endpoints_List()
svcs = Service.query.all()

# varre a tabela de serviços e pega o id de cada serviço para acessar seus endpoints
for item in svcs:
    # os números da url representam o id do endpoint    
    id = item.entrypoint
    id = re.sub('[^0-9]', '', id)
    response = requests.get('https://www.biocatalogue.org/services/'+str(id)+'/service_endpoint')
    print(response.status_code)
    # utiliza o soup para encontrar no html a classe 'entry', onde ficam os endpoints
    soup = BeautifulSoup(response.text, 'html.parser')
    services_list = soup.find_all(class_='entry')
    print('serviço:',id,'-',item.name)
    for service in services_list:
        end_record = Endpoints_List()
        end_record.url = 'http://www.biocatalogue.org' + service.a.get('href')
        end_record.service_id = item.id
        end_record.service_name = item.name
        id_value = end_record.url
        end_record.id = re.sub('[^0-9]', '', id_value)
        end_record.merge()
        end_record.session.commit()
end_record.session.commit()