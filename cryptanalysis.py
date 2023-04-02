from collections import Counter
from flask import Flask,render_template,request
from sympy import Matrix
import numpy as np
from math import ceil
from numpy import array

def monocrypt1(ctext,ptext):
    plain_text=ptext.lower()
    cipher_text=ctext.upper()
    len1=len(plain_text)
    len2=len(cipher_text)
    if ((len1==len2) and (len2==26)):
        unsorted_keys={}
        ind=0
        for p in plain_text:
            unsorted_keys[p]=cipher_text[ind]
            ind+=1
        unsorted_keys=sorted(unsorted_keys.items())
        key={}
        for i,j in unsorted_keys:
            key[i]=j
        return key
    else:
        return "invalid!"

def shiftcrypt1(ctext):
    cipher_text=ctext.upper()
    list_plaintext=[]
    plain_key={}
    for i in range(26):
        plain_text=""
        for c in cipher_text:
            plain_text+=chr(((ord(c)%65-i)%26)+97)
        list_plaintext.append(plain_text)
        plain_key[plain_text]=i
    words_list=open('wordslist.txt','r').read().split('\n')
    l=len(cipher_text)
    possible_words=[]
    possible_plaintexts=[]
    for word in list_plaintext:
        for i in range(l):
            j=i+4 #length of word>3
            while j<l+1:
                substring=word[i:j].lower()
                if substring in words_list:
                    possible_words.append(substring)
                    possible_plaintexts.append(word)
                j+=1
    print(possible_plaintexts)
    count=Counter(possible_plaintexts)
    if(len(count)!=0):
        for key,times in count.most_common(5):
            print(key,"occurs",times,"times with key value",plain_key[key])
        return [count.most_common()[0][0],plain_key[count.most_common()[0][0]]]
    else:
        return "invalid!"

def affinecrypt1(ctext):
    cipher_text=ctext.upper()
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
    list_plaintext=[] # holds every possible plaintext values
    plain_keypairs={} # holds key pairs corresponding to every plaintext
    inverse={1:1,3:9,5:21,7:15,9:3,11:19,15:7,17:23,19:11,21:5,23:17,25:25}
    for key1 in inverse:
        for key2 in range(0,26):
            plain_text=""
            for c in cipher_text:
                plain_text+=decryption_val[((encryption_val[c.lower()]-key2)*(inverse[key1]))%26].lower()
            list_plaintext.append(plain_text)
            plain_keypairs[plain_text]=(key1,key2)
    #print(list_plaintext)
    words_list=open('wordslist.txt','r').read().split('\n')
    l=len(cipher_text)
    possible_words=[]
    possible_plaintexts=[]
    for word in list_plaintext:
        for i in range(l):
            j=i+4 #length of word>3
            while j<l+1:
                substring=word[i:j].lower()
                if substring in words_list:
                    possible_words.append(substring)
                    possible_plaintexts.append(word)
                j+=1
    count=Counter(possible_plaintexts)
    print(count.most_common())
    if(len(count)!=0):
        for key,times in count.most_common():
            print(key,"occurs",times,"times with key pair",plain_keypairs[key])
        print("most common string:",count.most_common()[0][0])
        print("key pair:", plain_keypairs[count.most_common()[0][0]])
        return [count.most_common()[0][0],plain_keypairs[count.most_common()[0][0]]]
    else:
        return "invalid!"

def hillcrypt1(ctext,ptext,keysize):
    try:
        plain_text=ptext.lower()
        cipher_text=ctext.upper()
        key_size=int(keysize)
        plain_text=plain_text[:key_size*key_size]
        cipher_text=cipher_text[:key_size*key_size]
        plain_matrix=[]
        row=[]
        for p in plain_text:
            row.append(ord(p)%97)
            if len(row)==key_size:
                plain_matrix.append(row)
                row=[]
        # print(array(plain_matrix))
        cipher_matrix=[]
        row=[]
        for c in cipher_text:
            row.append(ord(c)%65)
            if len(row)==key_size:
                cipher_matrix.append(row)
                row=[]
        # print(array(cipher_matrix))
        invplain_matrix=Matrix(plain_matrix).inv_mod(26)
        # print(array(invplain_matrix))
        key_matrix=(Matrix(invplain_matrix)*Matrix(cipher_matrix)%26)
        # print(array(key_matrix))
        key=""
        for k in list(key_matrix):
            key+=chr(65+k)
        return key
    except Exception as e:
        print(e)
        return "invalid!"