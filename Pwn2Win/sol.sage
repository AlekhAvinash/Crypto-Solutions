import pickle
from string import printable
from gmpy2 import iroot, next_prime, is_prime

p = GF(random_prime(1<<32))
e = 341524
order = [(5, 3), (4, 0), (6, 0), (2, 0), (2, 1), (5, 0), (3, 1), (1, 0), (6, 3), (4, 1), (4, 3), (6, 4), (5, 4), (4, 2), (5, 2), (3, 0), (6, 1), (5, 1), (6, 5), (3, 2), (6, 2), (5, 5), (6, 6), (0, 0), (3, 3), (4, 4), (1, 1), (2, 2), (1, 3), (0, 1), (0, 5), (4, 6), (4, 5), (5, 6), (1, 5), (2, 3), (0, 4), (3, 6), (0, 3), (2, 6), (1, 4), (2, 5), (3, 4), (2, 4), (0, 6), (0, 2), (3, 5), (1, 2), (1, 6)]

def get_e(val, k= 2, ret = []):
	while val>128 and not is_prime(val):
		tmp, flag = iroot(val, k)
		if flag:
			val = tmp
			ret += [int(k)]
		else:
			k = next_prime(k)
	return int(k), ret

def brute(pt, ct, loc):
	for i in printable:
		pt[loc] = ord(i)
		if (pt^e)[loc]==ct[loc]:
			return i, True
	pt[loc] = 0
	return -1, False

def crack(pt, ct):
	print('cracking..')
	for depth in range(6):
		for i in range(7-depth):
			loc = (i+depth,i)
			if not pt[loc]:
				brute(pt, ct, loc)
		print(f'pass: {depth}\n{pt}')

def get_ct():
	cip = ''.join([str(i).zfill(2) for i in open('enc','rb').read()])
	ln = len(cip)
	# [2, 2, 3, 3, 3, 7, 7, 19, 349]
	for i in set(ecm.factor(ln)):
		sptLn = ln//(i^2)
		yield Matrix(p, i, i, [p(cip[i:i+sptLn]) 
			for i in range(0, ln, sptLn)])

if __name__ == '__main__':
	# enc is large file.. run at own risk.. 
	# ct = get_ct(GF(p))
	a = (pickle.load(open('ct.pickle', 'rb')))
	ct = Matrix(p, 7, 7, a)

	known = b'CTF-BR{'+b'\x00'*18+b'}'
	mat = Matrix(p, 7, 7)
	for i,j in zip(known, order):
		mat[j] = i

	crack(mat, ct)
	flag = ''.join([chr(mat[loc]) for loc in order if mat[loc]])
	print(flag)
