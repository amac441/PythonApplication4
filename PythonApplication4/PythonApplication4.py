import mechanize
import urllib2  #maybe python3
import urllib
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchAttributeException
from selenium.webdriver.common.keys import Keys
import threading
import os
import re
from bs4 import BeautifulSoup

id_att = []
issue_text = []

filename = raw_input("Name of file you want issues saved to ")
file = open(filename, 'w+')

stdate = raw_input("Enter Start Date (Format mm/dd/yyyy) ")
#print "you entered ", var

#open browser  - spoof it using mechanize
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_refresh(False)
br.addheaders = [('User-agent', 'Firefox')]

#instantiate selenium browser object
url1 = "https://login.incontact.com"
url2 = "https://home-c9.incontact.com/inContact/Support/AgentIssues/AgentIssueDashboard.aspx"
browser = webdriver.Firefox()
browser.get(url2)

#---- Login ------
#INPUT#ctl00_BaseContent_tbxUserName.textfield
username = raw_input("Enter Incontact Username ")
password = raw_input("Enter Incontact password ")
un = browser.find_element_by_name("ctl00$BaseContent$tbxUserName")
time.sleep(1)
un.send_keys(username)

#pw = browser.find_element_by_id("ctl00_BaseContent_tbxPassword.textfield").clear()
pw = browser.find_element_by_name("ctl00$BaseContent$tbxPassword")
time.sleep(1)
pw.send_keys(password + Keys.RETURN)


# ===== Threading =======

def get_url(issue, z):
    global file
    global issue_text
    details = 'https://home-c9.incontact.com/inContact/Support/AgentIssues/AgentIssueDetail.aspx?AgentIssueId=' + issue + '&issueTypeName='

    browser.get(details)
    #time.sleep(2)

    agent_num = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_ctl00_BaseContent_Content_BaseContent_lblAgentNr"]').text
    agent_name = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_ctl00_BaseContent_Content_BaseContent_lblLastName"]').text
    time = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_ctl00_BaseContent_Content_BaseContent_lblSubmitTime"]').text
    contact_id = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_ctl00_BaseContent_Content_BaseContent_lblContactId"]').text
    desc = browser.find_element_by_xpath('//*[@id="DescriptionRow"]/td[2]').text
    contact_url = 'https://home-c9.incontact.com/inContact/Manage/Reports/ContactDetail.aspx?contactid=' + contact_id

    #need to convert all to ascii
    file.write(issue_text[z] + '\t' +  agent_num + '\t' + agent_name.encode('ascii', 'ignore') + '\t' + time + '\t' + contact_id + '\t' + desc.encode('ascii', 'ignore') + '\t' + contact_url.encode('ascii', 'ignore') + '\n')


#----- AGENT ISSUES ------------

while True:
    try:
        time.sleep(4)
        #stdate = "12/1/2013"
        st = browser.find_element_by_id("ctl00_ctl00_ctl00_BaseContent_Content_BaseContent_agvsAgentIssues_tbxStartDate").clear()
        st = browser.find_element_by_id("ctl00_ctl00_ctl00_BaseContent_Content_BaseContent_agvsAgentIssues_tbxStartDate")
        st.send_keys(stdate + Keys.RETURN)

        time.sleep(2)
        el = browser.find_element_by_name("ctl00$ctl00$ctl00$BaseContent$Content$BaseContent$agvsAgentIssues$cmbPageSize")
        for option in el.find_elements_by_tag_name('option'):
            if option.text == '100':
                option.click() # select() in earlier versions of webdriver
        break

    except Exception:
            print "element exception"

# ====== FUNCTION =========

def grabHundred(y):

    global id_att
    
    while True:
        try: 
            for x in range(2, 10):
                #time.sleep(1)
                id = ""      
                xpath = '//*[@id="ctl00_ctl00_ctl00_BaseContent_Content_BaseContent_agvsAgentIssues_gridView_ctl0' + str(x) + '_hfAgentIssueId"]'
                id = browser.find_element_by_xpath(xpath)
                if id != "":
                    print x + y
                    id_att.append(id.get_attribute('value'))
                    issue = ""
                    xpath2 = '//*[@id="ctl00_ctl00_ctl00_BaseContent_Content_BaseContent_agvsAgentIssues_gridView"]/tbody/tr[' +str(x) + ']/td[3]'
                    issue = browser.find_element_by_xpath(xpath2).text
                    issue_text.append(issue)

            for x in range(10, 102):
                #time.sleep(1)
                id = ""
                xpath = '//*[@id="ctl00_ctl00_ctl00_BaseContent_Content_BaseContent_agvsAgentIssues_gridView_ctl' + str(x) + '_hfAgentIssueId"]'
                id = browser.find_element_by_xpath(xpath)

                if id != "":
                    print x + y
                    id_att.append(id.get_attribute('value'))
                    issue = ""
                    xpath2 = '//*[@id="ctl00_ctl00_ctl00_BaseContent_Content_BaseContent_agvsAgentIssues_gridView"]/tbody/tr[' +str(x) + ']/td[3]'
                    issue = browser.find_element_by_xpath(xpath2).text
                    if issue != "":
                        issue_text.append(issue)

            break

        except Exception:
            print "element exception"
            cont = raw_input("Should we continue (y/n)")
            if cont == "n":
                break

    return

# --------- EXECUTE CODE -----------

grabHundred(0)

#-----------------------

button = ""
button = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_ctl00_BaseContent_Content_BaseContent_agvsAgentIssues_GridFooter"]/table/tbody/tr/td[3]/div[1]/table/tbody/tr/td[7]/table/tbody/tr/td')
print(button.text)
if button.text == ' ':
    print("No Page 2")
else: 
    button.click()
    time.sleep(2)
    grabHundred(100)

button = ""
button = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_ctl00_BaseContent_Content_BaseContent_agvsAgentIssues_GridFooter"]/table/tbody/tr/td[3]/div[1]/table/tbody/tr/td[9]/table/tbody/tr/td')                                     
                                        
if button.text == ' ':
    print("No Page 3")
else:
    button.click()
    time.sleep(2)  
    grabHundred(200)

#---------------------

#button = ""
#button = browser.find_element_by_xpath('//*[@id="ctl00_ctl00_ctl00_BaseContent_Content_BaseContent_agvsAgentIssues_GridFooter"]/table/tbody/tr/td[3]/div[1]/table/tbody/tr/td[11]/table/tbody/tr/td')
#if not button:
#    print "nothing"
#else:
#    button.click()

#time.sleep(2)
#y=300
#for x in range(2, 10):
#        id = ""
#        xpath = '//*[@id="ctl00_ctl00_ctl00_basecontent_content_basecontent_agvsagentissues_gridview_ctl0' + str(x) + '_hfagentissueid"]'
#        id = browser.find_element_by_xpath(xpath)
#        print x + y
#        if not id:
#            print "nothing"
#        else:
#            id_att.append(id.get_attribute('value'))


# ====== PRINT THE FULL ID ARRAY ========

#print id_att
z = 0

for issue in id_att:
    #t = threading.Thread(target = get_url, args = (issue))
    #t.daemon = True
    #t.start()
    print issue
    get_url(issue, z)
    z = z + 1

file.close()

#=====  GRAB TEXT ======

#file = open('notes.txt', 'w+')
#htmlfile = urllib.urlopen(url1)
#htmltext = htmlfile.read()
#print htmltext
##print htmltext
#regex = "AgentIssueId=(.+?)&amp"
#pattern = re.compile(regex)
#issue_id = re.findall(pattern,htmltext)
#print issue_id

#the dropdown for page size
#"ctl00_ctl00_ctl00_BaseContent_Content_BaseContent_agvsAgentIssues_cmbPageSize"

#title of page 2
#"Go to Page 2"

#INPUT#ctl00_BaseContent_tbxPassword.textfield

# ==== CODE WONT WORK B/C INCONTACT IS USING AJAX ====

#need to scan this url and grab all agent issue IDs
#<tr class="gridRowWithHoverClass" onclickjavascript="window.location = 'AgentIssueDetail.aspx?AgentIssueId=39440&amp;issueTypeName=';" onclick="rowClicked(event, this); if (this.captureEvents) this.captureEvents(Event.CLICK);" onmouseover="" onmouseout="">

#file = open('notes.txt', 'w+')
#htmlfile = urllib.urlopen(url1)
#htmltext = htmlfile.read()
#print htmltext
##print htmltext
#regex = "AgentIssueId=(.+?)&amp"
#pattern = re.compile(regex)
#issue_id = re.findall(pattern,htmltext)
#print issue_id


#url2 = "https://home-c9.incontact.com/inContact/Support/AgentIssues/AgentIssueDetail.aspx?AgentIssueId=" + id + "&issueTypeName="
#htmltext =  urllib.urlopen(url)

##htmltext =  urllib.urlopen("http://www.fedsdatacenter.com/federal-pay-rates/output.php?n=&a=&l=&o=&y=&sEcho=20&iColumns=9&sColumns=&iDisplayStart=0&iDisplayLength=1000").read()

## reading the json response
## gives back an associative array (hashmap)  -  I need to give it a key

#i = 0

#while (i < 6000):
#    #3850768
#    start = str(i)
#    url = "http://www.fedsdatacenter.com/federal-pay-rates/output.php?n=&a=&l=&o=&y=&sEcho=20&iColumns=9&sColumns=&iDisplayStart=" + start + "&iDisplayLength=5000"
#    print url
#    htmltext =  urllib.urlopen(url)
#    data = json.load(htmltext)
#    jobs = data["aaData"]
#        for j = (0,5000):
            
#    file.write(str(jobs))
#    i = i + 5000

#jobs1 = jobs[1] #this gives you one row
#column2 = jobs1[3] #this gives you one column
#print jobs1
#print column2
#print data

#-------- tutorial on dealing with json -------
#http://similarsitesearch.com/api/similar/{url}
#htmltext = urllib.urlopen('http://similarsitesearch.com/api/similar/ebay.com').read()
#data = json.loads(htmltext)

#dat2 = [v for k, v in data.items() if type(v) == unicode and v != 'ok']

#people want to know what the fuck to study...
#kahn academy
#codeschool
#treehouse
#pluralsight
#cloudera
#udemy

