"""
vll_probabilities
===

We found all relevant processes, now find their relative probabilities.
"""

probs = {  # well, branching ratios, not actually probabilities
    "W": {
        r"$\ell\nu$": 0.3,
        r"$qq$": 0.7
    },
    "Z": {
        r"$\nu\nu$": 0.2,
        r"$\ell\ell$": 0.1,
        r"$qq$": 0.7
    },
    "H": {
        r'$\ell\ell$': 0,  # well pretty much zero for electrons / muons
        r'$gg$': 0.09,
        r'$qq$': 0.60+0.06,  # in particular b-jets and tau tau (which shows up as jets)
        r'$\gamma\gamma$': 0.0001,
        r'$ZqqZqq$': 0.03 * 0.7 * 0.7,
        r'$ZqqZ\ell\ell$': 0.03 * 0.7 * 0.1,
        r'$ZqqZ\nu\nu$': 0.03 * 0.7 * 0.2,
        r'$Z\ell\ellZ\ell\ell$': 0.03 * 0.1 * 0.1,
        r'$Z\ell\ellZ\nu\nu$': 0.03 * 0.1 * 0.2,
        r'$WqqWqq$': 0.21 * 0.7 * 0.7,
        r'$WqqW\ell\nu$': 0.21 * 0.7 * 0.3,
        r'$W\ell\nuW\ell\nu$': 0.21 * 0.3 * 0.3,
    }
}


with open('tables.md', 'r+') as tablefile:
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
            # ideally we'd multiply by the probability of VLL production
            # and by the probabilities of VLL --> boson 1 or 2
            # but we don't know those (as far as I can tell)
            # so take this as a kind of proxy but not the actual probability
            prob = probs[boson1][dp1] * probs[boson2][dp2]
            print(line + f" {prob:.2f} |")
