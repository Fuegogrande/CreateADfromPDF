import fitz
import re
from datetime import date
from pyad import *
import sys

# Extract PDF Data and save to Variables
loginName = input('What is your name, first and last? \n')
splitName = loginName.split()
loginFirst = splitName[0]
loginLast = splitName[1]
initials = loginFirst[0] + loginLast[0]
loginUsername = input('What is your login name (do not include -la)? ')
defaultUsername = loginUsername + '-la'
loginUsername2 = loginName + ' - la'
print(loginUsername2)
loginPassword = input('Password: ')

today = date.today()
inputMode = input('Employee or Contractor (E or C)? ')
fileName = input('What is the filename? \n')
numX = 0
while numX < input('How many accounts need to be added?'):
    try:
        doc = fitz.open('C:\\Users\\csimank\\Downloads' + fileName + '.pdf')
    except:
        doc = fitz.open('C:\\Users\\rmccallum\\Downloads' + fileName + '.pdf')
    text = ""
    line = 1
    for page in doc:
        text += page.get_text()
    oneline = text.split('\n')

    if inputMode.upper() == 'C':
        email = 0
        i = 27
        while email == 0:
            if oneline[i].find("@") > 0:
                email = i
            i += 1

        phoneNumber = 0
        x = 0
        pattern = re.compile('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')
        while phoneNumber == 0:
            testline = oneline[x]
            m = pattern.match(testline)
            if m:
                phoneNumber = x
            x += 1

        firstName = oneline[29]

        if phoneNumber - email == 4:
            UIN == oneline[email + 1]
        else:
            UIN = ""

        ADValues = {
            "givenName": oneline[29],
            "sn": oneline[30],
            "sAMAccountName": firstName[0] + oneline[30],
            "title": oneline[phoneNumber+1],
            "description": oneline[phoneNumber+1] + ', ' + initials.upper() + ' ' + str(today),
            "mail": oneline[email],
            "telephoneNumber": oneline[phoneNumber],
            "employeeID": UIN,
            "department": oneline[phoneNumber+2]
        }
    elif inputMode.upper() == 'E':
        i = 21
        while i < 33:
            i += 1

        email = 0
        i = 0
        while email == 0:
            if oneline[i].find("@") > 0:
                email = i
            i += 1

        phoneNumber = 0
        x = 0
        pattern = re.compile('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')
        while phoneNumber == 0:
            testline = oneline[x]
            m = pattern.match(testline)
            if m:
                phoneNumber = x
            x += 1
        firstName = oneline[21]
        if email == 24:
            department = oneline[23]
        elif email == 25:
            suffix = input('Is there a suffix (Y or N)? ')
            if suffix.upper() == 'Y':
                department = oneline[email - 2]
            else:
                department = oneline[email - 1]
        else:
            department = oneline[email - 2]
        ADValues = {
            "givenName": oneline[21],
            "sn": oneline[22],
            "sAMAccountName": firstName[0] + oneline[22],
            "title": oneline[phoneNumber + 5],
            "description": oneline[phoneNumber + 5] + ', ' + initials.upper() + ' ' + str(today),
            "mail": oneline[email],
            "telephoneNumber": oneline[phoneNumber],
            "employeeID": oneline[phoneNumber + 2],
            "department": department
        }

    for location in ADValues:
        print(ADValues[location])

    correct = input('Are the values correct (Y or N)? ')
    if correct.upper() != 'Y':
        sys.exit()

    pyad.set_defaults(ldap_server="AP-DC2.apogee.tamu.edu", username=defaultUsername, password=loginPassword)
    user = aduser.ADUser.from_cn(loginUsername2)
    print(user)

    ou = pyad.adcontainer.ADContainer.from_dn("OU=IT Service Desk,OU=IT Services,DC=apogee,DC=tamu,DC=edu")
    new_user = pyad.aduser.ADUser.create(ADValues['sAMAccountName'], ou, password="Temp1234!Temp1234!", upn_suffix=None, enable=True, optional_attributes={'employeeID':ADValues['employeeID'],'givenName':ADValues['givenName'],'sn':ADValues['sn'],'title':ADValues['title'],'description':ADValues['description'],'mail':ADValues['mail'],'telephoneNumber':ADValues['telephoneNumber'],'department':ADValues['department']})

    if ADValues['employeeID'] != "":
        new_user.set_attribute("employeeNumber", ADValues['employeeID'])

    numX+=1