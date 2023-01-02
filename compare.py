import argparse
import tokenize
import io

'''le levenstein diff between tokenized ver of codes (comments and docstrings ignored, fraction scoring implemented)

1 - codes similar, 0 - codes unsimilar
'''

parser = argparse.ArgumentParser(description='code similarity estimation')
parser.add_argument('indir', type=str, help='directory of codes')
parser.add_argument('outdir', type=str, help='file to dump le estimation')
args = parser.parse_args()

def levenstein(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    current_row = range(n+1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return 1 - current_row[n] / max(len(a), len(b))


def docstringRemoval(a): # must be a list of strings - token exact types
    if a[0] == 'STRING' and a[1] in ['NL','NEWLINE']:
        a = a[2:]
    lst_deleter = []
    for _ in range(1, len(a) - 1):
        if a[_] == 'STRING' and (a[_ - 1] in ['NL','NEWLINE'] or a[_ + 1] in ['NL','NEWLINE']):
            lst_deleter.append([_, _ + 1])
    for _ in lst_deleter:
        a = a[:_[0]] + a[_[1] + 1:]
    return a
    
    
def tokenCheck(a: str, b: str):
    a_, b_ = \
        docstringRemoval([tokenize.tok_name[t.exact_type] for t in tokenize.tokenize(io.BytesIO(a.encode('utf-8')).readline) if tokenize.tok_name[t.exact_type] != 'COMMENT']),\
        docstringRemoval([tokenize.tok_name[t.exact_type] for t in tokenize.tokenize(io.BytesIO(b.encode('utf-8')).readline) if tokenize.tok_name[t.exact_type] != 'COMMENT'])
    return levenstein(a_[1:], b_[1:])


def interface():
    in_, out_ = args.indir, args.outdir
    #in_, out_ = 'input.txt', 'scores.txt'
    with open(in_, 'r') as a:
        lst = []
        q = a.read().split('\n')
        for _ in q:
            x, y = _.split()
            with open(x, 'r') as x_, open(y,'r') as y_:
                w, t = x_.read(), y_.read()
                res = tokenCheck(w, t)
                lst.append(res)
    res_ = '\n'.join(map(str, lst))
    with open(out_, 'w') as b:
        b.write(res_)

interface()
