#approch:
#find leght by adding control variable.
#find no of blocks from size of text.
#add "a"*16 times the number of blocks subtract one. so that just one variable of secret text is in the last block
#use the same set but instead of subtractin 1 use a bruteforce algorithm to find similar result.


from Crypto.Cipher import AES
import binascii
import base64

def wrap(s,t=16):								#padding
    if(len(s)%t==0):
    	return s+chr(t)*t
    else:
    	t-=len(s)%16
    	return s+chr(t)*t

def encrypto(a,key="Yellow Submarine"):			#encrypt
	secret="Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
	secret=(base64.b64decode(secret)).decode("utf-8")

	a=wrap(a+secret)
	cipher=AES.new(key,AES.MODE_ECB)
	v=cipher.encrypt(a)
	v=str(binascii.hexlify(v))[2:-1]
	return v

def len_of(text):									#length of secret
	ctrllen=len(encrypto(""))
	t=ctrllen
	i=0
	while(ctrllen==t):
		t=len(encrypto("a"*i))
		i+=1
	return int(ctrllen/2)-(i),int(ctrllen/32)		#returns size of text and number of blocks

def brtest(li,go,ctrl,v=""):						#brutforce test
	for i in range(128):
		test=encrypto(li+v+chr(i))[:32*go]
		if test==ctrl:
			return i 								#returns each character

def decrypto(t):
	c,go=len_of(t)
	te=""
	print(c)
	for i in range(c+1):
		li="a"*(16*go-(i+1))
		ctrl=encrypto(li)[:32*go]
		v=brtest(li,go,ctrl,te)
		te+=chr(v)		
	return te

a=""
t=encrypto(a)
vr=decrypto(t)
print(vr)
