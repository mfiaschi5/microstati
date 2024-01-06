import pandas as pd
from itertools import combinations
from collections import Counter
""" 
Il seguente file non è commentato perché l'autore non aveva voglia, se avete voglia voi inviate la richiesta per il commit :)
"""

def generate_orbital_strings(n_electrons, n_orbitals=2):
    """
    Genera tutte le possibili stringhe di occupazione per una data configurazione
    
    """
    
    electron_positions = combinations(range(n_orbitals * 2), n_electrons)

    
    orbital_strings = []
    for positions in electron_positions:
        string = ['0'] * n_orbitals * 2  
        for pos in positions:
            string[pos] = '1'  
        orbital_strings.append(''.join(string))

    return orbital_strings

def calculate_ML_MS(orbital_string):
    """
    Calcola M_L and M_S per una stringa di occupazione
    """
    M_L = M_S = 0
    for i, state in enumerate(orbital_string):
        if state == '1':
            orbital_number = i // 2  
            electron_spin = 0.5 if i % 2 == 0 else -0.5  
            M_L += orbital_number - (len(orbital_string) // 4)  
            M_S += electron_spin
    return M_L, M_S


n_electrons = 3  
n_orbitals = 5  


orbital_strings = generate_orbital_strings(n_electrons, n_orbitals)


ml_ms_values = [calculate_ML_MS(string) for string in orbital_strings]
ml_ms_dicts = [{'M_L': ml_ms[0], 'M_S': ml_ms[1]} for ml_ms in ml_ms_values]


df_ml_ms = pd.DataFrame(ml_ms_dicts)


ml_ms_counts = df_ml_ms.value_counts().reset_index(name='Count')

ml_ms_counts.sort_values(by=['M_L', 'M_S'], inplace=True)
ml_ms_counts

def find_max_nonzero_index(column):
    """
    Funzione che trova il valore diverso da zero con indice più grande
    """
    
    nonzero_indices = column[column != 0].index
    if not nonzero_indices.empty:
        return max(nonzero_indices)
    else:
        return None


def find_ground_state_term(pivot_table):
    """
    Trova il termine di stato fondamentale dalla tabella dei microstati
    """
    
    max_ms_col = pivot_table.columns.max()

    
    max_ml_row =find_max_nonzero_index(pivot_table[max_ms_col])
    
    
    S = abs(max_ms_col) 
    L = abs(max_ml_row)

    
    multiplicity = int(2 * S + 1)

    
    term_symbol = get_orbital_symbol(L)

    return f"{multiplicity}{term_symbol}"




def get_orbital_symbol(L):
    orbitals = "SPDFGHIKLMNOQRTUVWXYZ"
    if L < len(orbitals):
        return orbitals[int(L)]
    else:
        return "?"


df_ml_ms, orbital_strings
pivot_table = ml_ms_counts.pivot(index='M_L', columns='M_S', values='Count').fillna(0)

print((pivot_table))
print(find_ground_state_term(pivot_table))

def generate_latex_output(elements):
    """
    Genera il testo in LaTeX per tabella microstati e stato fondamentale
    """
    latex_output = ""
    n_electrons_list = []
    n_orbitals_list = [] 

    for element in elements:
        electrons,orbitals= valence_electrons_and_orbitals(element)
        n_electrons_list.append(electrons)
        n_orbitals_list.append(orbitals)


    for n_electrons, n_orbitals, el in zip(n_electrons_list, n_orbitals_list,elements):

        orbital_strings = generate_orbital_strings(n_electrons, n_orbitals)
        ml_ms_values = [calculate_ML_MS(string) for string in orbital_strings]

 
        ml_ms_dicts = [{'M_L': ml_ms[0], 'M_S': ml_ms[1]} for ml_ms in ml_ms_values]
        df_ml_ms = pd.DataFrame(ml_ms_dicts)


        ml_ms_counts = df_ml_ms.value_counts().reset_index(name='Count')
        ml_ms_counts.sort_values(by=['M_L', 'M_S'], inplace=True)


        pivot_table = ml_ms_counts.pivot(index='M_L', columns='M_S', values='Count').fillna(0)


        ground_state_term = find_ground_state_term(pivot_table)


        latex_output += "\\section*{" + str(el) +   " microstates}\n"
        latex_output += "\\subsection*{Tabella microstati}\n"
        latex_output += pivot_table.to_latex()
        latex_output += "\n\\subsection*{Stato fondamentale}\n"
        latex_output += ground_state_term + "\n\n"

    return latex_output



def valence_electrons_and_orbitals(element):
    """
    Calcola il numero di elettroni di valenza e il numero di orbitali degeneri nel guscio di valenza di un elemento dato.
    """
    
    valence_configurations = {
        'H': '1s1', 'He': '1s2',
        'Li': '2s1', 'Be': '2s2', 'B': '2p1', 'C': '2p2', 'N': '2p3', 'O': '2p4', 'F': '2p5', 'Ne': '2p6',
        'Na': '3s1', 'Mg': '3s2', 'Al': '3p1', 'Si': '3p2', 'P': '3p3', 'S': '3p4', 'Cl': '3p5', 'Ar': '3p6',
        'K': '4s1', 'Ca': '4s2', 'Sc': '3d1', 'Ti': '3d2', 'V': '3d3', 'Cr': '3d4', 'Mn': '3d5', 'Fe': '3d6', 'Co': '3d7', 'Ni': '3d8', 'Cu': '3d9', 'Zn': '3d10',
        
    }

    
    def degenerate_orbitals(orbital_type):
        if orbital_type == 's':
            return 1  # s-orbital (l=0)
        elif orbital_type == 'p':
            return 3  # p-orbital (l=1)
        elif orbital_type == 'd':
            return 5  # d-orbital (l=2)
        elif orbital_type == 'f':
            return 7  # f-orbital (l=3)
        else:
            return 0

    valence_shell = valence_configurations.get(element, '')
    if valence_shell:
        orbital_type = valence_shell[-2]  
        valence_electrons = int(valence_shell[-1])  
        return valence_electrons, degenerate_orbitals(orbital_type)
    else:
        return 0, 0


elements = ['N', 'O', 'Ti','Ni']


latex_output = generate_latex_output(elements)
print(latex_output)
