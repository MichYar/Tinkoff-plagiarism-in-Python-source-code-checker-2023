import argparse
import tokenize

'''le levenstein diff between tokenized ver of codes (comments ignored)

0 - codes similar, many - codes unsimilar
'''

input, output = '', ''
parser = argparse.ArgumentParser(description='code similarity estimation')
parser.add_argument('indir', type=str, help='directory of codes')
parser.add_argument('outdir', type=str, help='file to dump le estimation')
args = parser.parse_args()

def levenstein(a, b) -> int :
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

    return current_row[n]


def tokenCheck(a: str, b: str):
    a_, b_ = [t.exact_type for t in tokenize.generate_tokens(a) if t.exact_type != 'COMMENT'], [t.exact_type for t in tokenize.generate_tokens(b) if t.exact_type != 'COMMENT']
    return levenstein(a_, b_)


def interface():
    in_, out_ = args.indir, args.outdir
    with open(in_, 'r') as a:
        lst = []
        q = a.read().split('\n')
        for _ in q:
            x, y = _.split()
            with open(x, 'r') as x_, open(y,'r') as y_:
                w, t = x_.read(), y_.read()
                res = token_check(w, t)
                lst.append(res)
    res_ = '\n'.join(map(str, res))
    with open(out_, 'w') as b:
        b.write(res_)

interface()
