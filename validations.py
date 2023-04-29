#validating monoalphabetic substitution cipher
def monovalidation(val):
    if(len(val)==26 and val.isalpha()):
        return True
    else:
        return False

#alphabets with space only
def checkspace(val):
	for i in val:
		if(i.isalpha()==False and i!=" "):
			return False
	return True

#numbers with space only
def checkspace1(val):
	for i in val:
		if(i.isdigit()==False and i!=" "):
			return False
	return True    

#transposition cipher
def transpositionvalid(k,dec,ciphert):
    if(checkspace1(k)==False):
        return "Enter a valid key"
    else:
        c=len(k)-1
        while(c!=-1):
            if(k[c]==' '):
                c=c-1
            else:
                break
        k=k[0:c+1]        
        lst=k.split(' ')
        lst.sort()
        if(lst[0]!='1'):
            return "enter a valid key"
        # print(lst)
        for a in lst:
            if(a.isdigit()==False):
                return "Enter a valid key"
        for j in range(1,len(lst)):
            if(int(int(lst[j-1])+1)!=int(lst[j])):
                return "Enter a valid key"
        if(dec==True):
            if(len(ciphert)%len(lst)!=0):
                return "The size of the cipher text must be divisible by the key size for decryption"
        return "valid!"


        