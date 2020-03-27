from models.models import Services_List
from models.models import Service
from models.models import Similar
from models.models import Details
from models.models import Logs
import requests
import labio
from bs4 import BeautifulSoup

labio.db.init()

svcs = Services_List.query.all()

# varre a tabela de serviços, acessa cada url para extrair informações
for item in svcs:
    response = requests.get(item.url)
    # utiliza o soup para encontrar no html as tags ondem ficam os tags e similares
    soup = BeautifulSoup(response.text, 'html.parser')

    # Popular a tabela de Serviços Similares ao Serviço
    similar_list = soup.find_all(class_='items')
    similar_num = 0 # esse número é para não adicionar o 1º, porque o primeiro item da lista é o nome do uploader
    similar_record = Similar()
    for similar in similar_list:
        similar_lis = similar.find_all('a')
        for similar_li in similar_lis:
            if similar_num > 0:
                similar_record = Similar()
                similar_record.service_id = item.id
                similar_record.name = similar_li.get_text()
                similar_record.merge()
            similar_num += 1
            detail = Details()
            detail.detail_id = detail.query.count()+1
            detail.detail_name = 'added service'+svc_record.name
            Similar.session.commit()
Similar.session.commit()