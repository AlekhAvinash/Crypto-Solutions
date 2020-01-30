from Crypto.Cipher import AES
import os
import binascii

key=b'\xd9Z\xbb\xe1Y"\x80\xc8\xabF\xa6\xba\xbb\x9du\x03'
IV="a"*16

def prepost(text):
	text="comment1=cooking%20MCs;userdata="+text
	text+=";comment2=%20like%20a%20pound%20of%20bacon"
	a=[';','=']
	for i in range(len(a)):
		text=text.replace(a[i],'#')
	return text

def padding(text):
	t=16
	if(len(text)%t!=0):
		t-=len(text)%16
	return text+chr(t)*t

def cbcencrypt(text):
	cipher = AES.new(key, AES.MODE_CBC, IV)
	return cipher.encrypt(IV+text)

def func_one(inp):
	inp=prepost(inp)
	pad_inp=padding(inp)
	cip=cbcencrypt(pad_inp)
	return binascii.hexlify(cip).decode('utf-8')

text="a"*11+"admin=true"
ciphertext=func_one(text)
print(ciphertext)