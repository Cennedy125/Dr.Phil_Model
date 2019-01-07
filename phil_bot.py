# CMSC/LING 208 Final Project
# Name: Kennedy Ellison

import re
import random
from nltk import sent_tokenize


# Part 1: Preprocessing
def preprocess(data):
  """function takes in corpus and makes everything lowercase
      and removes punctuation.
     input: list of strings
     output: list of strings"""

  #remove urls and convert to lowercase
  #used this thread for help on urls: https://stackoverflow.com/questions/11331982/how-to-remove-any-url-within-a-string-in-python
  remove_url = [re.sub(r'^https?:\/\/.*[\r\n]*', '', x) for x in data]
  lower=[x.lower() for x in remove_url]

  #remove all non alphanumeric chars  and empty strings
  return filter(None, [re.sub(r'\W','',x) for x in lower])

# Part 2: Get bigram and unigram counts

def get_counts(data):
   """function takes a list of strings
   creates a dictionary of bigrams with their counts as values
   and a dictionary of unigrams and their counts as values
   input: list of strings
   output: tuple of bigrams and unigrams"""

   bigrams = {}
   unigrams = {}
   #range is len-1 because the bigram uses ith+1 element
   data=list(data)
   for i in range(0, len(data)-1):
      #ith element and ith+1 element
       bigram=(data[i],data[i+1])
       if(bigram in bigrams):
           count=bigrams[bigram]
           bigrams[bigram]= count+1
       else:
          #if bigram not in dict of bigrams, add with count 1
           bigrams[bigram]=1

   for unigram in data:
       if(unigram in unigrams):
           count=unigrams[unigram]
           unigrams[unigram]= count+1
       else:
          #if unigram not present, add with count 1
           unigrams[unigram]=1

   return bigrams,unigrams


# Part 3: Build the bigram model

def build_bigram_model(data):
   """function takes a list of strings and produces a model
   which is a dictionary with a bigram key and probablility
   of the bigram as the value.
   input: list of strings
   output: dictionary of string keys and float values"""

   bigrams,unigrams = get_counts(data)
   model = {}
   for bigram in bigrams:
      #unigram count of first member of bigram
       uni_count=unigrams[bigram[0]]
       bi_count=bigrams[bigram]

       #probability is bigram count divided by unigram count
       model[bigram]=(bi_count/float(uni_count))
   return model


def generate_sentence(model, opener_words):
   """The function generates a random sentence of a random length.
   The first word is chosen by picking a random bigram.
   The following words are taken by using the second word in a bigram
   and making a list of all keys with that word as the first word in a bigram.
   A bigram from the list is picked randonmly.
   This process repeats until the sentence is the appropriate length.
   input:dictionary
   output: string """

   sentence=[]
   #sentences between 3 and 15 words
   length= random.randint(3,6)
   keys=model.keys()
   bigram=random.choice(list(keys))

   #choose a first word that can be a starter word
   while bigram[0] not in opener_words:
       bigram=random.choice(list(keys))
   #iterate until sentence is correct length
   for i in range(0,length):
      matches=[]
      found=False
      while not found:

         #search in keys for key[0] to match the bigram[1]
         for key in keys:
            regex=re.compile(r"\b%s\b"%bigram[1])
            result=regex.match(key[0])
            if result:
               matches.append(key)
               found=True
         if not found:
             matches=[]
             i=0
             bigram=random.choice(list(keys))
             sentence.pop()

      #add first member of bigram to sentence list
      sentence.append(bigram[1])
      #choose next bigram from the list of matches
      bigram=random.choice(matches)

   #combine strings from list
   return " ".join(sentence)

def openers(data):
    '''Finds words that begin sentences and returns a list'''
    sents = sent_tokenize(data)
    words=[]
    for sent in sents:
        word=(sent.split())[0]
        if word not in words:
                words.append(word)
    processed_words= list(preprocess(words))
    return processed_words


if __name__ == "__main__":
   corpus=open('tweets.txt','r',encoding='utf-8').read()
   mymodel = build_bigram_model(preprocess(corpus.split()))
   opener_words=openers(corpus)
   #generate 10 sentences
   for i in range(0,10):
       generated_sentence=generate_sentence(mymodel, opener_words)
       print ("A randomly generated sentence: ", generated_sentence)
