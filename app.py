from flask import Flask,render_template,request
from sympy import Matrix,Transpose
from flask_bootstrap import Bootstrap
import numpy as np
from math import ceil
from numpy import array
from cryptanalysis import *
from vigcryptanalysis import *
from validations import *

app=Flask(__name__)
bootstrap = Bootstrap(app)

def GCD(x,y):
    while y:
        (x, y) = (y,x%y)
    return x

def affinecipher(val,k1,k2):
    if(checkspace(val)==False):
        return "numerical!"
    key1=int(k1)%26
    val_org=val
    val=val.lower()
    val=val.replace(" ","")
    if(GCD(key1,26)!=1):
        return "invalid"
    key2=int(k2)%26
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
    if(checkspace(value1)==False):
        return "numerical!"
    plain_text=value1.lower().replace(" ","")
    key=key1.upper()
    cipher_text=""
    for p in plain_text:
        cipher_text+=key[ord(p)%97]
    cipher_text = list(cipher_text)
    for i in range(len(value1)):
        if value1[i]==" ":
            cipher_text.insert(i, " ")
        elif value1[i].islower():
            cipher_text[i]=cipher_text[i].lower()
    cipher_text = ''.join(cipher_text)
    return cipher_text

def vignerecipher(value1,key1):
    if(checkspace(value1)==False):
        return "numerical!"
    plain_text=value1.lower().replace(" ","")
    key=key1.upper().replace(" ","")
    cipher_text=""
    j=0
    for p in plain_text:
        cipher_text+=chr(65+(ord(p)%97+ord(key[j])%65)%26)
        j=(j+1)%len(key)
    cipher_text = list(cipher_text)
    for i in range(len(value1)):
        if value1[i]==" ":
            cipher_text.insert(i, " ")
        elif value1[i].islower():
            cipher_text[i]=cipher_text[i].lower()
    cipher_text = ''.join(cipher_text)
    return cipher_text

def shiftcipher(value1,key1):
    if(checkspace(value1)==False):
        return "numerical!"
    value1=value1.lower().replace(" ","")
    key=int(key1)
    plain_text=value1.lower()
    cipher_text=""
    for p in plain_text:
        cipher_text+=chr(((ord(p)%97+key)%26)+65)
    cipher_text = list(cipher_text)
    for i in range(len(value1)):
        if value1[i]==" ":
            cipher_text.insert(i, " ")
        elif value1[i].islower():
            cipher_text[i]=cipher_text[i].lower()
    cipher_text = ''.join(cipher_text)
    return cipher_text

def shiftcipherdec(value1,key1):
    if(checkspace(value1)==False):
        return "numerical!"
    key=int(key1)
    val_org=value1
    cipher_text=value1.upper().replace(" ","")
    plain_text=""
    for c in cipher_text:
        plain_text+=chr(((ord(c)%65-key)%26)+97)
    plain_text = list(plain_text)
    for i in range(len(val_org)):
        if val_org[i]==" ":
            plain_text.insert(i, " ")
        elif val_org[i].isupper():
            plain_text[i]=plain_text[i].upper()
    plain_text = ''.join(plain_text)
    return plain_text

def hillcipherenc(val,keysize,key1):
    if(checkspace(val)==False):
        return "numerical!"
    val_org=val
    val=val.replace(" ","")
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
    cipher_text = list(cipher_text)
    for i in range(len(val_org)):
        if val_org[i]==" ":
            cipher_text.insert(i, " ")
        elif val_org[i].islower():
            cipher_text[i]=cipher_text[i].lower()
    cipher_text = ''.join(cipher_text)
    return cipher_text

def railfencecipher(val):
    if(checkspace(val)==False):
        return "numerical!"
    plain_text=val.lower().replace(" ","")
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
    if(checkspace(val)==False):
        return "numerical!"
    plain_text=val.lower().replace(" ","")
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
    if(checkspace(val)==False):
        return "numerical!"
    plain_text=val.lower().replace(" ","")
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
    if(checkspace(val)==False):
        return "numerical!"
    plain_text=val.lower().replace(" ","")
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

def modularMultiplicativeInverse(x,y):
    for i in range(1,y):
        if ((x%y)*(i%y))%y ==1:
            return i


def affinedecryption(value,key11,key12):
    if(checkspace(value)==False):
        return "numerical!"
    key1=int(key11)%26
    val_org= value
    value=value.replace(" ","")
    while GCD(key1,26)!=1:
        return "invalid!"
    key2=int(key12)%26
    cipher_text=value.upper()
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
    plain_text=""
    key1_inverse= modularMultiplicativeInverse(key1,26)
    for c in cipher_text:
        plain_text+=decryption_val[((encryption_val[c.lower()]-key2)*(key1_inverse))%26].lower()
    plain_text = list(plain_text)
    print(value)
    for i in range(len(value)):
        if val_org[i]==" ":
            plain_text.insert(i, " ")
        elif val_org[i].isupper():
            plain_text[i]=plain_text[i].upper()
    plain_text = ''.join(plain_text)
    return plain_text

def monodecryption(value,key1):
    if(checkspace(value)==False):
        return "numerical!"
    cipher_text=value.upper().replace(" ","")
    key=key1.upper().replace(" ","")
    plain_text=""
    for c in cipher_text:
        plain_text+=chr(97+key.index(str(c)))
    plain_text = list(plain_text)
    for i in range(len(value)):
        if value[i]==" ":
            plain_text.insert(i, " ")
        elif value[i].isupper():
            plain_text[i]=plain_text[i].upper()
    plain_text = ''.join(plain_text)
    return plain_text

def vigdecryption(value,key1):
    if(checkspace(value)==False):
        return "numerical!"
    cipher_text=value.upper().replace(" ","")
    key=key1.upper().replace(" ","")
    plain_text=""
    j=0
    for c in cipher_text:
        plain_text+=chr(97+(ord(c)%65-ord(key[j])%65)%26)
        j=(j+1)%len(key)
    plain_text = list(plain_text)
    for i in range(len(value)):
        if value[i]==" ":
            plain_text.insert(i, " ")
        elif value[i].isupper():
            plain_text[i]=plain_text[i].upper()
    plain_text = ''.join(plain_text)
    return plain_text

def hilldecryption(value,keysize,key1):
    if(checkspace(value)==False):
        return "numerical!"
    val_org=value
    value=value.replace(" ","")
    cipher_text=value.upper()
    key_size=int(keysize)
    key=key1.lower()
    cipher_matrix=[]
    row=[]
    for c in cipher_text:
        row.append(ord(c)%65)
        if len(row)==key_size:
            cipher_matrix.append(row)
            row=[]
    key_matrix=[]
    row=[]
    for k in key:
        row.append(ord(k)%97)
        if len(row)==key_size:
            key_matrix.append(row)
            row=[]
    print(Matrix(key_matrix))
    invkey_matrix=Matrix(key_matrix).inv_mod(26)
    print(invkey_matrix)
    plain_matrix=((invkey_matrix*Transpose(Matrix(cipher_matrix)))%26)
    plain_text=""
    for p in list(plain_matrix):
        plain_text+=chr(p+97)
    plain_text = list(plain_text)
    for i in range(len(val_org)):
        if val_org[i]==" ":
            plain_text.insert(i, " ")
        elif val_org[i].isupper():
            plain_text[i]=plain_text[i].upper()
    plain_text = ''.join(plain_text)
    return plain_text

def railfencedec(value):
    if(checkspace(value)==False):
        return "numerical!"
    cipher_text=value.upper().replace(" ","")
    plain_1=""
    plain_2=""
    plain_text=""
    l=len(cipher_text)
    if(l%2==0):
        k=l//2
        plain_1=cipher_text[0:l//2].lower()
        plain_2=cipher_text[l//2:].lower()
    else:
        k=l//2+1
        plain_1=cipher_text[0:l//2+1].lower()
        plain_2=cipher_text[l//2+1:].lower()+" "
    for i in range(k):
        plain_text+=(plain_1[i]+plain_2[i])
    return plain_text

def keylesscipherdec(value,key1):
    if(checkspace(value)==False):
        return "numerical!"
    cipher_text=value.upper().replace(" ","")
    column=int(key1)
    cipher_text_list=[[-1]*column for i in range(int(ceil(len(cipher_text)/column)))]
    k=0
    for i in range(column):
        for j in range(ceil(len(cipher_text)/column)):
            cipher_text_list[j][i]=cipher_text[k]
            k=k+1
            if(k==len(cipher_text)):
                break
    plain_text=""
    k=0
    for i in range(int(ceil(len(cipher_text)/column))):
        for j in range(column):
            try:
                plain_text+=cipher_text_list[i][j].lower()
                k=k+1
            except:
                continue
    return plain_text

def permutationcipherdec(value,key1):
    if(checkspace(value)==False):
        return "numerical!"
    cipher_text=value.upper().replace(" ","")
    x=key1
    key=[int(i) for i in x.split(" ")]
    key_inverse=[-1]*len(key)
    for i in range(len(key)):
        key_inverse[key[i]-1]=i+1
    cipher_text_list=[[-1]*len(key) for i in range(int(ceil(len(cipher_text)/len(key))))]
    k=0
    for i in range(int(ceil(len(cipher_text)/len(key)))):
        for j in range(len(key)):
            cipher_text_list[i][j]=cipher_text[k]
            k=k+1
            if(k==len(cipher_text)):
                break
    plain_text=""
    k=0
    for i in range(int(ceil(len(cipher_text)/len(key)))):
        for j in range(len(key)):
            try:
                plain_text+=cipher_text_list[i][key_inverse[j]-1].lower()
                k=k+1
            except:
                continue
    return plain_text


def combinedapproachcipherdec(value,key1):
    if(checkspace(value)==False):
        return "numerical!"
    cipher_text=value.upper().replace(" ","")
    x=key1
    key=[int(i) for i in x.split(" ")]
    key_inverse=[-1]*len(key)
    for i in range(len(key)):
        key_inverse[key[i]-1]=i+1
    cipher_text_list2=[[-1]*len(key) for i in range(int(ceil(len(cipher_text)/len(key))))]
    k=0
    for i in range(len(key)):
        for j in range(int(ceil(len(cipher_text)/len(key)))):
            cipher_text_list2[j][i]=cipher_text[k]
            k+=1
            if k==len(cipher_text):
                break
    cipher_text_list=[[-1]*len(key) for i in range(int(ceil(len(cipher_text)/len(key))))]
    k=0
    for i in range(int(ceil(len(cipher_text)/len(key)))):
        for j in range(len(key)):
                cipher_text_list[i][j]=cipher_text_list2[i][key_inverse[j]-1].lower()
                k=k+1
    plain_text=""
    k=0
    for i in range(int(ceil(len(cipher_text)/len(key)))):
        for j in range(len(key)):
            try:
                plain_text+=cipher_text_list[i][j].lower()
                k=k+1
            except:
                continue
    return plain_text


@app.route("/")
@app.route("/homepage")
def homepage():
    return render_template("sample2.html")

@app.route("/caeserenc")
def caeserenc():
    return render_template("caeserenc.html")

@app.route("/caeserdec")
def caeserdec():
    return render_template("caeserdec.html")


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

@app.route("/monocrypt")
def monocrypt():
    return render_template("monocrypt.html")

@app.route("/vig")
def vig():
    return render_template("vignere.html")

@app.route("/decrypttext")
def decrypttext():
    return render_template("decselectpage.html")

@app.route("/cryptoanalysis")
def cryptoanalysis():
    return render_template("cryptoanalysis.html")

@app.route("/vigdec")
def vigdec():
    return render_template("vigdec.html")

@app.route("/monodec")
def monodec():
    return render_template("monodec.html")

@app.route("/monoenc")
def monoenc():
    return render_template("monoenc.html")

@app.route("/hilldec")
def hilldec():
    return render_template("hilldec.html")

@app.route("/transpositiondec")
def transpositiondec():
    return render_template("transpositiondec.html")

@app.route("/affinedec")
def affinedec():
    return render_template("affinedec.html")

@app.route("/cryptanalysis")
def cryptanalysis():
    return render_template("cryptanalysis.html")

@app.route("/vigcrypt")
def vigcrypt():
    return render_template("vigcrypt.html")

@app.route("/transpositioncrypt")
def transpositioncrypt():
    return render_template("transpositioncrypt.html")

@app.route("/shiftcrypt")
def shiftcrypt():
    return render_template("shiftcrypt.html")

@app.route("/affinecrypt")
def affinecrypt():
    return render_template("affinecrypt.html")

@app.route("/hillcrypt")
def hillcrypt():
    return render_template("hillcrypt.html")

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
        if(d1=="numerical!"):
            return render_template("encryption.html",err="Plain text should only consist of alphabets")
        a=1
    elif(ciphermethod=="Caeser cipher"):
        d1=shiftcipher(value,3)
        if(d1=="numerical!"):
            return render_template("caeserenc.html",err="Plain text should only consist of alphabets")
        a=10
    elif(ciphermethod=="Vigenere cipher"):
        if(key.isalpha()==False):
            return render_template("vignere.html",err="The Key should only consist of alphabets")
        d1=vignerecipher(value,key)
        if(d1=="numerical!"):
            return render_template("vignere.html",err="Plain text should only consist of alphabets")
        a=2
    elif(ciphermethod=="Monoalphabetic Substitution cipher"):
        if(monovalidation(key)==False):
            return render_template("monoenc.html",err="The Key must have 26 characters")
        d1=simplecipher(value,key)
        if(d1=="numerical!"):
            return render_template("monoenc.html",err="Plain text should only consist of alphabets")
        a=12
    elif(ciphermethod=="Affine cipher"):
        d1=affinecipher(value,key,key2)
        if(d1=="numerical!"):
            return render_template("affine.html",err="Plain text should only consist of alphabets")
        if(d1=="invalid"):
            return render_template("affine.html",err="Please enter a valid multiplicative key")
        else:
            return render_template("affine.html",value=d1,inputvalue=value,ciphermethod=ciphermethod)
    elif(ciphermethod=="Hill cipher"):
        d1=hillcipherenc(value,keysize,key)
        if(d1=="numerical!"):
            return render_template("hill.html",err="Plain text should only consist of alphabets")
        a=3
    elif(ciphermethod=="Rail fence cipher"):
        if(value.isalpha()==False):
            return render_template("transposition.html",err="The Plain Text must consist only of alphabets without spaces")
        d1=railfencecipher(value)
        a=4
    elif(ciphermethod=="keyless transposition cipher with fixed number of columns"):
        if(value.isalpha()==False):
            return render_template("transposition.html",err="The Plain Text must consist only of alphabets without spaces")
        d1=keylesscipher(value,key)
        a=4
    elif(ciphermethod=="Permutation transposition cipher"):
        if(value.isalpha()==False):
            return render_template("transposition.html",err="The Plain Text must consist only of alphabets without spaces")
        if(transpositionvalid(key,False,value)!="valid!"):
            p=transpositionvalid(key,False,value)
            return render_template("transposition.html",err=p)
        c=len(key)-1
        while(c!=-1):
            if(key[c]==' '):
                c=c-1
            else:
                break
        key=key[0:c+1]  
        d1=permutationcipher(value,key)
        a=4
    elif(ciphermethod=="Combined approach(key+keyless)"):
        if(value.isalpha()==False):
            return render_template("transposition.html",err="The Plain Text must consist only of alphabets without spaces")
        if(transpositionvalid(key,False,value)!="valid!"):
            p=transpositionvalid(key,False,value)
            return render_template("transposition.html",err=p)
        c=len(key)-1
        while(c!=-1):
            if(key[c]==' '):
                c=c-1
            else:
                break
        key=key[0:c+1]  
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
    elif(a==10):
        return render_template("caeserenc.html",value=d1,inputvalue=value,ciphermethod=ciphermethod)
    elif(a==12):
        return render_template("monoenc.html",value=d1,inputvalue=value,ciphermethod=ciphermethod)
    elif(a==4):
        return render_template("transposition.html",value=d1,inputvalue=value,ciphermethod=ciphermethod)

@app.route("/shiftdec")
def shiftdec():
    return render_template("shiftdec.html")

@app.route("/decrypt",methods=['GET','POST'])
def decrypt():
    output=request.form.to_dict()
    value=output.get("value")
    key=output.get("key")
    key2=output.get("key2")
    keysize=output.get("keysize")
    ciphermethod=output.get("ciphermethod")
    a=0
    if(ciphermethod=="Shift cipher"):
        d1=shiftcipherdec(value,key)
        if(d1=="numerical!"):
            return render_template("shiftdec.html",err="The Cipher Text must consist only of alphabets")
        a=1
    elif(ciphermethod=="Caeser cipher"):
        d1=shiftcipherdec(value,3)
        if(d1=="numerical!"):
            return render_template("caeserdec.html",err="The Cipher Text must consist only of alphabets")
        a=10
    elif(ciphermethod=="Vigenere cipher"):
        if(key.isalpha()==False):
            return render_template("vignere.html",err="The Key should only consist of alphabets")
        d1=vigdecryption(value,key)
        if(d1=="numerical!"):
            return render_template("vigdec.html",err="The Cipher Text must consist only of alphabets")
        a=2
    elif(ciphermethod=="Monoalphabetic Substitution cipher"):
        if(monovalidation(key)==False):
            return render_template("monodec.html",err="The key must have 26 characters")
        d1=monodecryption(value,key)
        if(d1=="numerical!"):
            return render_template("monodec.html",err="The Cipher Text must consist only of alphabets")
        a=3
    elif(ciphermethod=="Affine cipher"):
        d1=affinedecryption(value,key,key2)
        if(d1=="numerical!"):
            return render_template("affinedec.html",err="The Cipher Text must consist only of alphabets")
        if(d1=="invalid!"):
            return render_template("affinedec.html",err="Please enter a valid multiplicative key")
        else:
            return render_template("affinedec.html",value=d1,inputvalue=value,ciphermethod=ciphermethod)
    elif(ciphermethod=="Hill cipher"):
        d1=hilldecryption(value,keysize,key)
        if(d1=="numerical!"):
            return render_template("hilldec.html",err="The Cipher Text must consist only of alphabets")
        a=4
    elif(ciphermethod=="Rail fence cipher"):
        if(value.isalpha()==False):
            return render_template("transpositiondec.html",err="The Cipher Text must consist only of alphabets without spaces")
        d1=railfencedec(value)
        a=5
    elif(ciphermethod=="keyless transposition cipher with fixed number of columns"):
        if(value.isalpha()==False):
            return render_template("transpositiondec.html",err="The Cipher Text must consist only of alphabets without spaces")
        d1=keylesscipherdec(value,key)
        a=5
    elif(ciphermethod=="Permutation transposition cipher"):
        if(value.isalpha()==False):
            return render_template("transpositiondec.html",err="The Cipher Text must consist only of alphabets without spaces")
        if(transpositionvalid(key,True,value)!="valid!"):
            p=transpositionvalid(key,True,value)
            return render_template("transpositiondec.html",err=p)
        c=len(key)-1
        while(c!=-1):
            if(key[c]==' '):
                c=c-1
            else:
                break
        key=key[0:c+1]    
        d1=permutationcipherdec(value,key)
        a=5
    elif(ciphermethod=="Combined approach(key+keyless)"):
        if(value.isalpha()==False):
            return render_template("transpositiondec.html",err="The Cipher Text must consist only of alphabets without spaces")
        if(transpositionvalid(key,True,value)!="valid!"):
            p=transpositionvalid(key,True,value)
            return render_template("transpositiondec.html",err=p)
        c=len(key)-1
        while(c!=-1):
            if(key[c]==' '):
                c=c-1
            else:
                break
        key=key[0:c+1]  
        d1=combinedapproachcipherdec(value,key)
        a=5
    else:
        d1="test"
    if(a==1):
        return render_template("shiftdec.html",value=d1,inputvalue=value,ciphermethod=ciphermethod)
    elif(a==2):
        return render_template("vigdec.html",value=d1,inputvalue=value,ciphermethod=ciphermethod)
    elif(a==3):
        return render_template("monodec.html",value=d1,inputvalue=value,ciphermethod=ciphermethod) 
    elif(a==4):
        return render_template("hilldec.html",value=d1,inputvalue=value,ciphermethod=ciphermethod)
    elif(a==10):
        return render_template("caeserdec.html",value=d1,inputvalue=value,ciphermethod=ciphermethod)
    elif(a==5):
        return render_template("transpositiondec.html",value=d1,inputvalue=value,ciphermethod=ciphermethod)


@app.route("/crypt",methods=['GET','POST'])
def crypt():
    output=request.form.to_dict()
    value=output.get("value")
    key=output.get("key")   #plain_text
    key2=output.get("key2")
    keysize=output.get("keysize")
    ciphermethod=output.get("ciphermethod")
    a=0
    d1=""
    if(ciphermethod=="Monoalphabetic Substitution cipher"):
        if(value.isalpha()==False):
            return render_template("monocrypt.html",err="Cipher text must only consist of alphabets")
        if(key.isalpha()==False):
            return render_template("monocrypt.html",err="Plain text must only consist of alphabets")
        d1=monocrypt1(value,key)
        if(d1=="invalid!"):
            return render_template("monocrypt.html",err="Enter a valid input")
        else:
            return render_template("monocrypt.html",value=d1,inputvalue=value,ciphermethod=ciphermethod) 
    elif(ciphermethod=="Shift cipher"):
        if(value.isalpha()==False):
            return render_template("shiftcrypt.html",err="The Cipher Text must consist only of alphabets")
        d1=shiftcrypt1(value)
        return render_template("shiftcrypt.html",value=d1[0],key=d1[1]) 
    elif(ciphermethod=="Affine cipher"):
        if(value.isalpha()==False):
            return render_template("affinecrypt.html",err="The Cipher Text must consist only of alphabets")
        d1=affinecrypt1(value)
        if(d1!="invalid!"):
            return render_template("affinecrypt.html",value=d1[0],key=d1[1])
        else:
            return render_template("affinecrypt.html",err="valid word is not present in the used wordlist")
    elif(ciphermethod=="Hill cipher"):
        if(value.isalpha()==False):
            return render_template("vigcrypt.html",err="Cipher text must only consist of alphabets")
        d1=hillcrypt1(value,key,keysize)
        if(d1!="invalid!"):
            return render_template("hillcrypt.html",key=d1)
        else:
            return render_template("hillcrypt.html",err="valid word is not present in the used wordlist")
    elif(ciphermethod=="Vigenere cipher"):
        if(value.isalpha()==False):
            return render_template("vigcrypt.html",err="Cipher text must only consist of alphabets")
        d1=vigcrypt1(value)
        if(d1!="invalid!"):
            return render_template("vigcrypt.html",key=d1[0],ptext=d1[1])
        else:
            return render_template("vigcrypt.html",err="valid word is not present in the used wordlist")
    
if __name__=='__main__':
    app.run(debug=True,port=5000)