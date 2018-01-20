import os

def getFilesWithWord(word):
	files=[]
	dirfiles=os.listdir('corpus')

	#check if negation is required
	negate=False
	if 'not' in word:
		negate=True
		word=word.split('-')[1]
	
	#get files in which the word is present
	for filename in dirfiles:
		if filename.endswith(".txt"):
			for line in open('corpus/'+filename).readlines():
				if word in line:
					files.append(filename)
					break

	if negate:
		#get files in which word isn't present
		return [val for val in dirfiles if val not in files]
	else:
		return files


#perform and operation
def andOperation(files1,files2):
	return [val for val in files1 if val in files2]

#perform or operation
def orOperation(files1,files2):
	files1.extend(files2)
	return list(set(files1))


def evaluateQuery(query):
	stack=[]
	words=query.strip().split(" ")

	i=0
	while i < len(words):
		#if word is a term, add its file list to stack
		if words[i] not in ['and','or']:
			stack.append(getFilesWithWord(words[i]))
			i=i+1
		#else perform and/or operation on element on stack top and next word
		else:
			if words[i]=='and':
				stack.append(andOperation(stack.pop(),getFilesWithWord(words[i+1])))
			elif words[i]=='or':
				stack.append(orOperation(stack.pop(),getFilesWithWord(words[i+1])))
			i=i+2

	#print title of files of the result
	print "\nQuery: ",query
	for opfile in stack.pop():
		print open('corpus/'+opfile).readlines()[0],


evaluateQuery('Julius and Brutus and not-Calpurnia')
evaluateQuery('Julius and not-Calpurnia or Brutus')
evaluateQuery('Anthony and not-Cleopatra')
