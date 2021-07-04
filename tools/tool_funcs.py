import numpy as np
import pandas as pd
import re
from io import BytesIO
from io import StringIO

def findNPosBySequon(seq):

    # find sequon and n pos
    pattern = '(N[ARNDBCEQZGHILKMFSTWYV]T)|(N[ARNDBCEQZGHILKMFSTWYV]S)'
    ind = [str(m.start(0)+1)+'\n' for m in re.finditer(pattern, seq)]
    s = StringIO() 
    s.writelines(ind)

    return s

def alp_cutter(seq):

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