from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time
import csv
import os.path
import re

main_window_handle = None

input_district = "Hooghly"
input_year ="2019"

os.chdir("C:/Users/91961/Projects")
print(os.getcwd())
browser = webdriver.Chrome(executable_path="C:/Users/91961/Projects/chromedriver_win32/chromedriver.exe")
main_window_handle = browser.current_window_handle
type(browser)

districts_dict = {
    "Alipurduar":20,
    "Bankura":1,
    "Birbhum":3,
    "Burdwan":2,
    "Coochbehar":8,
    "Dakshin Dinajpur":17,
    "Darjeeling":4,
    "Hooghly":6,
    "Howrah":5,
    "Jalpaiguri":17,
    "Kalimpong":21,
    "Kolkata":19,
    "Malda":9,
    "Murshidabad":12,
    "Nadia":13,
    "North 24-Parganas":15,
    "Paschim Midnapore":10,
    "Purba Midnapore":11,
    "Purulia":14,
    "South 24-Parganas":16,
    "Uttar Dinajpur":18
}


url="https://wbregistration.gov.in/(S(3kx1wfhdeufypid5oiuiuu5p))/index/Search_By_Property_new.aspx?SearchingFrom=WS"
browser.get(url)

delay = 20 # seconds
try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'ctl00_CPH_txtCapcha')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")
    exit





district = Select(browser.find_element_by_css_selector("#ctl00_CPH_DDL_prop_district"))
district.select_by_visible_text(input_district)



time.sleep(5)


thana = Select(browser.find_element_by_css_selector("#ctl00_CPH_DDL_thana"))

thana_list = [o.text.replace(" ","") for o in thana.options]
print(thana_list)
thana_num=9
thana.select_by_visible_text(thana_list[thana_num])
input_thana = thana_list[thana_num]

filename = input_district+"_"+input_year+"_"+input_thana+"_"+str(thana_num)+".csv"   if(len(input_year)>0) else input_district+"_"+input_thana+"_"+str(thana_num)+".csv"
file_exists = os.path.isfile(filename) 



csv.register_dialect('kolkata_bot_format',quoting=csv.QUOTE_ALL)

f=open(filename,"a",newline='')
writer = csv.writer(f,dialect='kolkata_bot_format')
writer.writerow(["Property Location", "Property Type & Transaction", "Plot & Khatian No and Zone","Area of Property","Other Details","Party Details","SRO Code","Deed No","Year","Date of Registration"])




time.sleep(5)


form_year = browser.find_element_by_css_selector("#ctl00_CPH_txt_YearFrom")
form_year.clear()
form_year.send_keys(input_year)

time.sleep(5)

road =  browser.find_element_by_css_selector("#ctl00_CPH_chk_road")
road.click()

time.sleep(5)

captcha = browser.find_element_by_css_selector("#ctl00_CPH_txtCapcha")
user_captcha = input("Please enter the captcha: ")
captcha.send_keys(user_captcha)



display_button =  browser.find_element_by_css_selector("#ctl00_CPH_btn_SubmitQuery")
display_button.click()





try:
    myElem = WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, 'ctl00_CPH_GRV_SearchByProperty')))
    print("Tables have loaded!")
except TimeoutException:
    print("Loading took too much time!")
    exit

try:
    browser.find_element_by_css_selector("tr td table tbody tr").find_element_by_tag_name('td').find_element_by_tag_name('span')

except:
    browser.find_element_by_css_selector("tr td table tbody tr").find_element_by_tag_name('td').find_element_by_tag_name('a').click()
    time.sleep(5)  

flag_completion=0    

while 1:

    num_tr = len(browser.find_elements_by_css_selector("#ctl00_CPH_GRV_SearchByProperty>tbody>tr")) +1

    # #checking if header is part of thead or tbody
    # try:
    #     thead = browser.find_elements_by_css_selector("#ctl00_CPH_GRV_SearchByProperty>thead")
    #     start_position=0
    # except Exception:
    #     start_position=1
    # num_tr=9 

    for index_tr in [0,2,3,4,5,6,7,8]:

            #StaleElementReferenceException  to avoid this exception, reloading the driver webElement
            table = browser.find_element_by_css_selector("#ctl00_CPH_GRV_SearchByProperty>tbody")


            if(index_tr==num_tr-1):


                pagination = table.find_elements_by_tag_name('tr')[index_tr].find_element_by_css_selector('td table tbody tr')

                for count,pages in enumerate(pagination.find_elements_by_tag_name("td")):
                    
                    try:
                        pagenum = pages.find_element_by_tag_name("span").text
                        break
                    except Exception:
                        continue


                try:        
                    pagination.find_elements_by_tag_name("td")[count+1].find_element_by_tag_name("a").click()
                except Exception:
                    try:
                        pagination_link = pagination.find_elements_by_tag_name("td")[count+1].find_element_by_tag_name("a")
                        browser.execute_script("arguments[0].click();",pagination_link)
                    except Exception:
                        flag_completion=1 #all data downloaded
                        break

                time.sleep(10)
                break



            td = table.find_elements_by_tag_name('tr')[index_tr].find_elements_by_tag_name('td')
            property_location = td[0].text
            property_type_and_transaction = td[1].text
            plot_and_khatian_no_and_zone = td[2].text
            area_of_property = td[3].text
            other_details = td[4].text

            sro_code = re.match(r"Deed No: I-(\d{9})/",other_details)[1][0:4]        
            deed_no = re.match(r"Deed No: I-(\d{9})/",other_details)[1][4:]
            year_no = re.match(r"Deed No: I-\d{9}/(\d{4})",other_details)[1]
            date_of_registration = re.search(r"Date of Registration: (\d{2}.\d{2}.\d{4})",other_details)[1]

            attempt=1
            max_attempt=5

            while(attempt<=max_attempt):

                try:
                    view_party = td[5].find_element_by_tag_name("input").click()
                    break
                except Exception:
                    try:
                        view_party = td[5].find_element_by_tag_name("input")
                        browser.execute_script("arguments[0].click();",view_party)
                        break

                    except Exception:
                        attempt +=1


            time.sleep(5)
            #switch driver to clicked popup window
            popup_window_handle = None

            while not popup_window_handle:
                for handle in browser.window_handles:
                    if handle != main_window_handle:
                        popup_window_handle = handle
                        break

            browser.switch_to.window(popup_window_handle)
            table2 = browser.find_element_by_css_selector("#GRV_SearchByName tbody")

            count2=0
            party_details=""
            for tr2 in table2.find_elements_by_tag_name('tr'):
                if count2==0: 
                    count2 = count2+1
                    continue
                td2 = tr2.find_elements_by_tag_name('td')               
                name_and_address = td2[0].text
                status = td2[1].find_element_by_tag_name("span").text
                party_details = party_details + status + " " + name_and_address + " "

            browser.switch_to.window(main_window_handle)
            row =  [property_location, property_type_and_transaction, plot_and_khatian_no_and_zone,area_of_property,other_details,party_details,sro_code,deed_no,year_no,date_of_registration]   
            row =  [item.replace("\r","").replace("\n"," ") for item in row]
            writer.writerow(row)

    f.flush()
    os.fsync(f.fileno())
    print("Page no :",pagenum)
    if(flag_completion):
        break





print("done")


		

			


