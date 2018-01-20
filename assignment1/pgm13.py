from pandas import DataFrame
import os,pandas as pd,numpy as np 


dirfiles=os.listdir('corpus')
tdm=DataFrame(columns=dirfiles)
stack=[]

def updateTDM(word):
	global tdm,dirfiles
	files=[]
	for filename in dirfiles:
		if filename.endswith(".txt"):
			#add word index into the matrix
			tdm.loc[word]=[False]*len(dirfiles)
			#find files that contain the word
			for line in open('corpus/'+filename).readlines():
				if word in line:
					files.append(filename)
					break
	#make those files as true in the matrix
	tdm.loc[[word],files]=True


#perform and operation
def andOperation(row1,row2):
	return (row1 & row2)

#perform or operation
def orOperation(row1,row2):
	return (row1 | row2)

#check if word is present in document matrix else add
#add the word(negated if required) to stack
def checkWord(word):
	negate=False
	if 'not' in word:
		word=word.split('-')[1]
		negate=True

	if word not in tdm.index:
		updateTDM(word)
	
	if negate:
		stack.append(-tdm.loc[word])
	else:
		stack.append(tdm.loc[word])


def evaluateQuery(query):
	words=query.strip().split(" ")

	i=0
	while i < len(words):

		#if word is a term, add its file list to stack
		if words[i] not in ['and','or']:
			checkWord(words[i])
			i=i+1

		#else perform and/or operation on element on stack top and next word
		else:
			checkWord(words[i+1])
			if words[i]=='and':
				stack.append(andOperation(stack.pop(),stack.pop()))
			elif words[i]=='or':
				stack.append(orOperation(stack.pop(),stack.pop()))
			i=i+2
		
	#print title of files of the result
	print "\nQuery: ",query
	result=stack.pop()
	files=result.index[result]
	for opfile in files:
		print open('corpus/'+opfile).readlines()[0],
	

evaluateQuery('Julius and Brutus and not-Calpurnia')
evaluateQuery('Julius and not-Calpurnia or Brutus')
evaluateQuery('Anthony and not-Cleopatra')

