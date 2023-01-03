import fitz
import re
from datetime import date
from pyad import *
import os


def adusers():
    pyad.set_defaults(ldap_server="AP-DC2.apogee.tamu.edu", username=defaultUsername, password=loginPassword)
    user = aduser.ADUser.from_cn(loginUsername2)
    print(user)

    ou = pyad.adcontainer.ADContainer.from_dn("OU=IT Service Desk,OU=IT Services,DC=apogee,DC=tamu,DC=edu")
    print(ou)


    if ADValues['employeeID'] != "":
        new_user = pyad.aduser.ADUser.create(ADValues['sAMAccountName'], ou, password="Temp1234!Temp1234!",upn_suffix=None, enable=True,
        optional_attributes={'employeeID': ADValues['employeeID'], 'givenName': ADValues['givenName'], 'sn': ADValues['sn'], 'title': ADValues['title'],
        'description': ADValues['description'], 'mail': ADValues['mail'], 'telephoneNumber': ADValues['telephoneNumber'], 'department': ADValues['department'], 'employeeNumber': ADValues['employeeID']})
    else:
        new_user = pyad.aduser.ADUser.create(ADValues['sAMAccountName'], ou, password="Temp1234!Temp1234!", upn_suffix=None,enable=True, optional_attributes={'employeeID': ADValues['employeeID'],
        'givenName': ADValues['givenName'], 'sn': ADValues['sn'], 'title': ADValues['title'], 'description': ADValues['description'],
        'mail': ADValues['mail'], 'telephoneNumber': ADValues['telephoneNumber'], 'department': ADValues['department']})

# Extract PDF Data and save to Variables

with open('creds.txt') as credentials:
    lines = credentials.readlines()
print(lines)

loginName = lines[0]
loginName = loginName[:-1]
splitName = loginName.split()
loginFirst = splitName[0]
loginLast = splitName[1]
initials = loginFirst[0] + loginLast[0]
loginUsername = lines[1]
defaultUsername = loginUsername + '-la'
loginUsername2 = loginName
print(loginUsername2)
loginPassword = input('Password: ')

today = date.today()

numC = 0
numE = 0
numX = 0
fileList = []
filePath = 'C:\\Users\\' + loginUsername + '\\Downloads\\Accounts'
os.chdir(filePath)
print("Current working directory: {0}".format(os.getcwd()))

for f_name in os.listdir('C:\\Users\\' + loginUsername + '\\Downloads\\Accounts'):
    if f_name.startswith('Computer Access Request'):
            numC+=1
    elif f_name.startswith('UES - Pre'):
        numE+=1
    fileList.append(f_name)

numIterations = numC + numE
x = 0

for files in fileList:
    print(files)
    documents = os.path.join('C:\\Users\\' + loginUsername + '\\Downloads\\Accounts', files)
    print(documents)

    if files.startswith('Computer'):
        inputMode = 'C'
    else:
        inputMode = 'E'
    x += 1

    text = ""
    line = 1

    doc = fitz.open(files)
    for page in doc:
        text += page.get_text()
    oneline = text.split('\n')

    if inputMode.upper() == 'C':
        email = 0
        i = 27
        print('Contractor')
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
        print('Employee')
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
        print(email)
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
            "title": oneline[phoneNumber + 4],
            "description": oneline[phoneNumber + 4] + ', ' + initials.upper() + ' ' + str(today),
            "mail": oneline[email],
            "telephoneNumber": oneline[phoneNumber],
            "employeeID": oneline[phoneNumber + 2],
            "department": department
        }

    for location in ADValues:
        print(ADValues[location])
    print(ADValues)
    correct = input('Are the values correct (Y or N)? ')
    if correct.upper() == 'Y':
        adusers()
        doc.close()
        os.remove(files)

    numX += 1
