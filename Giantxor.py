import string

def get_english_score(input_bytes):
	if all (x.isalnum() or x=='=' or x=='/' or x=='+' or x=='\n'for x in input_bytes):
		return 1
	else:
		return 0

def bruteforce_single_byte_xor(ciphertext,key_byte):
	a = []
	for i in range(256):
		message = single_byte_xor(ciphertext, i)
		score = get_english_score(message)
		a.append(score)
	val=chr(a.index(max(a)))
	return val

def single_byte_xor(input_bytes, char_value):
    output_bytes = ""
    for byte in input_bytes:
        output_bytes += chr(ord(byte) ^ char_value)
    return output_bytes

def find_key(length,ciphertext):
	key=""
	for i in range(length):
		block = ""
		for j in range(i, len(ciphertext), length):
			block+=(ciphertext[j])
		key += bruteforce_single_byte_xor(block,i) 
	return message(key,ciphertext)

def message(key,ciphertext):
	message=""
	for i in range(len(ciphertext)):
		message+=chr(ord(key[i%len(key)])^ord(ciphertext[i]))
	return message.decode("base64")


def find_keylen(cip):
	IC=[]
	for lenn in range(2, 50):
		v=0
		a,c=0,0
		for i in range(len(cip)):
			test=cip[lenn+i::lenn]
			c+=test.count(cip[i])
			a+=len(test)
		v=float(c)/float(a)
		IC.append(v)
	return IC.index(max(IC))+2


secret_flag = "6e19223f204b31183e333f005c122d37264a350e3e3c2808672436250b3f3d1b2e2c151c671d553e182b4713262c3f045c1d553e0b3f391c1449385d7309223c20153d022d3c011a673322394822242e0118003a5a1333123b222b361b22353d5110231230222b1f102c28566e03281a2e21240c041e3e2d491337022e313b26181a3a5a532919122a31343e071f2e2d4928531a2e31342607713702673a3963140b1737001c0f5c742d3a172e133a331b4b3d167f090418210b3a31390d0f025933390810023a334e0e2427733c021818081119141c0928552629170c172a230f08373808246a0a113d142645421b357e0853327132013d2439243565000c190514093d3f171b0b6503070a2f001b2e0d140a0e6a7f0a340522442d1a3d17356913500870290b2e31435d0d7a32061e70101f7e2f495d5f6730263a1a4b39042d49055f6d79506d48"
secret_flag=secret_flag.decode('hex')
klen=find_keylen(secret_flag)
t=find_key(klen,secret_flag)
print(t)