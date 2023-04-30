from collections import Counter
from flask import Flask,render_template,request
from sympy import Matrix
import numpy as np
from math import ceil
from numpy import array
import itertools

def transcrypt1(value, keysize):
    # The ciphertext to be decrypted
    ciphertext = value.lower() #"EVLNAAETOFCRLTTUOOYMNEAGERTTDSYFEWSPYSH"
    block_size = int(keysize) #5

    # Calculate the number of rows required for the transposition matrix
    num_rows = ceil(len(ciphertext) / block_size)
    print(num_rows)

    # Create an empty transposition matrix
    transposition_matrix = [[''] * num_rows for _ in range(block_size)]

    # Fill the transposition matrix column-wise
    for i in range(block_size):
        for j in range(num_rows):
            if i*num_rows + j < len(ciphertext):
                transposition_matrix[i][j] = ciphertext[i*num_rows + j]

    column_indices = list(range(len(transposition_matrix[0])))

    # Generate all permutations of the column indices
    column_permutations = list(itertools.permutations(column_indices))

    # Generate all permutations of the matrix by rearranging the columns
    matrix_permutations = []
    for perm in column_permutations:
        matrix_permutation = [[row[i] for i in perm] for row in transposition_matrix]
        matrix_permutations.append(matrix_permutation)
        
    # Decrypt the ciphertext by reading the transposition matrix row-wise
    plaintext = []
    for matrix in matrix_permutations:
        ptext = ""
        for row in matrix:
            ptext += "".join(row)
        plaintext.append(ptext)

    # print("Decrypted plaintext:", plaintext)
    return plaintext
    
    

expected_frequencies = {
    'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253,
    'e': 0.12702, 'f': 0.02228, 'g': 0.02015, 'h': 0.06094,
    'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025,
    'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929,
    'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
    'u': 0.02758, 'v': 0.00978, 'w': 0.0236, 'x': 0.0015,
    'y': 0.01974, 'z': 0.00074
}

def frequency_analysis(ciphertext):
    """
    Perform frequency analysis on a ciphertext and return a substitution key
    """
    # count the frequency of each letter in the ciphertext
    freq = {}
    for letter in ciphertext:
        if letter.isalpha():
            if letter.lower() not in freq:
                freq[letter.lower()] = 1
            else:
                freq[letter.lower()] += 1
                
    # calculate the frequency distribution
    total = sum(freq.values())
    distribution = {}
    for letter in freq:
        distribution[letter] = freq[letter] / total
    
    # sort the letters by frequency
    sorted_letters = sorted(distribution, key=distribution.get, reverse=True)
    
    # create the substitution key
    key = {}
    for i in range(len(sorted_letters)):
        key[sorted_letters[i]] = list(expected_frequencies.keys())[i]
    
    return key

def decrypt(ciphertext, key):
    """
    Decrypt a ciphertext using a substitution key
    """
    plaintext = ''
    for letter in ciphertext:
        if letter.isalpha():
            if letter.isupper():
                plaintext += key[letter.lower()].upper()
            else:
                plaintext += key[letter]
        else:
            plaintext += letter
            
    return plaintext

def monocrypt1(ctext):
    ciphertext = "".join(ctext.split(" "))
    # ciphertext = ctext #"Uif mjtu pg bqqmf isphfdujpo jt tjdifs xpsme"
    # plaintext = ptext
    
    key = frequency_analysis(ciphertext)
    plaintext = decrypt(ciphertext, key)
    # print("key:", key)
    # print("Plaintext:", plaintext)
    original_dict = key
    key = {value: key for key, value in original_dict.items()}
    return {"plaintext":plaintext, "key":key}

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

def hillcrypt1(ctext,ptext,keysize):

# Define the ciphertext, plaintext, block length, and alphabet size
    ciphertext = ctext.upper() #'XETGL'
    plaintext = ptext.upper() #'HELLO'
    block_length = int(keysize) #2
    # print(ciphertext, plaintext, block_length)
    alphabet_size = 26

    # Convert the plaintext and ciphertext to matrices
    plaintext_matrix = np.zeros((block_length, len(plaintext)//block_length), dtype=int)
    ciphertext_matrix = np.zeros((block_length, len(ciphertext)//block_length), dtype=int)
    for i in range(len(plaintext)//block_length):
        for j in range(block_length):
            plaintext_matrix[j][i] = ord(plaintext[i*block_length+j]) - 65
            ciphertext_matrix[j][i] = ord(ciphertext[i*block_length+j]) - 65

    # Solve the system of linear equations to obtain the key matrix
    key_matrix = np.dot(ciphertext_matrix, np.linalg.inv(plaintext_matrix)) % alphabet_size

    # Verify the key matrix by checking if it is invertible modulo the alphabet size and if its determinant is relatively prime to the alphabet size
    key_det = int(np.round(np.linalg.det(key_matrix)))
    if np.gcd(key_det, alphabet_size) != 1 or np.linalg.det(key_matrix) == 0:
        print("Invalid key matrix!")
        return "invalid!"
    else:
        print(key_matrix)
        
        key = ""
        
        for row in key_matrix:
            for ch in row:
                key += chr(65 + (round(ch) % 26))
        print(key)
        return key

#     import numpy as np
# from collections import Counter

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

# def hillcrypt1(ciphertext, block_size):
#     alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#     ciphertext = ciphertext.upper()
#     alphabet_size = len(alphabet)
#     n = block_size
    
#     # Determine expected letter frequencies for the plaintext language
#     freqs = {'A': 0.0817, 'B': 0.0150, 'C': 0.0278, 'D': 0.0425, 'E': 0.1270, 
#              'F': 0.0223, 'G': 0.0202, 'H': 0.0609, 'I': 0.0697, 'J': 0.0015, 
#              'K': 0.0077, 'L': 0.0403, 'M': 0.0241, 'N': 0.0675, 'O': 0.0751, 
#              'P': 0.0193, 'Q': 0.0010, 'R': 0.0599, 'S': 0.0633, 'T': 0.0906, 
#              'U': 0.0276, 'V': 0.0098, 'W': 0.0236, 'X': 0.0015, 'Y': 0.0197, 'Z': 0.0007}
    
#     # Determine the ciphertext blocks and their corresponding plaintext blocks
#     ciphertext_blocks = [ciphertext[i:i+n] for i in range(0, len(ciphertext), n)]
#     plaintext_blocks = []
#     for block in ciphertext_blocks:
#         block_freqs = Counter(block)
#         block_freqs = {k: v/len(block) for k, v in block_freqs.items()}
#         diff_freqs = {k: abs(v - freqs[k]) for k, v in block_freqs.items() if k in freqs}
#         best_guess = ''.join([x[0] for x in sorted(diff_freqs.items(), key=lambda x: x[1])][:n])
#         plaintext_blocks.append(best_guess)
    
#     # Construct the equation system
#     A = []
#     B = []
#     for i in range(len(plaintext_blocks)):
#         a_row = []
#         for j in range(n):
#             a_row += [alphabet.index(plaintext_blocks[i][j])]
#         A.append(a_row)
#         b_row = []
#         for j in range(n):
#             b_row += [alphabet.index(ciphertext_blocks[i][j])]
#         B.append(b_row)
#     A = np.array(A)
#     B = np.array(B)
#     B = B.flatten()

#     # Solve the equation system
#     det = int(round(np.linalg.det(A))) % alphabet_size
#     if gcd(det, alphabet_size) != 1:
#         print('Error: key matrix is not invertible')
#         return None
#     inv_det = mod_inverse(det, alphabet_size)
#     adj = inv_det * np.round(np.linalg.inv(A) * det)
#     adj = adj % alphabet_size
#     key = adj.dot(B) % alphabet_size
    
#     # Decrypt the ciphertext using the found key
#     key = key.reshape(n, n)
#     return key
