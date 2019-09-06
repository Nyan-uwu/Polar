import sys

tokens = []
lumptokens = []
variables = []

class SyntaxIdentifiers:
	comment_ident  = '%'
	variable_ident = '$'
	set_ident      = "set"
	setas_ident    = ':'
	int_ident      = "int"
syntax = SyntaxIdentifiers()

class fileFunctions:
	def load(self, filename):
		return open(filename, "r").read()

	def splitfile(self, file):
		file = file.split("\n")
		output = []
		for line in file:
			output.append(line.split(" "))
		return output

	def cleanfile(self, file):
		for i in range(0, len(file)):
			for j in range(0, len(file[i])):
				if file[i][j] == "":
					file[i].remove(file[i][j])

		return file

	def complete(self):
		if len(sys.argv) > 1:
			return self.cleanfile(self.splitfile(self.load(sys.argv[1])))
		else:
			return self.cleanfile(self.splitfile(self.load(input("Filename: "))))
fileoperator = fileFunctions()

################################################

class Token:

	t = None # Type
	v = None # Value

	l = 0
	p  = 0

	def __init__(self, t, v=None, l=0, p=0):
		self.t = t
		self.v = v
		self.l = l
		self.p = p

class LumpToken:

	t = None # Type
	n = None # Name
	v = None # Value

	l = 0    # Line
	p  = 0   # Pos

	def __init__(self, t, n=None, v=None, l=0, p=0):
		self.t = t
		self.n = n
		self.v = v
		self.l = l
		self.p = p


################################################

def main():
	global tokens
	file = fileoperator.complete()
	print(file)

	################################################

	# Parse
	line = 0
	while line < len(file):
		pos = 0
		while pos < len(file[line]):
			tok = file[line][pos].lower()
			# print(tok) # DEBUG
			if tok[0] == syntax.comment_ident:
				pos = len(file[line]) + 1
				continue
			else:
				if tok[0] == syntax.variable_ident:
					# print("FOUND VARIABLE") # DEBUG
					tokens.append(Token(t="var", v=tok[1:], l=line,p=pos))
				elif tok == syntax.set_ident:
					# print("FOUND SET") # DEBUG
					tokens.append(Token(t="set", l=line,p=pos))
				elif tok == syntax.setas_ident:
					# print("FOUND SETAS") # DEBUG
					tokens.append(Token(t="setas", l=line,p=pos))
				elif tok == syntax.int_ident:
					# print("FOUND INT") # DEBUG
					pos += 1
					tok = int(file[line][pos])
					tokens.append(Token(t="int", v=tok, l=line,p=pos))

			pos += 1
		line += 1

	# Build Lump Tokens
	tokpos = 0
	global lumptokens
	while tokpos < len(tokens):
		token = tokens[tokpos]
		if token.t == "set":
			tokpos += 1
			token = tokens[tokpos]
			if token.t == "var":
				varname = token.v
				try:
					tokpos += 1
					token = tokens[tokpos]
					if token.t == "setas":
						tokpos += 1
						token = tokens[tokpos]
						if token.t == "int":
							lumptokens.append(LumpToken(t="setvar", n=varname, v=token.v))
						else:
							print("ERROR: Expected a int declaration after SETAS ':' | Line:{}, Pos:{}".format(token.l+1, token.p))		
							break
					else:
						tokpos -= 1
						lumptokens.append(LumpToken(t="setvar", n=varname, v=None))
				except IndexError:
					tokpos -= 1
					lumptokens.append(LumpToken(t="setvar", n=varname, v=None))
			else:
				print("ERROR: Expected a variable declaration after SET | Line:{}, Pos:{}".format(token.l+1, token.p))
				break

		tokpos += 1

	# Final Execute script
	ltokpos = 0
	while ltokpos < len(lumptokens):
		ltoken = lumptokens[ltokpos]
		print(ltoken.t)
		if ltoken.t == "setvar":
			updatevar(ltoken)

		ltokpos += 1

def updatevar(lumptoken):
	global variables

	vex = False

	for i in range(0, len(variables)):
		if variables[i][0] == lumptoken.n:
			vex = True
			variables[i][1] = lumptoken.v
			break

	if vex == False:
		variables.append([lumptoken.n, lumptoken.v])


main()

print(variables)

# for token in lumptokens:         # DEBUG
# 	print(token.t, ":", token.v)   # DEBUG