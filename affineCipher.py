import operator
import fractions
import os.path
import sys
import getopt

'''
	Finding the multiplicative inverse, by using the Extended Euclidean Algorithm.
 
	First number returned is the multiplicative inverse for u if v is the base
	Third number determines whether u and v are actually coprime. Should be 1 if they are
'''
def findMultiplicativeInverse(u, base):
	u1 = 1
	u2 = 0
	u3 = u
	v1 = 0
	v2 = 1
	v3 = base
	while v3 != 0:
		q = u3 / v3
		t1 = u1 - q * v1
		t2 = u2 - q * v2
		t3 = u3 - q * v3
		u1 = v1
		u2 = v2
		u3 = v3
		v1 = t1
		v2 = t2
		v3 = t3
	return u1, u2, u3
 
'''
	Decrypts a character based on the alpha/beta values of the algorithm
'''
def decrypt(key, shift, char):
	v = findMultiplicativeInverse(key, 26)
 
	return chr(((v[0]) * ((ord(char) - 65) - shift) % 26) + 97)
 
'''
	Guesses a key/shift pair based on a CIPHER=plaintext combo
 
	Input Example:
		First character: Y=e
		Second character: N=j
 
	Returns a pair of integers. The first is the key, and the second is the shift
'''
def guess_key(key1, key2):
	p = ord(key1.split("=")[1]) - 97
	r = ord(key1.split("=")[0]) - 65
	q = ord(key2.split("=")[1]) - 97
	s = ord(key2.split("=")[0]) - 65
 
	d = (p - q) % 26
	dinv = findMultiplicativeInverse(d, 26)[0]
 
	a = (dinv * (r - s)) % 26
	b = (dinv * (p * s - q * r)) % 26
 
	return a, b

def frequencyAnalsys(cipher):
	dict = {}
	for letter in cipher:
		if letter not in dict:
			dict[letter] = 1
		else:
			dict[letter] += 1

	sd = sorted(dict.iteritems(), key=operator.itemgetter(1))

	sd.reverse()
	return sd
 
'''
	Loop to allow multiple guesses without needing to restart the program
'''
def run(freq, cipher):
	x=0
	y=0
	length=len(freq)-1
	while x < length:

		if (y >= length):
			y=0
			x = x + 1
		else:
			y = y + 1

		a, b = guess_key(freq[x][0]+"=e", freq[y][0]+"=t")

		print 
		print "Guess is: a = " + str(a) + ", b = " + str(b)
		cd = fractions.gcd(a, 26)
		print "GCP( " + str(a) + ", 26 ) = " + str(cd)

		if ( cd != 1 ) :
			print "[ERROR] \"a\" not allowed as key"

		if ( a != 0 and cd==1):
			print "[SUCCESS] \"a\" is allowed as key"

			print freq[x][0]+"=e"
			print freq[y][0]+"=t" 

			message = ""
			for c in cipher:
				message = message + decrypt(a, b, c)

			print message
			s = raw_input("Is this the correct cleartext? (y/N)")
			if (s == "y"):
				print "Nice..."
				sys.exit(0)

def usage():
	print "Affine Cipher decoder"
	print ""
	print " -h			- Prints this dialog"
	print " --help			- See -h"
	print ""
	print " -f			- The path to the file containing the cipher text"
	print " --file=		- See -f"

def main(argv):
	global file
	global cipherText
	try:
		opts, args = getopt.getopt(argv, "hf:", ["help", "file="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-f", "--file"):
			file = arg

	if 'file' not in globals():
		usage()
		sys.exit(2)

	os.path.exists(file)
	cipherText = ""

	infile = open(file)
	cipherText = infile.read()


if (__name__ == "__main__"):
    main(sys.argv[1:])
print "File: "
print "	" + file
print "Cipher: "
print "	" + cipherText
freq = frequencyAnalsys(cipherText)

print "Letter frequency used to guess key from:"
for key in freq:
	  print key
run(freq, cipherText)
