from flask import Flask,render_template,request
from sympy import Matrix
import numpy as np
from math import ceil
from numpy import array

app=Flask(__name__)

def GCD(x,y):
    while y:
        (x, y) = (y,x%y)
    return x

def affinecipher(val,k1,k2):
    key1=int(k1)
    val_org=val
    val=val.lower()
    val=val.replace(" ","")
    if(GCD(key1,26)!=1):
        return "invalid"
    key2=int(k2)
    plain_text=val
    encryption_val={}
    ind=0
    while ind!=26:
        encryption_val[chr(97+ind)]=ind
        ind+=1
    decryption_val={}
    ind=0
    while (ind!=26):
        decryption_val[ind]=chr(65+ind)
        ind+=1
    cipher_text=""
    if GCD(key1,26)==1:
        for p in plain_text:
            cipher_text+=decryption_val[((encryption_val[p]*key1)+key2)%26]
    cipher_text = list(cipher_text)
    for i in range(len(val_org)):
        if val_org[i]==" ":
            cipher_text.insert(i, " ")
        elif val_org[i].islower():
            cipher_text[i]=cipher_text[i].lower()
    cipher_text = ''.join(cipher_text)
    return cipher_text

def simplecipher(value1,key1):
    plain_text=value1.lower()
    key=key1.upper()
    cipher_text=""
    for p in plain_text:
        cipher_text+=key[ord(p)%97]
    return cipher_text

def vignerecipher(value1,key1):
    plain_text=value1.lower()
    key=key1.upper()
    cipher_text=""
    j=0
    for p in plain_text:
        cipher_text+=chr(65+(ord(p)%97-ord(key[j])%65)%26)
        j=(j+1)%len(key)
    return cipher_text

def shiftcipher(value1,key1):
    key=int(key1)
    plain_text=value1.lower()
    cipher_text=""
    for p in plain_text:
        cipher_text+=chr(((ord(p)%97+key)%26)+65)
    return cipher_text

def shiftcipherdec(value1,key1):
    key=int(key1)
    cipher_text=value1.upper()
    plain_text=""
    for c in cipher_text:
        plain_text+=chr(((ord(c)%65-key)%26)+97)
    return plain_text

def hillcipherenc(val,keysize,key1):
    plain_text=val.lower()
    key_size=int(keysize)
    key=key1.lower()
    count=0
    if(key_size**2!=len(key)):
        pass
    if (len(plain_text)%key_size!=0):
        count=key_size-len(plain_text)%key_size
    while(count):
        plain_text+=chr(123-count)
        count-=1
    plain_matrix=[]
    row=[]
    for p in plain_text:
        row.append(ord(p)%97)
        if len(row)==key_size:
            plain_matrix.append(row)
            row=[]
    row=[]
    key_matrix=[[0]*key_size for i in range(key_size)]
    k=0
    for i in range(key_size):
        for j in range(key_size):
            key_matrix[i][j]=ord(key[k])%97
            k=k+1
    cipher_matrix=((Matrix(plain_matrix)*Matrix(key_matrix).transpose())%26)
    cipher_text=""
    for c in list(cipher_matrix):
        cipher_text+=chr(65+c)
    return cipher_text

def railfencecipher(val):
    plain_text=val.lower()
    cipher_1=""
    cipher_2=""
    for i in range(len(plain_text)):
        if i%2==0:
            cipher_1+=plain_text[i].upper()
        else:
            cipher_2+=plain_text[i].upper()
    cipher_text=cipher_1+cipher_2
    return cipher_text

def keylesscipher(val,columnno):
    plain_text=val.lower()
    column=int(columnno)
    plain_text_list=[[-1]*column for i in range(int(ceil(len(plain_text)/(column))))]
    k=0
    for i in range(int(ceil(len(plain_text)/(column)))):
        for j in range(column):
            plain_text_list[i][j]=(plain_text[k])
            k=k+1
            if(k==len(plain_text)):
                break

    cipher_text=""
    for i in range(column):
        for j in range(ceil(len(plain_text)/column)):
            try :
                cipher_text+=(plain_text_list[j][i]).upper()
            except :
                continue
    return cipher_text

def permutationcipher(val,key):
    plain_text=val.lower()
    x=key
    key=[int(i) for i in x.split(" ")]
    count=0
#Addition of boguz characters
    if (len(plain_text)%len(key)!=0):
        count=len(key)-len(plain_text)%len(key)
    while(count):
        plain_text+=chr(123-count)
        count-=1
#print(plain_text)
    plain_text_list=[[-1]*len(key) for i in range(int(ceil(len(plain_text)/len(key))))]
    k=0
    for i in range(int(ceil(len(plain_text)/len(key)))):
        for j in range(len(key)):
            plain_text_list[i][j]=(plain_text[k])
            k=k+1
            if(k==len(plain_text)):
                break
#print(array(plain_text_list))
    cipher_text=""
    for i in range(ceil(len(plain_text)/len(key))):
        for j in range(len(key)):
            try :
                cipher_text+=(plain_text_list[i][key[j]-1]).upper()
            except :
                continue
    return cipher_text

def combinedapproachcipher(val,key):
    plain_text=val.lower()
    x=key
    key=[int(i) for i in x.split(" ")]
    count=0
    #Addition of boguz characters
    if (len(plain_text)%len(key)!=0):
        count=len(key)-len(plain_text)%len(key)
    while(count):
        plain_text+=chr(123-count)
        count-=1
    #print(plain_text)

    plain_text_list=[[-1]*(len(key)) for i in range(int(ceil(len(plain_text)/(len(key)))))]
    k=0
    for i in range(int(ceil(len(plain_text)/(len(key))))):
        for j in range(len(key)):
            plain_text_list[i][j]=(plain_text[k])
            k=k+1
            if(k==len(plain_text)):
                break
    #print(array(plain_text_list))

    plain_text_list2=[[-1]*(len(key)) for i in range(int(ceil(len(plain_text)/(len(key)))))]
    for i in range(int(ceil(len(plain_text)/(len(key))))):
        for k in range(len(key)):
            plain_text_list2[i][k]=plain_text_list[i][key[k]-1].upper()
    #print(array(plain_text_list2))

    cipher_text=""
    for i in range(len(key)):
        for j in range(ceil(len(plain_text)/(len(key)))):
            try :
                cipher_text+=(plain_text_list2[j][i]).upper()
            except :
                continue
    return cipher_text

@app.route("/")
@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/hill")
def hill():
    return render_template("hill.html")

@app.route("/transposition")
def transposition():
    return render_template("transposition.html")

@app.route("/encrypttext")
def encrypttext():
    return render_template("encselectpage.html")

@app.route("/shift")
def shift():
    return render_template("encryption.html")

@app.route("/affine")
def affine():
    return render_template("affine.html")

@app.route("/vig")
def vig():
    return render_template("vignere.html")

@app.route("/decrypttext")
def decrypttext():
    return render_template("decselectpage.html")

@app.route("/cryptoanalysis")
def cryptoanalysis():
    return render_template("cryptoanalysis.html")

@app.route("/encrypt",methods=['GET','POST'])
def encrypt():
    output=request.form.to_dict()
    value=output.get("value")
    key=output.get("key")
    key2=output.get("key2")
    keysize=output.get("keysize")
    ciphermethod=output.get("ciphermethod")
    a=0
    if(ciphermethod=="Shift cipher"):
        d1=shiftcipher(value,key)
        a=1
    elif(ciphermethod=="Caeser cipher"):
        d1=shiftcipher(value,3)
        a=1
    elif(ciphermethod=="Vignere cipher"):
        d1=vignerecipher(value,key)
        a=2
    elif(ciphermethod=="Monoalphabetic Substitution cipher"):
        d1=simplecipher(value,key)
        a=2
    elif(ciphermethod=="Affine cipher"):
        d1=affinecipher(value,key,key2)
        if(d1=="invalid"):
            return render_template("affine.html")
        else:
            return render_template("affine.html",value=d1,inputvalue=value,ciphermethod=ciphermethod)
    elif(ciphermethod=="Hill cipher"):
        d1=hillcipherenc(value,keysize,key)
        a=3
    elif(ciphermethod=="Rail fence cipher"):
        d1=railfencecipher(value)
        a=4
    elif(ciphermethod=="keyless transposition cipher with fixed number of columns"):
        d1=keylesscipher(value,key)
        a=4
    elif(ciphermethod=="Permutation transposition cipher"):
        d1=permutationcipher(value,key)
        a=4
    elif(ciphermethod=="Combined approach(key+keyless)"):
        d1=combinedapproachcipher(value,key)
        a=4
    else:
        d1="test1"
        a=1
    if(a==1):
        return render_template("encryption.html",value=d1,inputvalue=value,ciphermethod=ciphermethod)
    elif(a==2):
        return render_template("vignere.html",value=d1,inputvalue=value,ciphermethod=ciphermethod)
    elif(a==3):
        return render_template("hill.html",value=d1,inputvalue=value,ciphermethod=ciphermethod)
    elif(a==4):
        return render_template("transposition.html",value=d1,inputvalue=value,ciphermethod=ciphermethod)
@app.route("/shiftdec")
def shiftdec():
    return render_template("shiftdec.html")

@app.route("/decrypt",methods=['GET','POST'])
def decrypt():
    output=request.form.to_dict()
    value=output["value"]
    key=output["key"]
    ciphermethod=output["ciphermethod"]
    if(ciphermethod=="Shift cipher"):
        d1=shiftcipherdec(value,key)
    elif(ciphermethod=="Caeser cipher"):
        d1=shiftcipherdec(value,3)
    else:
        d1="test"
    return render_template("shiftdec.html",value=d1,inputvalue=value,ciphermethod=ciphermethod)

if __name__=='__main__':
    app.run(debug=True,port=5000)
