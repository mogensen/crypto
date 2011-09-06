import operator
import fractions
import os.path
import sys
import getopt

 
'''
	Decrypts a character based on the alpha/beta values of the algorithm
'''
def decrypt(shift, char):
	letter = ord(char) - 65
	return chr(((letter - shift ) % 26) + 97 )
 
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
	length=len(freq)-1
	while x < length:

		print
		print freq[x][0]+"=e"
		print "shift key is: " + str(ord(freq[x][0])-65-4)

		print ord(freq[x][0] )-65-4
		key = ord(freq[x][0][0] )-65-4
		shift = key
		print key

		message = ""
		for c in cipher:
			message = message + decrypt(shift, c)

		print message
		s = raw_input("Is this the correct cleartext? (y/N)")
		if (s == "y"):
			print "Nice..."
			sys.exit(0)
		x = x + 1

def usage():
	print "Shift Cipher decoder"
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
