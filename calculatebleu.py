# Author : Shivankur Kapoor
# Date : 01-05-2016

from __future__ import division
import math
import sys
import os
import re

reload(sys)
sys.setdefaultencoding('utf-8')

def genNgram(str,n):
    tokens = str.split()
    return zip(*[tokens[i:] for i in range(n)])

def calcNgramMap(str,n):
    ngrams = genNgram(str,n)
    ngramMap = {}
    for ngram in ngrams:
        if ngram in ngramMap:
            ngramMap[ngram] += 1
        else:
            ngramMap[ngram] = 1
    return ngramMap


def calcPn(candidateList,referenceList,n):

    den = 0
    num = 0

    for i in range(len(candidateList)):
        candidate = candidateList[i]
        curr_references = []

        for reference in referenceList:
            curr_references.append(reference[i])

        candidateNGramMap = calcNgramMap(candidate,n)
        referenceNGramMaps = []

        for curr_reference in curr_references:
            referenceNGramMaps.append(calcNgramMap(curr_reference,n))

        count = 0
        for key in candidateNGramMap.keys():
            nGramCount = candidateNGramMap[key]
            den += candidateNGramMap[key]
            max_Ref_Count = 0
            for map in referenceNGramMaps:
                if key in map:
                    max_Ref_Count = max(map[key],max_Ref_Count)
            count += min(nGramCount,max_Ref_Count)
        num += count

    if num == 0:
        num = 1
    pn = float(num)/float(den)
    return pn

def calcBP(candidateList, referenceList):
    r = 0
    c = 0

    for i in range(len(candidateList)):
      closestMatch = 0
      min = 999999
      c += len(candidateList[i].split())
      sum = 0

      for each in referenceList:
          sum += len(each[i].split())
      avgLen = float(sum)/float(len(referenceList))

      for each in referenceList:
          curr = len(each[i].split())
          if abs(len(candidateList[i].split()) - curr) < min:
                 closestMatch = curr
          elif abs(len(candidateList[i].split()) - curr) == min:
              if abs(curr - avgLen) < abs(closestMatch - avgLen):
                 closestMatch = curr
          min = abs(len(candidateList[i].split()) - curr)
      r += closestMatch

    if c > r:
        bp = 1
    else:
        bp = math.exp(1-(float(r)/float(c)))
    return bp

if __name__ == '__main__':

    candidateFile = sys.argv[1]
    referenceDirectory = sys.argv[2]
    candidateList = []
    with open(candidateFile,'r') as input:
        for line in input.readlines():
            ##line = re.sub(r'[^\w\s]','',line)
            ##line = re.sub('\n','',line)
            candidateList.append(line.strip())


    referenceList = []
    if os.path.isdir(referenceDirectory):
        for root, directories, filenames in os.walk(referenceDirectory):
            for filename in filenames:
                list = []
                with open(os.path.join(root,filename),'r') as input:
                    for line in input.readlines():
                       ##line = re.sub(r'[^\w\s]','',line)
                       ##line = re.sub('\n','',line)
                       list.append(line.strip())
                referenceList.append(list)

    else:
        list = []
        with open(referenceDirectory,'r') as input:
            for line in input.readlines():
                ##line = re.sub(r'[^\w\s]','',line)
                ##line = re.sub('\n','',line)
                list.append(line.strip())
        referenceList.append(list)

    pn_list = []
    for n in range(1,5):
       pn_list.append(calcPn(candidateList,referenceList,n))

    bp = calcBP(candidateList,referenceList)
    weight = [0.25,0.25,0.25,0.25]

    val = 0
    for i in range(0, len(pn_list)):
        val += weight[i]*math.log(pn_list[i])
    BLEU = bp*math.exp(val)

    with open('bleu_out.txt','w') as outputfile:
        outputfile.write(str(BLEU))
    print 'BP ' + str(bp) + '\n'
    print 'BLEU ' + str(BLEU) + '\n'
