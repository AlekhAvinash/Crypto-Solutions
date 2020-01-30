from Crypto.Cipher import AES
import binascii

key = b'\xd9Z\xbb\xe1Y"\x80\xc8\xabF\xa6\xba\xbb\x9du\x03'
IV = "a"*16
counter=0

def byte_flip(pt,ct,idx,aidx,trgt,ctrl=-1):
	attack_byte = b''
	for i in range(ctrl*-1):
		attack_byte += (str(hex(int(ct[aidx+(i*2):aidx+(i*2)+2],16)^pt[idx+i]^trgt[i]))[2:]).encode()
	result = ct[:aidx] + attack_byte + ct[aidx+ctrl*-2:]
	return result

def exep(pt,ct):
	idx = pt.find(b'=')
	ctrl = idx%16-5
	idx += ctrl
	aidx = idx*2
	trgt = b'admin'
	result = byte_flip(pt,ct,idx,aidx,trgt,ctrl)
	dec_result = cbcdecrypt(result)
	return dec_result

def attack(pt,ct):
	idx = pt.find(b'admin')+5
	aidx = idx*2-32
	trgt = b'='
	result = byte_flip(pt,ct,idx,aidx,trgt)
	dec_result = cbcdecrypt(result)
	return dec_result,result

def cbcdecrypt(cip):
	dec_inp = binascii.unhexlify(cip)
	cipher = AES.new(key, AES.MODE_CBC, IV)
	dec_str = cipher.decrypt(dec_inp)
	return dec_str

def unwarp(text):
	text = text[16:]
	t = text[-1]
	text = text[:-t]
	return text

def check_func(text):
	if text.find(b'admin=true')!=-1:
		print("True")
	else:
		print("False")

ciphertext = b'e0e3b3964dd16cead874d2f1121204703be595c92076aa9bed0e03c35c75c8fc72d3d87ece5d1715e441c0f886f6e2dc786b256ac915271a3fdad0d03583d21815c70e7c563d7798f7fa711e467a66e58f2d46e2d80c1de372344348f933e941fc585626a7167a529c0f888930a9b158'
plaintext = cbcdecrypt(ciphertext)
at,ciphertext = attack(plaintext,ciphertext)
loc = unwarp(at)
if loc.find(b'admin=true')==-1:
	loc = exep(loc,ciphertext)
check_func(loc)