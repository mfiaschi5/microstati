import pandas as pd
from itertools import combinations
from collections import Counter
import decopose as dec
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

def get_j(S,L,atom):
    electron, orbitals = valence_electrons_and_orbitals(atom)
    if electron == orbitals:
        J = S
    elif electron < orbitals :
        J = abs(L-S)
    else:
        J = abs(L+S)
    return J
        

def find_ground_state_term(pivot_table,atom):
    """
    Trova il termine di stato fondamentale dalla tabella dei microstati
    """
    
    max_ms_col = pivot_table.columns.max()

    
    max_ml_row =find_max_nonzero_index(pivot_table[max_ms_col])
    
    J = 0
    S = abs(max_ms_col)
    L = abs(max_ml_row)
    J = get_j(S,L,atom)
    
    multiplicity = int(2 * S + 1)

    
    term_symbol = get_orbital_symbol(L)

    return f"^{multiplicity}{term_symbol}_{J}"

def term_from_decompose(L,S,atom):
    
    J = get_j(S,L,atom)
    multiplicity = int(2 * S + 1)

    
    term_symbol = get_orbital_symbol(L)
    
    return  f"^{multiplicity}{term_symbol}_{J}"

def get_orbital_symbol(L):
    orbitals = "SPDFGHIKLMNOQRTUVWXYZ"
    if L < len(orbitals):
        return orbitals[int(L)]
    else:
        return "?"


#df_ml_ms, orbital_strings
#pivot_table = ml_ms_counts.pivot(index='M_L', columns='M_S', values='Count').fillna(0)




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

        
        ground_state_term = find_ground_state_term(pivot_table,el)
        
        terms = ""
        
        
        for LS in dec.decompose_matrix(pivot_table.values):
            terms += "   \quad   " + str(term_from_decompose(LS[0],LS[1],el))
            
        
        latex_output += "\\section*{" + str(el) +   " microstates}\n"
        latex_output += "\\subsection*{Tabella microstati}\n"
        latex_output += pivot_table.to_latex()
        latex_output += "\n\\subsection*{Stato fondamentale}\n"
        latex_output += ground_state_term + "\n\n"
        latex_output += "\n\\subsection*{Stati}\n"
        latex_output += "$" + terms + "$" +"\n\n"

    return latex_output



def valence_electrons_and_orbitals(element):
    """
    Calcola il numero di elettroni di valenza e il numero di orbitali degeneri nel guscio di valenza di un elemento dato.
    """
    
    valence_configurations = {
        'H': '1s1', 'He': '1s2',
        'Li': '2s1', 'Be': '2s2', 'B': '2p1', 'C': '2p2', 'N': '2p3', 'O': '2p4', 'F': '2p5', 'Ne': '2p6',
        'Na': '3s1', 'Mg': '3s2', 'Al': '3p1', 'Si': '3p2', 'P': '3p3', 'S': '3p4', 'Cl': '3p5', 'Ar': '3p6',
        'K': '4s1', 'Ca': '4s2', 'Sc': '3d1', 'Ti': '3d2', 'V': '3d3', 'Cr': '3d4', 'Mn': '3d5', 'Fe': '3d6', 'Co': '3d7', 'Ni': '3d8', 'Cu': '3d9', 'Zn': '3d10','Ga': '4p1', 'Ge': '4p2', 'As': '4p3', 'Se': '4p4', 'Br': '4p5', 'Kr': '4p6',
        'Rb': '5s1', 'Sr': '5s2', 'Y': '4d1', 'Zr': '4d2', 'Nb': '4d3', 'Mo': '4d4', 'Tc': '4d5', 'Ru': '4d6', 'Rh': '4d7', 'Pd': '4d8', 'Ag': '4d9', 'Cd': '4d10','In': '5p1', 'Sn': '5p2', 'Sb': '5p3', 'Te': '5p4', 'I': '5p5', 'Xe': '5p6',
        'Cs': '6s1', 'Ba': '6s2', 'La': '5d1', 'Ce': '4f1', 'Pr': '4f2', 'Nd': '4f3', 'Pm': '4f4', 'Sm': '4f5', 'Eu': '4f6', 'Gd': '4f7', 'Tb': '4f8', 'Dy': '4f9', 'Ho': '4f10', 'Er': '4f11', 'Tm': '4f12', 'Yb': '4f13', 'Lu': '4f14','Hf': '5d2', 'Ta': '5d3', 'W': '5d4', 'Re': '5d5', 'Os': '5d6', 'Ir': '5d7', 'Pt': '5d8', 'Au': '5d9', 'Hg': '5d10','Tl': '6p1', 'Pb': '6p2', 'Bi': '6p3', 'Po': '6p4','At': '6p5', 'Rn': '6p6',
        'Fr': '7s1', 'Ra': '7s2', 'Ac': '6d1', 'Th': '6d2', 'Pa': '5f2', 'U': '5f3', 'Np': '5f4', 'Pu': '5f6', 'Am': '5f7', 'Cm': '5f7', 'Bk': '5f9', 'Cf': '5f10'

        
    }

    
    def degenerate_orbitals(orbital_type):
        if orbital_type == 's':
            return 1
        elif orbital_type == 'p':
            return 3
        elif orbital_type == 'd':
            return 5
        elif orbital_type == 'f':
            return 7
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
