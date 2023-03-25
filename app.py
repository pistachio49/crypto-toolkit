from flask import Flask,render_template,request

app=Flask(__name__)

def GCD(x,y):
    while y:
        (x, y) = (y,x%y)
    return x

def affinecipher(val):
    key1=23
    while(GCD(key1,26)!=1):
        print("Enter a valid multiplicative key")
        key1=23%26
    key2=21%26
    plain_text=val
    encryption_val={}
    ind=0
    while ind!=26:
        encryption_val[chr(97+ind)]=ind
        ind+=1
    #print(encryption_val)
    decryption_val={}
    ind=0
    while (ind!=26):
        decryption_val[ind]=chr(65+ind)
        ind+=1
    #print(decryption_val)
    cipher_text=""
    if GCD(key1,26)==1:
        for p in plain_text:
            cipher_text+=decryption_val[((encryption_val[p]*key1)+key2)%26]
    return cipher_text


@app.route("/")
@app.route("/homepage")
def homepage():
    return render_template("homepage.html")
@app.route("/encrypttext")
def encrypttext():
    return render_template("encryption.html")

@app.route("/decrypttext")
def decrypttext():
    return render_template("decryption.html")

@app.route("/cryptoanalysis")
def cryptoanalysis():
    return render_template("cryptoanalysis.html")

@app.route("/encrypt",methods=['GET','POST'])
def encrypt():
    output=request.form.to_dict()
    value=output["value"]
    d1=affinecipher(value)
    print(d1)
    return render_template("encryption.html",value=d1,inputvalue=value)

if __name__=='__main__':
    app.run(debug=True,port=5000)