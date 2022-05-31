from firebase_admin import credentials
from firebase_admin import db
import firebase_admin
from decrypt import *


#fetch the credentials from the JSON
login = credentials.Certificate(r'PATH FOR YOUR FIREBASE CREDENTIALS')

#initialize the database
firebase_admin.initialize_app(login, {
    'databaseURL': 'ANY DATABASE URL' #You can put the url for your firebase database
})

res0 = "yes"

def cmp(password):
    try:
        #splitting the string containing password and username into a list
        str2 = list(password.split(":"))

        #reading from the database
        ref = db.reference(f'/app/{str2[0]}')
        data = ref.get()

        #converting input and original password into bytes
        tmpinputpass = bytes(str2[1], 'ascii')
        tmpogpass = bytes(data['nfcPassword'], 'ascii')


        #key, original and input  password
        key = bytes(data['key'], 'ascii')
        ogpass = dcrypt(tmpogpass, key)
        inputpass = dcrypt(tmpinputpass, key)

        if inputpass == ogpass:
            return res0
    except:
        return None
