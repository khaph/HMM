
import pickle
import os
import sys

A = {}
B = {}
labels = {}
texts = {}
path = './dataset/vn'

def draw_progress_bar(title, percent, barLen=20):
    sys.stdout.write("\r"+title)
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "#"
        else:
            progress += "="
    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()


def dataset_analyze():
    files = os.listdir(path)
    _sum = len(files)
    _count = 0
    _count_file = 0
    _sum_sen = 0
    _sum_word = 0
    for filename in files:
        if _count_file == 80:
            break
        _count_file += 1
        draw_progress_bar("Init A, B: ", _count/_sum)
        _count += 1
        _f = open(path + "/" + filename, 'r')
        lines = _f.readlines()
        data = ' '.join(list(lines)).replace("\n",'').split(' ')
        _sum_sen += len([i for i in data if i == "./."])
        _sum_word += len(data)
        mem = "<s>"
        labels[mem] = 1
        for s in data:
            s = s.split('/')
            if len(s) < 2:
                break
            _temp1 = s[0]
            _temp2 = s[1]
            # print(_temp1,_temp2)
            # print(_temp1,_temp2)
            if _temp1 != '.':
                labels[_temp2] = 1
                texts[_temp1] = 1
            # generate A
            if _temp2 == '.':
                mem = "<s>"
            else:
                if mem in A.keys():
                    if _temp2 in A[mem].keys():
                        A[mem][_temp2] += 1
                    else:
                        A[mem][_temp2] = 1
                else:
                    A[mem] = {_temp2: 1}

                # generate B
                if _temp2 in B.keys():
                    if _temp1 in B[_temp2].keys():
                        B[_temp2][_temp1] += 1
                    else:
                        B[_temp2][_temp1] = 1
                else:
                    B[_temp2] = {_temp1: 1}
                
                mem = _temp2
        _f.close()

    return _sum_sen, _sum_word

def smoothy():
    _t = len(labels)
    _sum = _t*(_t-1)
    _count = 1
    for l in labels:
        draw_progress_bar("Smoothing: ", _count/_sum)
        _count += _t
        for k in labels:
            if k != "<s>":
                if l in A.keys():
                    if k in A[l].keys():
                        A[l][k] += 1
                    else:
                        A[l][k] = 1
                else:
                    A[l] = {k: 1}
        if l != "<s>":
            for s in texts:
                if l in B.keys():
                    if s in B[l].keys():
                        B[l][s] += 1
                    else:
                        B[l][s] = 1
                else:
                    B[l] = {s: 1}

def count_sum():
    for i in A:
        _sum = 0
        for j in A[i]:
            _sum += A[i][j]
        A[i]["_total"] = _sum

    for i in B:
        _sum = 0
        for j in B[i]:
            _sum += B[i][j]
        B[i]["_total"] = _sum


def generate_model():
    model = {}
    model['A'] = A
    model['B'] = B
    with open('./trained_model/HMM_trained_model_'+path[len(path)-2:]+'.pickle', 'wb') as handle:
        pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)


_sen, _word = dataset_analyze()
smoothy()
count_sum()
generate_model()
print("\nSum of labels: ",len(B), "\nSum of words: ", _word, "\nSum of sen: ", _sen)