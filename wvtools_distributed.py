## ---- to include this toolbox:
## ---- sys.path.insert(0, os.path.realpath('/afs/cs/u/wzou/mt/wvtools/'))

import os, sys, numpy
from collections import defaultdict
import random

## ---- general class with tools to process word vectors ----
# - load wvs to numpy nd-array

class wvtools(object): 
    def __init__(self):
        return
    
    def load_wv_file(self, filename): 
        f = open(filename, 'r')
        l = [map(float, line.split(',')) for line in f];
        return numpy.asarray(l)
    
    def loadvocab(self, filename):
        vocab = []
        f = open(filename, 'r')
        while 1:
            line = f.readline()
            if not line:
                break
            vocab.append(unicode(line.split('\n')[0].split(' ')[0], 'utf-8'))
        return vocab
    
    def load_default_vocab(self, lan):
        if lan == 'zh':
            filename = '/afs/cs/u/wzou/lwv/vocab/zh_initial_vocabShrink_1to100000_bkup.txt'
            return self.loadvocab(filename)
        else:
            filename = '/afs/cs/u/wzou/lwv/vocab/en_vocab_default.txt'
            return self.loadvocab(filename)
        
    def load_dict(self, lan): 
        # makes a dictionary of vocab->index [0 start]
        # idx is index to the We matrix
        
        vocab = self.load_default_vocab(lan)
        D = defaultdict()
        for i in range(len(vocab)):
            D[vocab[i]] = i
        return D
    
    def load_wvs(self, lan, exp): 
        filename = '/afs/cs/u/wzou/lwv/best/'+exp+'_'+lan+'.txt'
        return self.load_wv_file(filename)

    def load_wvs_randrange(self, lan, exp, range): 
        id = random.randrange(range)        
        filename = '/afs/cs/u/wzou/lwv/best/'+str(id)+exp+'_'+lan+'.txt'
        return self.load_wv_file(filename)

    def load_wvs_temp(self, lan): 
        filename = '/afs/cs/u/wzou/lwv/best/swap-latest_transpose_'+lan+'.txt'
        #filename = '/afs/cs/u/wzou/lwv/best/'+str(id)+exp+'_'+lan+'.txt'
        return self.load_wv_file(filename).transpose()
    
    def write_matrix(self, filename, M):
        f = open(filename, 'w')
        for r in range(M.shape[0]):
            line = ''
            for c in range(M.shape[1]):
                line = line + str(M[r, c])+','
            line = line[0:-1]
            f.write(line+'\n')
        f.close()

    def write_mfile(self, filename, templatename, varnames, varvalues):
        assert(len(varnames)==len(varvalues))
        fo = open(filename, 'w')
        f = open(templatename, 'r')
        for v in range(len(varnames)):            
            fo.write(str(varnames[v])+'='+str(varvalues[v])+'; \n')
        
        while 1:
            line = f.readline()
            if not line:
                break
            fo.write(line)
        f.close()
        fo.close()
        
    def dec_hash_number(self, number, base, level):
        # simple hashing a number into a hierarchy of folders
        
        a= len(str(number))
        b= len(str(base))
        
        strnum = str(number).zfill(b)
        
        return strnum[0:level]
    
        # return 'level' numbers
        # to indicate which folders the number file goes into
        
    def get_hash_folder(self, filecount, base, level):
        prefix = wvt.dec_hash_number(filecount, base, level)
        folder = ''
        for j in range(len(prefix)):
            folder = folder + prefix[j] + '/'
        return folder
    
    def dict_lookup(self, word, dict):
        if dict.has_key(word):
            return dict[word]
        else:
            return 0
        
