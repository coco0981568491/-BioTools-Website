import numpy as np
import pandas as pd
import re
from io import BytesIO
from io import StringIO

def findNPosBySequon(seq):

    # seq preprocessing
    if '>' in seq:
        seq = seq.split('\n')[1:] # get rid of the name section
        seq = ''.join(re.findall(r'(?i)[a-z]', ''.join(seq))) # get rid of the possible ending w/ *
    else:
        seq = ''.join(re.findall(r'(?i)[a-z]', seq)) # get rid of the possible ending w/ *

    # find sequon and n pos
    pattern = '(?i)(N[ARNDBCEQZGHILKMFSTWYV]T)|(N[ARNDBCEQZGHILKMFSTWYV]S)'
    npos = [m.start(0)+1 for m in re.finditer(pattern, seq)]
    sequon = [seq[m.start(0):m.start(0)+3] for m in re.finditer(pattern, seq)]
    # Generate dataframe from result
    df = [(npos[i], sequon[i]) for i in range(len(npos))]
    df = pd.DataFrame(df)
    df.columns = ['N-site', 'Sequon']
    b = BytesIO()
    writer = pd.ExcelWriter(b, engine='xlsxwriter')
    df.to_excel(writer, header=True, index=False)
    writer.save()

    return b

def alp_cutter(seq):

    # seq preprocessing
    if '>' in seq:
        seq = seq.split('\n')[1:] # get rid of the name section
        seq = ''.join(re.findall(r'(?i)[a-z]', ''.join(seq))) # get rid of the possible ending w/ *
    else:
        seq = ''.join(re.findall(r'(?i)[a-z]', seq)) # get rid of the possible ending w/ *

    # cutting sites for α-Lytic Protease
    T_ind = [pos for pos, char in enumerate(seq) if char == 'T' or char == 't'] 
    A_ind = [pos for pos, char in enumerate(seq) if char == 'A' or char == 'a']
    S_ind = [pos for pos, char in enumerate(seq) if char == 'S' or char == 's']
    V_ind = [pos for pos, char in enumerate(seq) if char == 'V' or char == 'v']

    a = set(T_ind).union(A_ind).union(S_ind).union(V_ind)
    a = list(a)
    a.sort() #cutting site result
    #all add one to cut the fragments.
    a = np.array(a)
    a += 1
    a = list(a)

    frag_lst = [] #store the cutted frag.
    first_frag = seq[0: a[0]]
    frag_lst.append(first_frag)
    for i in range(len(a)):
        if i != (len(a) -1): #last index recorded.
            frag = seq[a[i]:a[i +1]]
            frag_lst.append(frag)
        elif i == (len(a) -1):
            #last frag
            frag = seq[a[i]:]
            frag_lst.append(frag)

    frag_len = [len(j) for j in frag_lst]
    cleavage_site = list(np.cumsum(frag_len))

    # Generate dataframe from list and write to xlsx.
    frag_data = [(cleavage_site[i], frag_lst[i], frag_len[i]) for i in range(len(frag_lst))]
    frag_df = pd.DataFrame(frag_data)
    frag_df.columns = ['Position of cleavage site', 'Resulting peptide sequence', 'Peptide length [aa]']

    b = BytesIO()
    writer = pd.ExcelWriter(b, engine='xlsxwriter')
    frag_df.to_excel(writer, header=True, index=False)
    writer.save()

    return b

def findPotentialOPos(seq):

    # seq preprocessing
    if '>' in seq:
        seq = seq.split('\n')[1:] # get rid of the name section
        seq = ''.join(re.findall(r'(?i)[a-z]', ''.join(seq))) # get rid of the possible ending w/ *
    else:
        seq = ''.join(re.findall(r'(?i)[a-z]', seq)) # get rid of the possible ending w/ *

    # find o pos & numbered results
    opos = [m.start(0)+1 for m in re.finditer(r'(?i)(s)|(t)', seq)]
    st = [seq[m.start(0)] for m in re.finditer(r'(?i)(s)|(t)', seq)]
    # Generate dataframe from result
    df = [(st[i], opos[i]) for i in range(len(opos))]
    df = pd.DataFrame(df)
    df.columns = ['S/T', 'Potential O-glycan Sites']
    b = BytesIO()
    writer = pd.ExcelWriter(b, engine='xlsxwriter')
    df.to_excel(writer, header=True, index=False)
    writer.save()

    return b

def GlycamToPDB(file):
    with open(file, 'r') as f:
        content = f.read()
        # SPECIAL PAIRS: mods made to atm if nag is resi
        content_altered = re.sub('C2N (0YB|4YB|UYA|UYB)', 'C7  NAG', content, flags = re.M)
        content_altered = re.sub('O2N (0YB|4YB|UYA|UYB)', 'O7  NAG', content_altered, flags = re.M)
        content_altered = re.sub('CME (0YB|4YB|UYA|UYB)', 'C8  NAG', content_altered, flags = re.M)
        # SPECIAL PAIRS: mods made to atm if sia is resi
        content_altered = re.sub('CME 0SA', 'C11 SIA', content_altered, flags = re.M)
        # rest of the atm name changes
        content_altered = re.sub('O5N', 'O10', content_altered, flags = re.M)
        content_altered = re.sub('C5N', 'C10', content_altered, flags = re.M)
        # rest of the resi name changes (-> NAG)
        content_altered = re.sub('0YB|4YB|UYA|UYB', 'NAG', content_altered, flags = re.M)
        # (-> BMA)
        content_altered = re.sub('VMB', 'BMA', content_altered, flags = re.M)
        # (-> MAN)
        content_altered = re.sub('(V|X|Y|0|2|4)MA', 'MAN', content_altered, flags = re.M)
        # (-> GAL)
        content_altered = re.sub('(0|6)LB', 'GAL', content_altered, flags = re.M)
        # (-> FUC)
        content_altered = re.sub('0fA', 'FUC', content_altered, flags = re.M)
        # (-> HIS)
        content_altered = re.sub('HIE', 'HIS', content_altered, flags = re.M)
        # (-> CYS)
        content_altered = re.sub('CYX', 'CYS', content_altered, flags = re.M)
        # (-> SIA)
        content_altered = re.sub('0SA', 'SIA', content_altered, flags = re.M)

    output = StringIO()
    output.write(content_altered)
    output.close()

    return output