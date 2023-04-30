from collections import defaultdict,deque
import numpy as np
from math import ceil
import math
from collections import Counter

def kasiski(ciphertext):
    # Find repeated sequences of three or more letters in the ciphertext
    repeated_sequences = defaultdict(list)
    for i in range(len(ciphertext) - 2):
        seq = ciphertext[i:i+3]
        if seq in ciphertext[i+3:]:
            repeated_sequences[seq].append(i)

    # Calculate the distances between the occurrences of each repeated sequence
    distances = {}
    for seq, positions in repeated_sequences.items():
        distances[seq] = [positions[j+1] - positions[j] for j in range(len(positions)-1)]

    # Identify the factors of each distance and group them by distance
    factors = defaultdict(list)
    for seq, dists in distances.items():
        for d in dists:
            for i in range(2, int(d**0.5)+1):
                if d % i == 0:
                    factors[d].extend([i, d//i])
            factors[d] = list(set(factors[d]))

    # Choose the most likely length based on the frequency of its factors
    likely_lengths = []
    for dist, factors_list in factors.items():
        for f in factors_list:
            if f > 2:
                length = dist // f
                if length > 2 and length not in likely_lengths:
                    likely_lengths.append(length)
    return likely_lengths


# def decrypt_vigenere(ciphertext, keyword):
#     plaintext = ''
#     keyword_len = len(keyword)
#     for i in range(len(ciphertext)):
#         shift = ord(keyword[i % keyword_len]) - 65
#         cipher_char = ciphertext[i]
#         if cipher_char.isalpha():
#             plaintext += chr((ord(cipher_char) - shift - 65) % 26 + 65)
#         else:
#             plaintext += cipher_char
#     return plaintext


# def vigcrypt1(ciphertext):
#     # Determine the length of the keyword using the Kasiski test
#     ciphertext = ciphertext.replace(" ","")
#     likely_lengths = kasiski(ciphertext)
#     print("Likely keyword lengths:", likely_lengths)

#     # Divide the ciphertext into segments
#     segments = []
#     for i in range(min(likely_lengths), len(ciphertext)):
#         if i in likely_lengths:
#             segments.append([ciphertext[j] for j in range(0, len(ciphertext), i)])
    
#     # Perform frequency analysis on each segment
#     keyword = ''
#     for segment in segments:
#         # Calculate the frequency of each letter in the segment
#         freq = Counter(segment)
#         most_common = freq.most_common(5)
        
#         # Calculate the shift value for the most common letter (assuming it's 'E')
#         shift = (ord(most_common[0][0]) - 69) % 26
#         keyword += chr(shift + 65)
    
#     # Determine the keyword
#     # print("Possible keywords:", keyword)

#     # Decrypt the ciphertext using the keyword
#     plaintext = decrypt_vigenere(ciphertext, keyword)
#     print(keyword)
#     return [1, plaintext]



# def kasiski(cipher_text,size=3):
#     possible_seq=defaultdict(list)
#     repeating_seq={}
#     pos=0
#     while(pos+size<=len(cipher_text)):
#         substr=cipher_text[pos:pos+size]
#         ind = [i for i in range(len(cipher_text)) if cipher_text.startswith(substr, i)]
#         possible_seq[substr]=ind
#         pos+=1
#     for key,val in possible_seq.items():
#         if len(val)>1:
#             repeating_seq[key]=val
#     #print(repeating_seq)
#     sd={}
#     j=""
#     initial=""
#     for i,val in repeating_seq.items() :
#         if j=="":
#             initial=i
#             j=i
#         elif count==val:
#             j+=i[-1]
#         else :
#             sd[j]=repeating_seq[initial]
#             j=i
#             initial=i
#         count=[x+1 for x in val]
#     sd[j]=repeating_seq[initial]
#     #print(sd)
#     diff=[]
#     for key,val in sd.items():
#         j=0
#         while(j+1<len(val)):
#             diff.append(val[j+1]-val[j])
#             j+=1
#     return diff
    #possible_gcd=[]

def divisors(n):
    ret =[]
    for i in range(1,math.ceil(math.sqrt(n))+1):
        if n%i== 0:
            if i>2: #since we consider key of length >=3 in kasiski method
                ret.append(i)
            if (i!=int(n/i)):
                ret.append(int(n/i))
    return ret

def frequency_calculator(word):
    frequency = { "a" : 0,  "b" : 0,  "c" : 0,  "d" : 0,  "e" : 0, "f" : 0,  "g" : 0,
        "h" : 0,  "i" : 0,  "j" : 0,  "k" : 0,  "l" : 0,  "m" : 0,  "n" : 0,  "o" :   0,
        "p" : 0,  "q" : 0,  "r" : 0,  "s" : 0,  "t" : 0,  "u" : 0,  "v" : 0,  "w" : 0,
        "x" : 0,  "y" : 0,  "z" : 0 }
    for letter in word:
        frequency[letter]+= 1
    for i in frequency:
        frequency[i]=frequency[i]/len(word)*100
    return frequency

def product_value(actual_freq,stand_freq):
    f1=deque(actual_freq.values())
    f2=list(stand_freq.values())
    sum_array=[]
    for _ in range (len(f2)):
        sum1=0
        for i in range(len(f2)):
            sum1+=f1[i]*f2[i]*100
        sum_array.append(sum1)
        f1.rotate(-1)
    keychar=max(sum_array)
    return chr(sum_array.index(keychar)+97)

def vigcrypt1(ctext):
    cipher_text=ctext
    s= kasiski(cipher_text)
    divisors_list=[]
    for i in s:
        divisors_list.extend(divisors(i))
    possible_gcd=Counter(divisors_list)
    key_length=2
    v=0
    for key,val in possible_gcd.most_common():
        if key>key_length and v<=val:
            key_length= key
            v=val
    print(key_length)
    print(possible_gcd)
    count=0
    for x,y in possible_gcd.most_common(4):
        key_length=x
        print("Key length: ",x)
        count+=1
        collect={}
        #print(collect)
        for i in range(len(cipher_text)):
            if (i%key_length not in collect):
                collect[i%key_length]=[]
            collect[i%key_length].append(cipher_text[i])
        string_set={}
        for i in range(key_length):
            string_set[i]="".join(collect[i]).lower()
        #print(string_set)
        freq_set={}
        for key,val in string_set.items():
            freq_set[key]=frequency_calculator(val)
        #print(freq_set)
        keyset=[]
        stand_freq={'A':8.2,'B':1.5,'C':2.8,'D':4.3,'E':12.7,'F':2.2,'G':2.0,'H':6.1,'I':7.0,'J':0.02,'K':0.08,'L':4.0,'M':2.4,'N':6.7,'O':7.5,'P':1.9,'Q':0.01,'R':6.0,'S':6.3,'T':9.1,'U':2.8,'V':1.0,'W':2.3,'X':0.01,'Y':2.0,'Z':0.01}
        for key,val in freq_set.items():
            keyset.append(product_value(val,stand_freq))
        key="".join(keyset).lower()
        plain_text=""
        j=0
        for c in cipher_text:
            plain_text+=chr(97+(ord(c)%65-ord(key[j])%65)%26)
            j=(j+1)%len(key)
        print("key value:",key)
        print(plain_text)
        return [key,plain_text]
