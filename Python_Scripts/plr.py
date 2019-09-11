# Polar v 0.0.2
# Author : Nyan-uwu - https://github.com/Nyan-uwu


tokens = []
lumptokens = []
variables = []
defenitions = []

import Syntax as syntax
syntax = syntax.SyntaxIdentifiers()

import Utility as utility
fileoperator = utility.fileFunctions()

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
	# print(file)

	################################################

	# Parse
	line = 0
	while line < len(file):
		pos = 0
		while pos < len(file[line]):
			tok = file[line][pos]
			# print(tok) # DEBUG
			if tok[0] == syntax.comment_ident:
				pos = len(file[line]) + 1
				continue
			else:
				if tok[0] == syntax.variable_ident:
					# print("FOUND VARIABLE") # DEBUG
					tokens.append(Token(t="var", v=tok[1:], l=line,p=pos))

				elif tok == syntax.echo_ident:
					# print("FOUND ECHO") # DEBUG
					tokens.append(Token(t="echo", l=line,p=pos))
				elif tok == syntax.echotag_ident:
					# print("FOUND ECHO") # DEBUG
					tokens.append(Token(t="echotag", l=line,p=pos))

				elif tok == syntax.def_ident:
					# print("FOUND DEF")
					pos += 1
					tok = file[line][pos]
					tokens.append(Token(t="def", v=tok, l=line, p=pos))
				elif tok[0] == syntax.def_ident:
					# print("FOUND DEF")
					tokens.append(Token(t="def", v=tok[1:], l=line, p=pos))
				elif tok == syntax.indef_ident:
					# print("FOUND INDEF")
					tokens.append(Token(t="indef", v=True, l=line, p=pos))
				elif tok == syntax.go_ident:
					# print("FOUND INDEF")
					tokens.append(Token(t="godef", l=line, p=pos))

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
				elif tok == syntax.string_ident:
					# print("FOUND STR") # DEBUG
					pos += 1
					tok = file[line][pos]
					if tok[0] == "\"":
						string = tok[1:]
						while True:
							pos += 1
							tok = file[line][pos]
							if tok[len(tok)-1] == "\"":
								string += " " + tok[0:len(tok)-1]
								tokens.append(Token(t="str", v=string, l=line,p=pos))
								break
							else:
								string += " " + tok
								continue
					else:
						tokens.append(Token(t="str", v=tok, l=line,p=pos))
				elif tok[0] == syntax.str_ident:
					# print("FOUND STR") # DEBUG
					if tok[len(tok)-1] == "\"":
						string = tok[1:len(tok)-1]
						tokens.append(Token(t="str", v=string, l=line,p=pos))
					else:
						string = tok[1:]
						while True:
							pos += 1
							tok = file[line][pos]
							if tok[len(tok)-1] == "\"":
								string += " " + tok[0:len(tok)-1]
								tokens.append(Token(t="str", v=string, l=line,p=pos))
								break
							else:
								string += " " + tok
								continue
				elif tok == syntax.input_ident:
					# print("FOUND INPUT") # DEBUG
					tokens.append(Token(t="input", l=line,p=pos))

				elif tok == syntax.true_ident:
					# print("FOUND TRUE")
					tokens.append(Token(t="bool", v=True, l=line, p=pos))
				elif tok == syntax.false_ident:
					# print("FOUND FALSE")
					tokens.append(Token(t="bool", v=False, l=line, p=pos))
				else:
					print()

			pos += 1
		tokens.append(Token(t="newline", l=line,p=pos))			
		line += 1

	# Build Lump Tokens
	tokpos = 0
	global lumptokens, defenitions

	defstate = False
	defname = None
	switchdefstate = False
	currentDef = [] # [ [defname, [ lTokens]], [defname, [lTokens]] ]

	lumptoken = None

	while tokpos < len(tokens):
		token = tokens[tokpos]
		if token.t == "newline":
			if defstate:
				try:
					tokpos += 1
					token = tokens[tokpos]
					if token.t != "indef":
						switchdefstate = True
						tokpos -= 1
					else:
						switchdefstate = False
				except IndexError:
					break;
		elif token.t == "def":
			defstate = True
			defname = token.v
		elif token.t == "echo":
			tokpos += 1
			token = tokens[tokpos]
			if token.t == "var":
				varname = token.v
				lumptoken = LumpToken(t="echovar", n=varname, v=token.v)
			elif token.t == "str":
				lumptoken = LumpToken(t="echo", v=token.v)
			else:
				print("ERROR: Expected a Variable after 'echo' | Line:{}, Pos:{}".format(token.l+1, token.p))		
				break
		elif token.t == "set":
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
							lumptoken = LumpToken(t="setvar", n=varname, v=token.v)
						elif token.t == "str":
							lumptoken = LumpToken(t="setvar", n=varname, v=token.v)
						elif token.t == "var":
							lumptoken = LumpToken(t="setvarasvar", n=varname, v=token.v)
						elif token.t == "input":
							lumptoken = LumpToken(t="setvar", n=varname, v="inputreq")
						else:
							print("ERROR: Expected a VariableType declaration after SETAS ':' | Line:{}, Pos:{}".format(token.l+1, token.p))		
							break
					else:
						tokpos -= 1
						lumptoken = LumpToken(t="setvar", n=varname, v=None)
				except IndexError:
					tokpos -= 1
					lumptoken = LumpToken(t="setvar", n=varname, v=None)
			else:
				print("ERROR: Expected a variable declaration after SET | Line:{}, Pos:{}".format(token.l+1, token.p))
				break
		elif token.t == "echotag":
			tokpos += 1
			token = tokens[tokpos]
			if token.t == "bool":
				lumptoken = LumpToken(t="echotag", v=token.v)
			else:
				print("ERROR: Expected a Boolean after ECHOTAG | Line:{}, Pos:{}".format(token.l+1, token.p))
				break
		elif token.t == "godef":
			tokpos += 1
			token = tokens[tokpos]
			if token.t == "def":
				lumptoken = LumpToken(t="godef", v=token.v)
			else:
				print("ERROR: Expected a Defenition after GO | Line:{}, Pos:{}".format(token.l+1, token.p))
				break

		# Add lToken to final arr
		if lumptoken != None:
			if (defstate == True):
				# print("Adding lToken To Def")
				currentDef.append(lumptoken)
			else:
				# print("Adding lToken To Script")
				lumptokens.append(lumptoken)
			lumptoken = None

		if switchdefstate:
			defstate = False
			defenitions.append([defname, currentDef])
			defname = None
			currentDef = []
			switchdefstate = False

		tokpos += 1

echotag = True
def exe(ltokens):
	global echotag
	# Final Execute script
	ltokpos = 0
	while ltokpos < len(ltokens):
		ltoken = ltokens[ltokpos]
		# print(ltoken.t) # DEBUG

		if ltoken.t == "setvar":
			updatevar(ltoken)
		elif ltoken.t == "setvarasvar":
			ltoken.v = searchvar(ltoken.v)
			updatevar(ltoken)

		elif ltoken.t == "echotag":
			echotag = ltoken.v
		elif ltoken.t == "echo":
			if echotag:
				print(">", ltoken.v)
			else:
				print(ltoken.v)
		elif ltoken.t == "echovar":
			if echotag:
				print(">", searchvar(ltoken.n))
			else:
				print(searchvar(ltoken.n))

		elif ltoken.t == "godef":
			defarr = searchdef(ltoken.v)
			if defarr != None:
				exe(defarr)

		ltokpos += 1

# lToken Utility
def updatevar(lumptoken):
	global variables

	vex = False # Variable EXists

	for i in range(0, len(variables)):
		if variables[i][0] == lumptoken.n:
			vex = True
			if lumptoken.v == "inputreq":
				variables[i][1] = input(lumptoken.n + ": ")	
			else:
				variables[i][1] = lumptoken.v
			break

	if vex == False:
		if lumptoken.v == "inputreq":
			variables.append([lumptoken.n, input(lumptoken.n + ": ")])
		else:
			variables.append([lumptoken.n, lumptoken.v])

def searchvar(varname):
	for i in range(0, len(variables)):
		if variables[i][0] == varname:
			return variables[i][1]
	# print("Variable not found: Value:Null")
	return None

def searchdef(defname):
	for i in range(0, len(defenitions)):
		if defenitions[i][0] == defname:
			return defenitions[i][1]
	# print("Variable not found: Value:Null")
	return None	



main()
exe(lumptokens)

# DEBUG #

# print("- - - - - - -")

# for token in tokens:
# 	print(token.t, ":", token.v)

# print("- - - - - - -")

# print(variables)

# print("- - - - - - -")

# for d in defenitions:
# 	print(d[0])
# 	if d[1] == []:
# 		print("EMPTY DEF")
# 	else:
# 		for dt in d[1]:
# 			print(dt.t)

# print("- - - - - - -")

# for token in lumptokens:
# 	print(token.t, ":", token.v)