import re,os

#initializeInvertedIndex
dictionary={}

class Node:
	def __init__(self,value):
		self.value=value
		self.next=None



def createLinkedList(files):
	if len(files):
		linkedlist=Node(files[0])
		cur=linkedlist
		for f in files[1:]:
			cur.next=Node(f)
			cur=cur.next
		return linkedlist


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
	return createLinkedList(files)


def findOtherFiles(fileslist):
	i=1
	result=[]
	newlist=[]
	cur=fileslist
	while cur:
		newlist.append(cur.value)
		cur=cur.next
	while i<=27:
		if i not in newlist:
			result.append(i)
		i=i+1

	return createLinkedList(result)


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
	cur1=list1
	cur2=list2
	while cur1 and cur2:
		if cur1.value==cur2.value:
			answer.append(cur1.value)
			cur1=cur1.next
			cur2=cur2.next
		elif cur1.value<cur2.value:
			cur1=cur1.next
		else:
			cur2=cur2.next
	return createLinkedList(answer)


def orOperation(list1,list2):
	answer=[]
	cur1=list1
	cur2=list2
	while cur1 and cur2:
		if cur1.value==cur2.value:
			answer.append(cur1.value)
			cur1=cur1.next
			cur2=cur2.next
		elif cur1.value<cur2.value:
			answer.append(cur1.value)
			cur1=cur1.next
		else:
			answer.append(cur2.value)
			cur2=cur2.next

	while cur1:
		answer.append(cur1.value)
		cur1=cur1.next
	while cur2:
		answer.append(cur2.value)
		cur2=cur2.next
	return createLinkedList(answer)


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
			cur=getFiles(words[i+1])
			while cur:
				cur=cur.next
			if words[i]=='and':
				stack.append(andOperation(stack.pop(),getFiles(words[i+1])))
			elif words[i]=='or':
				stack.append(orOperation(stack.pop(),getFiles(words[i+1])))
			i=i+2

	#print (dictionary)
	#print title of files of the result
	print "\nQuery: ",query
	cur=stack.pop()
	while cur:
		print open('corpus/play'+str(cur.value)+'.txt').readlines()[0],
		cur=cur.next


evaluateQuery('Julius and Brutus and not-Calpurnia')
evaluateQuery('Julius and not-Calpurnia or Brutus')
evaluateQuery('Anthony and not-Cleopatra')
