## ---- to include this toolbox:
## ---- sys.path.insert(0, os.path.realpath('/afs/cs/u/wzou/mt/wvtools/'))

import os, sys, numpy, datetime
from collections import defaultdict
import random
from datetime import datetime

## ---- general class with tools to process word vectors ---- ##

### [Section 1: loading and writing files, vocabulary, word vectors, word indices] ###

# ----- latest used functions for [for debugging] -----
def load_wvs(exp): 
    filename = '/afs/cs/u/wzou/lwv/best/'+exp+'_latest.txt'
    wvs = load_wv_file(filename)
    wvs = wvs.transpose()
    return wvs

def load_dual_wvs(exp):
    # what is this? 
    # ok dual wvs with 100000 zh vocab and 1029* en vocab
    zhwvs = load_wvs(exp)
    enwvs = load_wvs('enWe')
    wvs = numpy.concatenate((zhwvs, enwvs), axis=1)
    return wvs

def load_combined_vocab_debug():
    filename = '/afs/cs/u/wzou/lwv/vocab/zh_initial_vocab_zhen_combined_debug.txt'
    vocab = loadvocab(filename, 'unicode')
    return vocab[0]

def load_combined_dict_debug():
    # load combined vocab, the vocab indices are exactly the postion in the vocabulary list
    vocab = load_combined_vocab_debug()
    print len(vocab)
    D = defaultdict()
    for i in range(len(vocab)):
        D[vocab[i]] = i+1
    return D

# ---- load wvs to numpy nd-array ---- 
def load_wv_file(filename): 
    f = open(filename, 'r')
    l = [map(float, line.split(',')) for line in f];
    return numpy.asarray(l)

def load_latest_wvs(lan, prefix, startv, endv, lamb):
    filename = '/afs/cs/u/wzou/lwv/best/'+lan + '_'+prefix+'_vocab'+str(startv)+'_'+str(endv)+'_lambda'+str(lamb)+'_latest.txt'
    return load_wv_file(filename)

def loadvocab(filename, tokentype):
    vocab = []
    #Vidx = []
    #freq = []
    f = open(filename, 'r')
    while 1:
        line = f.readline()
        if not line:
            break
        if tokentype == 'unicode':
            token =unicode(line.split('\n')[0].split(' ')[0], 'utf-8')
        else:
            token =line.split('\n')[0].split(' ')[0]
        vocab.append(token)
        #Vidx.append(int(line.split('\n')[0].split(' ')[1]))
        #freq.append(int(line.split('\n')[0].split(' ')[2]))
    return [vocab] #[vocab, Vidx, freq]

def load_old_default_vocab(lan):
    if lan == 'zh':
        filename = '/afs/cs/u/wzou/lwv/vocab/zh_initial_vocabShrink_1to100000.txt'
        vocab = loadvocab(filename, 'unicode')
        return vocab[0]
    else:
        filename = '/afs/cs/u/wzou/lwv/vocab/en_vocab_default_full.txt'
        vocab = loadvocab(filename, 'unicode')
        return vocab[0]

def load_old_default_vocab_ZhDict(lan):
    if lan == 'zh':
        filename = '/afs/cs/u/wzou/lwv/vocab/zh_initial_vocabShrink_1to100000.txt'
        vocab = loadvocab(filename, 'str')
        return vocab[0]
    else:
        filename = '/afs/cs/u/wzou/lwv/vocab/en_vocab_default_full.txt'
        vocab = loadvocab(filename, 'str')
        return vocab[0]
    
def load_combined_vocab():
    filename = '/afs/cs/u/wzou/lwv/vocab/bi_reg_vocabShrink_1to100000.txt'
    #zh_initial_vocab_zhen_combined.txt'
    vocab = loadvocab(filename, 'unicode')
    return vocab[0]

def load_default_vocab(lan):
    if lan == 'zh':
        filename = '/afs/cs/u/wzou/lwv/vocab/new_vocab_zh.txt'
        vocab = loadvocab(filename, 'unicode')
        return vocab[0]
    else:
        filename = '/afs/cs/u/wzou/lwv/vocab/new_vocab_en.txt'
        vocab = loadvocab(filename, 'unicode')
        return vocab[0]


def load_default_vocab_ZhDict(lan):
    if lan == 'zh':
        filename = '/afs/cs/u/wzou/lwv/vocab/new_vocab_zh.txt'
        vocab = loadvocab(filename, 'str')
        return vocab[0]
    else:
        filename = '/afs/cs/u/wzou/lwv/vocab/new_vocab_en.txt'
        vocab = loadvocab(filename, 'str')
        return vocab[0]

def load_dict(lan): 
    # makes a dictionary of vocab->index [0 start]
    # Idx is index to the We matrix
    # note that we return 1 starting indices
    
    vocab = load_default_vocab(lan)
    D = defaultdict()
    for i in range(len(vocab)):
        D[vocab[i]] = i+1
    return D

def load_old_dict(lan): 
    # makes a dictionary of vocab->index [0 start]
    # Idx is index to the We matrix
    # note that we return 1 starting indices
    
    vocab = load_old_default_vocab(lan)
    D = defaultdict()
    for i in range(len(vocab)):
        D[vocab[i]] = i+1
    return D

def load_old_combined_dict():
    zhv = load_old_default_vocab('zh')
    env = load_old_default_vocab('en')
    
    old_vocab=zhv+env
    D = defaultdict()
    for i in range(len(old_vocab)):
        D[old_vocab[i]] = i+1
    return D    
    
def load_combined_dict():
    # load combined vocab, the vocab indices are exactly the postion in the vocabulary list
    vocab = load_combined_vocab()
    D = defaultdict()
    for i in range(len(vocab)):
        D[vocab[i]] = i+1
    return D

def load_wvs_zh_en(exp): 
    filename = '/afs/cs/u/wzou/lwv/best/'+exp+'_latest.txt'
    wvs = load_wv_file(filename)
    wvs = wvs.transpose()
    return [wvs[:, 0:99641], wvs[:, 99641:]]
    
def load_wvs_randrange(exp, range):
    id = random.randrange(range)
    filename = '/afs/cs/u/wzou/lwv/best/'+str(id)+exp+'_latest.txt'
    wvs = load_wv_file(filename)
    wvs = wvs.transpose()
    return wvs

# --- reads a file with one column format --- 
def read_column_from_file(fp, method):
    wlist = []
    while 1:
        line = fp.readline()
        if not line: 
            break
        t = line.split('\n')[0]
        if method == 'int' and len(t)>0:
            t = int(t)
        wlist.append(t)
    return wlist

def write_matrix(filename, M):
    f = open(filename, 'w')
    for r in range(M.shape[0]):
        line = ''
        for c in range(M.shape[1]):
            line = line + str(M[r, c])+','
        line = line[0:-1]
        f.write(line+'\n')
    f.close()
    
def write_mfile(filename, templatename, varnames, varvalues):
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
    
def file_write_unicode(file, code):
    file.write(code.encode('utf8'))


### [Section 2: algorithms] ###
# --- the following two numbers are used to hash fold trees ---
def dec_hash_number(number, base, level):
    # simple hashing a number into a hierarchy of folders
    
    a= len(str(number))
    b= len(str(base))
    
    strnum = str(number).zfill(b)
    
    return strnum[0:level]

# return 'level' numbers
# to indicate which folders the number file goes into        
def get_hash_folder(filecount, base, level):
    prefix = wvt.dec_hash_number(filecount, base, level)
    folder = ''
    for j in range(len(prefix)):
        folder = folder + prefix[j] + '/'
    return folder

# --- simple wrapper for dictionary lookup ----
def dict_lookup(word, dict):
    if dict.has_key(word):
        return dict[word]
    else:
        return False

### [Section 3 NLP related] ### 
def get_zh_doc_delims():
    ft = open('/afs/cs/u/wzou/mt/chardata/zh_delim.txt', 'r')
    l = ft.readline()
    p1 = l.split('\n')[0]
    l = ft.readline()
    p2 = l.split('\n')[0]
    return [p1, p2]

# --- write a function to read sentence, 
# --- parse out en, zh, enalign and zhalign 
# --- in vocab index strings 
# --- [see phrasedeepmt.pdf] 
def parse_align_sentence(sentzh, senten, sentA, dict):
    # input:  string sentences, and alignment
    # output: number indexed sentences
    #  - for zh
    #  - for zh-align-en: list of indices hopefully in En vocab, or use self index of the Zh word 
    #  - for en
    #  - for en-align-zh
    
    zhlist = sentzh.strip().split(' ')
    enlist = senten.strip().split(' ')
    Alist = sentA.strip().split(' ')
    numzh = []
    numen = []
    numzh_a_en = []
    numen_a_zh = []
    
    minidict = defaultdict()
    minidictR = defaultdict()
    if len(Alist) > 1:
        for i in range(len(Alist)):
            minidict[int(quick_parse_A(Alist[i])[0])] = int(quick_parse_A(Alist[i])[1])
        for i in range(len(Alist)):
            minidictR[int(quick_parse_A(Alist[i])[1])] = int(quick_parse_A(Alist[i])[0])
    
    for i in range(len(zhlist)):
        zh = unicode(zhlist[i], 'utf8')
        if dict.has_key(zh): 
            nzh = dict[zh]
        else:
            nzh = 1
        numzh.append(nzh)
        nnen = dict_lookup(i, minidict)
        if not nnen:
            nen = nzh
        else:
            enw = enlist[nnen]
            if dict.has_key(enw):
                nen = dict[enw]
            else:
                nen = 1
        
        numzh_a_en.append(nen)
    
    for i in range(len(enlist)):
        en = enlist[i]
        if dict.has_key(en): 
            nen=dict[en]
        else:
            nen = 1
        numen.append(nen)
        nnzh = dict_lookup(i, minidictR)
        if not nnzh:
            nzh = nen
        else: 
            zhw = unicode(zhlist[nnzh], 'utf8')
            if dict.has_key(zhw):
                nzh = dict[zhw]
            else:
                nzh = 1
        
        numen_a_zh.append(nzh)
        
    return [numzh, numzh_a_en, numen, numen_a_zh, minidict, minidictR]

def quick_parse_A(A):
    zh = int(A.split('-')[0])
    en = int(A.split('-')[1])
    return [zh, en]

# --- function that generates a datestring --- 
def generate_datestring(): 
    datestring = unicode(datetime.now()).split('.')[0].replace(' ', '-')
    return datestring

# --- write a function that generates html which display a list of images ---
# def display_image_list_html()

### [Section 4 compute distances] ### 
def comp_cosine_sim(wvzh, wven):
    wvzh = numpy.matrix(wvzh);
    wven = numpy.matrix(wven);
    cossim = wvzh.transpose()*wven/(numpy.sqrt(wvzh.transpose()*wvzh)+1e-10)/(numpy.sqrt(wven.transpose()*wven)+1e-10)
    cossim = float(cossim)
    return cossim

### [Section 5 gorgon submissions] ### 
## implement a function that submits a aset of jobs given a number of sets of parameters
## to run a python script
## to run a matlab script

def write_execute_mfile(dummypath, templatename, varnames, varvalues):
    numtimestr = str(datetime.now()).split('.')[1]
    filename = dummypath + 'mfile'+numtimestr+'.m'
    logname = dummypath + 'logs/log'+numtimestr
    errname = dummypath + 'logs/err'+numtimestr
    matlabcommand = 'mfile'+numtimestr
    write_mfile(filename, templatename, varnames, varvalues)
    os.system('mkdir -p '+dummypath+'logs/')
    ssfilename = dummypath+'ss'+numtimestr+'.sh'
    ss = open(ssfilename,'w')
    ss.write('#!/bin/bash\n')
    ss.write('cd '+dummypath + '\n')
    ss.write('uname -a 1> ' + logname + ' 2>'+ errname+'\n')
    command = 'matlab -nojvm -nodisplay << EOF\n' #1>>' + logname + ' 2>>' + errname + ' << EOF\n'
    ss.write(command)
    ss.write(matlabcommand+'\n');
    ss.write('exit\n')
    ss.write('EOF\n')
    ss.close()
    
    os.system('chmod +x '+ssfilename)
    command = 'sh '+ssfilename
    print command
    os.system(command)

