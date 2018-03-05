import re,os

#initializeInvertedIndex
dictionary={}


def addPosting(term,docIDlist):
	if term in dictionary.keys():
		dictionary[term]=orOperation(dictionary[term],docIDlist)
	else:
		dictionary[term]=docIDlist


def findFiles(term):
	files=[]
	dirfiles=os.listdir('corpus')

	for filename in dirfiles:
		if filename.endswith(".txt"):
			for line in open('corpus/'+filename).readlines():
				if term in line:
					files.extend(re.findall(r'\d+',filename.strip()))
					break
	files=[int(f) for f in files]
	files.sort()
	return files


def findOtherFiles(files):
	i=1
	result=[]
	while i<=27:
		if i not in files:
			result.append(i)
		i+=1
	return result


def getFiles(word):
	negate=False
	if 'not' in word:
		negate=True
		term=word.split("-")[1]
	else:
		term=word
	addPosting(term,findFiles(term))
	return findOtherFiles(dictionary[term]) if negate else dictionary[term]


def andOperation(list1,list2):
	answer=[]
	i,j=0,0
	while i!=len(list1) and j!=len(list2):
		if list1[i]==list2[j]:
			answer.append(list1[i])
			i+=1
			j+=1
		elif list1[i]<list2[j]:
			i+=1
		else:
			j+=1
	return answer


def orOperation(list1,list2):
	answer=[]
	i,j=0,0
	while i!=len(list1) and j!=len(list2):
		if list1[i]==list2[j]:
			answer.append(list1[i])
			i+=1
			j+=1
		elif list1[i]<list2[j]:
			answer.append(list1[i])
			i+=1
		else:
			answer.append(list2[j])
			j+=1

	if i==len(list1):
		while j!=len(list2):
			answer.append(list2[j])
			j+=1
	else:
		while i!=len(list1):
			answer.append(list1[i])
			i+=1
	return answer

def evaluateQuery(query):
	stack=[]
	words=query.strip().split(" ")

	i=0
	while i < len(words):
				
		#if word is a term, add its file list to stack
		if words[i] not in ['and','or']:
			stack.append(getFiles(words[i]))
			i=i+1

		#else perform and/or operation on element on stack top and next word
		else:
			if words[i]=='and':
				stack.append(andOperation(stack.pop(),getFiles(words[i+1])))
			elif words[i]=='or':
				stack.append(orOperation(stack.pop(),getFiles(words[i+1])))
			i=i+2

	#print (dictionary)
	#print title of files of the result
	print "\nQuery: ",query
	for opfile in stack.pop():
		print open('corpus/play'+str(opfile)+'.txt').readlines()[0],


evaluateQuery('Julius and Brutus and not-Calpurnia')
evaluateQuery('Julius and not-Calpurnia or Brutus')
evaluateQuery('Anthony and not-Cleopatra')

