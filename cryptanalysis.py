from collections import Counter
from flask import Flask,render_template,request
from sympy import Matrix
import numpy as np
from math import ceil
from numpy import array

def monocrypt1(ctext,ptext):
    plain_text=ptext.lower().replace(" ","")
    cipher_text=ctext.upper().replace(" ","")
    len1=len(plain_text)
    len2=len(cipher_text)
    if ((len1==len2)):
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
    ctext=ctext.replace(" ","")
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
    words_list=open('wordslist.txt','r').read().split('\n')
    l=len(cipher_text)
    possible_words=[]
    possible_plaintexts=[]
    for word in list_plaintext:
        for i in range(l):
            j=i+2 #length of word>3
            while j<l+1:
                substring=word[i:j].lower()
                if substring in words_list:
                    possible_words.append(substring)
                    possible_plaintexts.append(word)
                j+=1
    count=Counter(possible_plaintexts)
    
    if(len(count)!=0):
        print(count.most_common())
        # most_time=count.most_common()[0][1]
        # print(most_time)
        for key,times in count.most_common():
            print(key,"occurs",times,"times with key pair",plain_keypairs[key])
            # if (times == most_time):
            #     print(key,"-->this")
        print("most common string:",count.most_common()[0][0])
        print("key pair:", plain_keypairs[count.most_common()[0][0]])
        # want to return all possible values which repeats 
        # same no.of times but maximum times
        return [count.most_common()[0][0],plain_keypairs[count.most_common()[0][0]]]
    else:
        return "invalid!"

# def hillcrypt1(ctext,ptext,keysize):
    # try:
    #     plain_text=ptext.lower().replace(" ","")
    #     cipher_text=ctext.upper()
    #     key_size=int(keysize)
    #     plain_text=plain_text[:key_size*key_size]
    #     cipher_text=cipher_text[:key_size*key_size]
    #     plain_matrix=[]
    #     row=[]
    #     for p in plain_text:
    #         row.append(ord(p)%97)
    #         if len(row)==key_size:
    #             plain_matrix.append(row)
    #             row=[]
    #     # print(array(plain_matrix))
    #     cipher_matrix=[]
    #     row=[]
    #     for c in cipher_text:
    #         row.append(ord(c)%65)
    #         if len(row)==key_size:
    #             cipher_matrix.append(row)
    #             row=[]
    #     # print(array(cipher_matrix))
    #     invplain_matrix=Matrix(plain_matrix).inv_mod(26)
    #     # print(array(invplain_matrix))
    #     key_matrix=(Matrix(invplain_matrix)*Matrix(cipher_matrix)%26)
    #     # print(array(key_matrix))
    #     key=""
    #     for k in list(key_matrix):
    #         key+=chr(65+k)
    #     return key
    # except Exception as e:
    #     print(e)
    #     return "invalid!"
import numpy as np
from collections import Counter

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return 1

def hillcrypt1(ciphertext, block_size):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ciphertext = ciphertext.upper()
    alphabet_size = len(alphabet)
    n = int(block_size)
    
    # Determine expected letter frequencies for the plaintext language
    freqs = {'A': 0.0817, 'B': 0.0150, 'C': 0.0278, 'D': 0.0425, 'E': 0.1270, 
             'F': 0.0223, 'G': 0.0202, 'H': 0.0609, 'I': 0.0697, 'J': 0.0015, 
             'K': 0.0077, 'L': 0.0403, 'M': 0.0241, 'N': 0.0675, 'O': 0.0751, 
             'P': 0.0193, 'Q': 0.0010, 'R': 0.0599, 'S': 0.0633, 'T': 0.0906, 
             'U': 0.0276, 'V': 0.0098, 'W': 0.0236, 'X': 0.0015, 'Y': 0.0197, 'Z': 0.0007}
    
    # Determine the ciphertext blocks and their corresponding plaintext blocks
    print(ciphertext)
    ciphertext_blocks = [ciphertext[i:i+n] for i in range(0, len(ciphertext), n)]
    plaintext_blocks = []
    for block in ciphertext_blocks:
        block_freqs = Counter(block)
        block_freqs = {k: v/len(block) for k, v in block_freqs.items()}
        diff_freqs = {k: abs(v - freqs[k]) for k, v in block_freqs.items() if k in freqs}
        best_guess = ''.join([x[0] for x in sorted(diff_freqs.items(), key=lambda x: x[1])][:n])
        plaintext_blocks.append(best_guess)
    
    # Construct the equation system
    A = []
    B = []
    for i in range(len(plaintext_blocks)):
        a_row = []
        for j in range(n):
            a_row += [alphabet.index(plaintext_blocks[i][j])]
        A.append(a_row)
        b_row = []
        for j in range(n):
            b_row += [alphabet.index(ciphertext_blocks[i][j])]
        B.append(b_row)
    A = np.array(A)
    B = np.array(B)
    B = B.flatten()

    # Solve the equation system
    det = int(round(np.linalg.det(A))) % alphabet_size
    if gcd(det, alphabet_size) != 1:
        print('Error: key matrix is not invertible')
        return None
    inv_det = mod_inverse(det, alphabet_size)
    adj = inv_det * np.round(np.linalg.inv(A) * det)
    adj = adj % alphabet_size
    key = adj.dot(B) % alphabet_size
    
    # Decrypt the ciphertext using the found key
    key = key.reshape(n, n)
    return key
