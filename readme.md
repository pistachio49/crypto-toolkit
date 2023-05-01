Install python3 on linux device and go to the root folder.
<div class="scrollable" id="scrollable">
	<ul>
		<li>List Item</li>
		<li>List Item</li>
		<li>List Item</li>
		<li>List Item</li>
		<li>List Item</li>
		<li>List Item</li>
	</ul>
</div>
install modules using command : pip install -r requirements.txt

Run the server using command: python3 app.py 


Everytime if numerical appear in plain/cipher text error message will popup.<br>
Everytime if a blank column is present error message will popup.<br>

Message box: 
AFFINE:

	ENCRYPTION:
	plain text should be alphabetic characters.Numericals are not allowed in plain text. Key1 should have multiplicative inverse in modulo 26.

	DECRYPTION:
	cipher text should be alphabetic characters.Numericals are not allowed in plain text. Key1 should have multiplicative inverse in modulo 26.

	
	CRYPTANALYSIS:
	message :cipher text = alphabets only 
	doubt and correction:
	updated words list with more words?
	analyse cryptanalysis.py file and make changes as mentioned.
	
	
HILL:

	ENCRYPTION:
	key size = size of key matrix
	key = alphabetic characters only with length key size*2
	plain text = alphabets 							
	boguz characters will be added (eg: z, yz, xyz, wxyz) as required
	
	DECRYPTION:
	ciphertext must be a multiple of the key matrix size
	key size = size of key matrix
	key = alphabetic characters only with length key size*2, key should be necessarily invertible. if non invertible matrix added then show error message.
	cipher text = alphabets     //update on python side
	boguz characters will be added (eg: z, yz, xyz, wxyz) as required
	
	CRYPTANALYSIS:
	plain and cipher text should be alphabets.
	cipher - WBVE
	plain - INMA
	keysize = 2
	
SHIFT/CAESER:
	
	Caeser cipher is choosen then key should not be present:
	ENCRYPTION:
	plain text = alphabets 
	key = numericals
	
	DECRYPTION:
	cipher text = alphabets 
	key = numericals
	
	CRYPTANALYSIS:
	cipher text = alphabets

VIGENERE CIPHER:
	
	Ensure naming is correct "Vigenere"
	ENCRYPTION:
	plain text = alphabets
	key = alphabets
	
	
	DECRYPTION:
	cipher text = alphabets
	key = alphabets
	

Monoalphabetic Substitution cipher:

	
	ENCRYPTION:
	Plain text: alphabets
	Key: alphabets only with 26 characters present necessarily 
	
	DECRYPTION:
	Cipher text: alphabets
	Key: alphabets only with 26 characters present necessarily 


TRANSPOSITION:
	
	ENCRYPTION:
	plain text= alphabets only without spaces
	Number of Columns : numbers only
	
	DECRYPTION:
	cipher  text    text= alphabets only without spaces
	Number of Columns : numbers only
	
   PERMUTATION CIPHER:
   	ENCRYPTION:
   	Message: Boguz characters are added (like z,yz,xyz,..)
   	Plain text: alphabets are only allowed
	Key: should be space separated numericals. and they should have (numericals in 1 2 3 4... check in front end)
	
	DECRYPTION:
	Message: key size should be a multiple of cipher text size
	Cipher text text: alphabets are only allowed
	Key: should be space separated numericals. and they should have (numericals in 1 2 3 4... check in front end)
	
   COMBINED APPROACH:
   	ENCRYPTION: 
   	Message: Boguz characters are added (like z,yz,xyz,..)
   	Plain text: alphabets are only allowed
	Key: should be space separated numericals. and they should have (numericals in 1 2 3 4... check in front end)
	
	DECRYPTION:
	Message: key size should be a multiple of cipher text size
	Cipher text text: alphabets are only allowed
	Key: should be space separated numericals. and they should have (numericals in 1 2 3 4... check in front end)
	
	
Examples:

Affine:
p:    securityisapriority
k:    17,23
c:    rnfzadipdrxsadbadip

Shift:
p:    todayisagoodday
k:    17
c:    kfurpzjrxffuurp

Mono:
p: abcde
k: plmoknijbuhvygctfxrdzeswaq
c: plmok


Hill:
c - WBVE
p - INMA
keysize = 2


Input  : Plaintext: ACT
Key: GYBNQKURP
Output : Ciphertext: POH
keysize : 3


Vigenere crypt:
c - WwpemsrgjttdrfvrtcncArgjttdrfvrtcncihpomgxilpcjgcinrnhlirwtwacpwxegclxiktqsrbdqtanbprtrgpettsfwicvprcgnaxidclpgdgtxhbhElejhpsftcnvyeitsnitnlndazkithxiachelairccpidnyrgtygithqynritsnqdelahpnyrgtygypcoespktvtjpwecrdfrtxcrwyhipq

p-
WhatiscryptocurrencyAcryptocurrencyisadigitalcurrencywhichisanalternativeformofpaymentcreatedusingencryptionalgorithmsTheuseofencryptiontechnologiesmeansthatcryptocurrenciesfunctionbothasacurrencyandasavirtualaccountingsystem

k-apple

Transposition:

Railfence;

P: metmeatthepark
c: MEMATEAKETETHPR

fixed columns:
P: metmeatthepark
k : 4

permutation: 	
P: enemyattackstonightz
K: 3 1 4 5 2	
C: EEMYNTAACTTKONSHITZG

combined approach:

P: enemyattackstonightz
K: 3 1 4 5 2	
c: ETTHEAKIMAOTYCNZNTSG




	
		

   
