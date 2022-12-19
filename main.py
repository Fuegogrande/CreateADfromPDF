import fitz
import re
from datetime import date
import pyad

#Extract PDF Data and save to Variables
"""initials = input('What are your initials?')
today = date.today()
inputMode = input('Employee or Contractor (E or C)? ')
fileName = input('What is the filename? \n')
doc = fitz.open(fileName + '.pdf')
text = ""
line = 1
for page in doc:
    text+=page.get_text()
oneline = text.split('\n')

if inputMode.upper() == 'C':
    email = 0
    i = 27
    while email == 0:
        if oneline[i].find("@") > 0:
            email = i
        i +=1

    phoneNumber = 0
    x = 0
    pattern = re.compile('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')
    while phoneNumber == 0:
        testline = oneline[x]
        m = pattern.match(testline)
        if m:
            phoneNumber = x
        x +=1

    firstName = oneline[29]

    if phoneNumber - email == 4:
        UIN == oneline[email+1]
    else:
        UIN = None
 
    ADValues = {
        "First Name": oneline[29],
        "Last Name": oneline[30],
        "Username": firstName[0] + oneline[30],
        "Title": oneline[phoneNumber+1],
        "Description": oneline[phoneNumber+1] + ', ' + initials.upper() + ' ' +str(today),
        "Email": oneline[email],
        "Phone": oneline[phoneNumber],
        "UIN": UIN,
        "Department": oneline[phoneNumber+2]
    }
elif inputMode.upper() == 'E':
    i = 21
    while i < 33:
        i+=1

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
        "First Name": oneline[21],
        "Last Name": oneline[22],
        "Username": firstName[0] + oneline[22],
        "Title": oneline[phoneNumber + 5],
        "Description": oneline[phoneNumber + 5] + ', ' + initials.upper() + ' ' + str(today),
        "Email": oneline[email],
        "Phone": oneline[phoneNumber],
        "UIN": oneline[phoneNumber + 2],
        "Department": department
    }

for location in ADValues:
    print(ADValues[location])"""
