import pickle

model = {}
A = {}
B = {}
viterbi_vector = {}
query = ""
lang = "en"


def read_model():
    with open('./trained_model/HMM_trained_model_'+lang+'.pickle', 'rb') as handle:
        _model = pickle.load(handle)
    A = _model["A"]
    B = _model["B"]
    return A, B


def setup_viterbi():
    _start = query[0]
    for i in B.keys():
        _val = -1
        if _start in B[i]:
            _val = (A["<s>"][i]/A["<s>"]["_total"])
        else:
            _val = (1/A["<s>"]["_total"]+1)
        if _start in viterbi_vector.keys():
            viterbi_vector[_start][i] = {"val": _val, "pre": "<s>"}
        else:
            viterbi_vector[_start] = {i: {"val": _val, "pre": "<s>"}}


def main_viterbi():
    read_model()
    setup_viterbi()
    _temp_key = query[0]
    for q in query[1:]:
        for b in B.keys():
            _max = {}
            for v in viterbi_vector[_temp_key].keys():
                if v not in A.keys() or b not in A[v].keys():
                    continue
                # print(v,b,_temp_key)
                # print(A[v]," ",b)
                _val = -1
                if q in B[b].keys():
                    _val = (B[b][q]/B[b]["_total"])*(A[v][b]/A[v]
                                                      ["_total"])*viterbi_vector[_temp_key][v]["val"]
                else:
                    _val = (1/B[b]["_total"]+1)*(A[v][b]/A[v]
                                                 ["_total"])*viterbi_vector[_temp_key][v]["val"]
                if _max == {} or _val > _max["val"]:
                    _max = {"val": _val, "pre": v}
                    if q in viterbi_vector.keys():
                        viterbi_vector[q][b] = _max
                    else:
                        viterbi_vector[q] = {b: _max}
        _temp_key = q


def output():
    _output = []
    _max_temp = -1
    _max_v = ''
    q = query[::-1][0]
    query.pop()
    for v in viterbi_vector[q].keys():
        if _max_temp == -1 or viterbi_vector[q][v]["val"] > _max_temp["val"]:
            _max_temp = viterbi_vector[q][v]
            _max_v = v
    _output.append({q: _max_v})
    k = _max_temp["pre"]
    for qe in query[::-1]:
        _output.append({qe: k})
        k = viterbi_vector[qe][k]["pre"]
    print(_output[::-1])


query = "but you must have heard it said that the drawing-room disappeared forever with the somnolent years of James and the antic heyday of Coward .".split(
    ' ')
A, B = read_model()
main_viterbi()
# setup_viterbi()
output()
