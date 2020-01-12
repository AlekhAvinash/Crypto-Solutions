#approch:
#find the block in which the prefix ends by adding "a" and check singular blocks until different block
#find number of random chars in said block by adding 32 bytes of "a" so that there is atlest 1 block of "a"s
#and comparing it with incremental "a"s until the block after random chars is equal. the counter -16 is the 
#number of bytes req to fill block with last random variables
#now use the algorithm for ECB easier but when calling add counted variable and remove the random blocks.


from Crypto.Cipher import AES
import binascii
import base64
import random

def prefixer():										#adding prefix
	k=random.randrange(100)
	s=""							#random byte count
	for i in range(k):
		s=(chr(random.randrange(100)))+s
	return s

def defixer(s):
	i=0
	while(s[i]==s[i+1]):
		i+=1
	return s[i+1:]

def prep():											#prepares given text
	secret="Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
	secret=(base64.b64decode(secret)).decode("utf-8")
	return secret

def wrap(s,t=16):									#padding
    if(len(s)%t==0):
    	return s+chr(t)*t
    else:
    	t-=len(s)%16
    	return s+chr(t)*t

def encrypto(a,key="Yellow Submarine"):				#encrypt
	global er
	global pr
	a=wrap(pr+a+er)
	cipher=AES.new(key,AES.MODE_ECB)				#ENCRYPTING
	v=cipher.encrypt(a)
	v=str(binascii.hexlify(v))[2:-1]
	return v

def len_of(text):
	ctrllen=len(text)								#length of secret
	t=encrypto("a")
	for k in range(int(ctrllen/32)):
		if text[k*32:(k+1)*32]!=t[k*32:(k+1)*32]:
			break
	j=0
	t=encrypto("a"*32)[(k+1)*32:(k+2)*32]
	l=text[(k+1)*32:(k+2)*32]
	while(l!=t):
		j+=1
		l=encrypto("a"*j)[(k+1)*32:(k+2)*32]
	j-=16
	d=16-j
	k=(k+2)*32
	ctrllen=len(encrypto("a"*j))
	t=ctrllen
	i=-1
	while(ctrllen==t):
		i+=1
		t=len(encrypto("a"*(i+j)))
	return int(ctrllen/32),int(d),int((t-k-32)/2)+(16-i)	#returns size of text and number of blocks

def brtest(li,go,ctrl,v=""):						#brutforce test
	for i in range(128):
		test=encrypto(li+v+chr(i))[32*go:32*(go+1)]
		if test==ctrl:
			return i 								#returns each character

def decrypto(t):
	go,j,k=len_of(t)
	te=""
	for i in range(k):
		li="a"*((16*go-(i+1))+(16-j))
		ctrl=encrypto(li)[32*go:32*(go+1)]
		v=brtest(li,go,ctrl,te)
		te+=chr(v)		
	return te


er=prep()
pr=prefixer()
print("Before Encryption:-\n"+er)
test_case=wrap(pr+er)
print("After Prefix and Wrapping:-\n"+test_case)
t=encrypto("")
dr=decrypto(t)
print("After Decryption:-\n"+dr)
