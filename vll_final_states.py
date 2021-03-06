"""
vll_final_states
===

We found all possible diagrams. Now go through and final states
"""


with open('info.txt', 'r+') as datafile:
    lines = datafile.readlines()

# data comes in triplets of lines
# line with image file name and number
# line with legend
# line with data
file_lines = lines[0::3]
legend_lines = lines[1::3]
data_lines = lines[2::3]

output_lines = []

# organize data into tables
tables = {}
for file_line, legend_line, data_line in zip(file_lines, legend_lines, data_lines):
    # use first couple characters of file_line to get VLL_decaytype/VLL_type
    vll_decaytype = file_line[:2]
    vll_type = file_line[3:5]
    # make table
    if vll_decaytype not in tables.keys():
        tables[vll_decaytype] = {}
    # make legend line if does not exist
    if vll_type not in tables[vll_decaytype].keys():
        tables[vll_decaytype][vll_type] = [legend_line]
        tables[vll_decaytype][vll_type].append('| --- | --- | --- | --- | --- |')
    else:
        assert legend_line == tables[vll_decaytype][vll_type][0]
    # add data line
    tables[vll_decaytype][vll_type].append(data_line)

# print tables
for vll_decaytype in tables.keys():
    for vll_type in tables[vll_decaytype].keys():
        output_lines.append(f'VLL_decaytype = {vll_decaytype}, VLL_type = {vll_type}')
        output_lines.append('')
        printed = []
        for line in tables[vll_decaytype][vll_type]:
            line = line.replace('\n', '')
            if '---' in line or 'decay' in line:
                output_lines.append(line)
            else:
                stripped = line.replace('|', '').replace('  ', ' ').strip()
                n_l, n_j, n_n, dp1, dp2 = stripped.split()
                potential_line = set([dp1, dp2])
                if potential_line not in printed:
                    output_lines.append(line)
                    printed.append(potential_line)
        output_lines.append('')

output_text = '\n'.join(output_lines)

with open('tables.md', 'w+') as output_file:
    output_file.write(output_text)
