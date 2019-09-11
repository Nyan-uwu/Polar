import sys

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