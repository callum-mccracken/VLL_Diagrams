"""
vll_probabilities
===

We found all relevant processes, now find their relative probabilities.
"""

probs = {
    "W": {
        r"$\ell\nu$": 0.3,
        r"$qq$": 0.7
    },
    "Z": {
        r"$\nu\nu$": 0.2,
        r"$\ell\ell$": 0.1,
        r"$qq$": 0.7
    }
}


with open('tables.txt', 'r+') as tablefile:
    lines = tablefile.readlines()

'''
data looks like this:

VLL_decaytype = WW, VLL_type = LL

| $n_{\ell}$ | $n_{j}$ | $n_{\nu}$ | $W$ decay | $W$ decay |
| --- | --- | --- | --- | --- |
| 2 | 0 | 4 | $\ell\nu$ | $\ell\nu$ |
| 1 | 2 | 3 | $\ell\nu$ | $qq$ |
| 1 | 2 | 3 | $qq$ | $\ell\nu$ |
| 0 | 4 | 2 | $qq$ | $qq$ |

'''

vll_decaytype = None
vll_type = None

total_prob = 0

for line in lines:
    if 'decaytype' in line:
        newline = line.replace(' = ', ' ').replace(',', '')
        _, vll_decaytype, _, vll_type = newline.split()
        boson1, boson2 = vll_decaytype
        print(line, end='')
    else:
        line = line.replace('\n', '')
        if line == '':
            print(line)
        elif 'decay' in line:
            print(line + " prob |")
        elif "---" in line:
            print(line + " --- |")
        else:
            newline = line.replace('|', '').replace('  ', ' ')
            _, _, _, dp1, dp2 = newline.split()
            prob = probs[boson1][dp1] * probs[boson2][dp2]
            total_prob += prob
            print(line + f" {prob:.2f} |")

print('total prob:', total_prob)
# TODO look up how to parse text in a format like formatstring?

