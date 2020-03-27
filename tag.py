from models.models import Services_List
from models.models import Service
from models.models import Tag
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

    # Popular a tabela de Tags dos Serviços
    tag_list = soup.find_all(class_='tag_cloud')
    for tag in tag_list:
        tag_lis = tag.find_all('a')
        for tag_li in tag_lis:
            tag_record = Tag()
            tag_record.service_id = item.id
            tag_record.name = tag_li.get_text()
            tag_record.merge()
            detail = Details()
            detail.detail_id = detail.query.count()+1
            detail.detail_name = 'added service'+svc_record.name
            Tag.session.commit()   
Tag.session.commit()

