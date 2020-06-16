import requests
from bs4 import BeautifulSoup as BS
import time
import pandas as pd
import re



param = {
"ctl00$SM_Mast": "ctl00$CPH$UP_SearchCriteria|ctl00$CPH$GRV_SearchByProperty",
"ctl00$CPH$DDL_prop_district": 15,
"ctl00$CPH$DDL_thana": "05",
"ctl00$CPH$DDL_local_body": "3M",
"ctl00$CPH$txt_YearFrom": 2019,
"ctl00$CPH$DDListDistrict": 99,
"ctl00$CPH$chk_road": "on",
"ctl00$CPH$DDL_road": 000000,
"ctl00$CPH$txtCapcha": 53145,
"ctl00$CPH$DDL_Ro_District": 00,
"ctl00$CPH$DDLpropertytype": "A",
"ctl00$CPH$DDL_tran_maj": "04",
"ctl00$CPH$DDL_tran_min": 00,
"ctl00$CPH$rbl_date_type": "R",
"ctl00$CPH$txt_RegDate": "",
"ctl00$CPH$DDLMonth": 0,
"ctl00$CPH$txt_ward_no":"", 
"ctl00$CPH$txt_Premises":"", 
"ctl00$CPH$txt_LR_kht_no":"", 
"ctl00$CPH$txt_LR_kht_Bata":"", 
"__EVENTTARGET": "ctl00$CPH$GRV_SearchByProperty",
"__EVENTARGUMENT": "Page$1",
"__LASTFOCUS":"",
"__VIEWSTATE": "",
"__VIEWSTATEGENERATOR": "451C46D8",
"__VIEWSTATEENCRYPTED":"", 
"__ASYNCPOST": True,
}

headers = {
"Cookie": "regas_cookie=Regas_New2",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
"X-MicrosoftAjax": "Delta=True",
"X-Requested-With": "XMLHttpRequest"
}

url="https://wbregistration.gov.in/(S(whnfyw2o53220vc3k2r34aoz))/index/Search_By_Property_new.aspx?SearchingFrom=WS"

session = requests.Session()
page_num = 1
data_list=[]

#initialize view state
param['__VIEWSTATE']=''
param['ctl00$CPH$txtCapcha']=37434

while True:
    
  
    response = session.post(url, data=param,headers=headers)
    soup = BS(response.content,"lxml")
    viewstate = soup.find('input',id='__VIEWSTATE').attrs['value']
    table = soup.find('table', id='ctl00_CPH_GRV_SearchByProperty').tbody
    table_rows = table.find_all('tr')
    
    for row_item in table_rows:
        table_elems = row_item.find_all('td')
        for  item  in table_elems:
            data = item.text
            data = re.sub('\n','',data)
            data_list.append(data)
            
    page_num +=1
    param['__EVENTARGUMENT']=f'Page${page_num}'
    param['__VIEWSTATE']=viewstate       


data_list = [item for item in data_list if not (item.isnumeric() or item=="")]

