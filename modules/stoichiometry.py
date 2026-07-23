"""
Stoichiometry & Analytical Chemistry Module
-------------------------------------------
This module handles calculations related to chemical formulas and reaction analytics.
Calculators included:
1. Molar Mass: Parses formulas (e.g., H2O, Ca(OH)2, (NH4)2SO4) and sums atomic masses.
2. pH & pOH: Computes pH, pOH, [H+], and [OH-] concentrations.
3. Percentage Yield: Calculates reaction efficiency.
4. Equivalent Weight: Molar Mass / n-factor (valence/acidity/basicity).
"""

import math
import re

# Comprehensive list of standard elements and their atomic weights
ATOMIC_MASSES = {
    "H": 1.008, "He": 4.0026, "Li": 6.94, "Be": 9.0122, "B": 10.81, "C": 12.011,
    "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180, "Na": 22.990, "Mg": 24.305,
    "Al": 26.982, "Si": 28.085, "P": 30.974, "S": 32.06, "Cl": 35.45, "Ar": 39.948,
    "K": 39.098, "Ca": 40.078, "Sc": 44.956, "Ti": 47.867, "V": 50.942, "Cr": 51.996,
    "Mn": 54.938, "Fe": 55.845, "Co": 58.933, "Ni": 58.693, "Cu": 63.546, "Zn": 65.38,
    "Ga": 69.723, "Ge": 72.630, "As": 74.922, "Se": 78.971, "Br": 79.904, "Kr": 83.798,
    "Rb": 85.468, "Sr": 87.62, "Y": 88.906, "Zr": 91.224, "Nb": 92.906, "Mo": 95.95,
    "Tc": 98.0, "Ru": 101.07, "Rh": 102.91, "Pd": 106.42, "Ag": 107.87, "Cd": 112.41,
    "In": 114.82, "Sn": 118.71, "Sb": 121.76, "Te": 127.60, "I": 126.90, "Xe": 131.29,
    "Cs": 132.91, "Ba": 137.33, "La": 138.91, "Ce": 140.12, "Pr": 140.91, "Nd": 144.24,
    "Pm": 145.0, "Sm": 150.36, "Eu": 151.96, "Gd": 157.25, "Tb": 158.93, "Dy": 162.50,
    "Ho": 164.93, "Er": 167.26, "Tm": 168.93, "Yb": 173.05, "Lu": 174.97, "Hf": 178.49,
    "Ta": 180.95, "W": 183.84, "Re": 186.21, "Os": 190.23, "Ir": 192.22, "Pt": 195.08,
    "Au": 196.97, "Hg": 200.59, "Tl": 204.38, "Pb": 207.2, "Bi": 208.98, "Po": 209.0,
    "At": 210.0, "Rn": 222.0, "Fr": 223.0, "Ra": 226.0, "Ac": 227.0, "Th": 232.04,
    "Pa": 231.04, "U": 238.03
}

def parse_chemical_formula(formula: str) -> dict:
    """
    Parses a chemical formula string (e.g. H2O, Ca(OH)2, (NH4)2SO4)
    and returns a dictionary of element counts, e.g. {"C": 6, "H": 12, "O": 6}.
    Uses a stack to correctly handle nested parenthetical groups.
    """
    # Clean whitespace and validate brackets
    formula = formula.strip().replace(" ", "")
    if not formula:
        raise ValueError("Formula string cannot be empty.")
    if formula.count('(') != formula.count(')'):
        raise ValueError("Mismatched parentheses in chemical formula.")
    
    # Tokenize formula. 
    # [A-Z][a-z]* captures elements (capital letter + optional lower letters)
    # \( and \) capture parentheses
    # \d+ captures numbers (multipliers)
    tokens = re.findall(r'([A-Z][a-z]*|\(|\)|\d+)', formula)
    
    # Re-verify that total characters captured match the formula length
    # to catch illegal characters like special symbols or lowercase starts
    total_token_len = sum(len(t) for t in tokens)
    if total_token_len != len(formula):
        raise ValueError("Formula contains invalid characters or elements must start with capital letters.")

    stack = [{}]
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if token == '(':
            # Push a new level on the stack for the subgroup
            stack.append({})
            i += 1
        elif token == ')':
            # Check if there is an outer multiplier following the parenthesis
            multiplier = 1
            if i + 1 < len(tokens) and tokens[i+1].isdigit():
                multiplier = int(tokens[i+1])
                i += 2  # skip ')' and the number token
            else:
                i += 1  # skip ')'
            
            # Pop the nested group and merge it with the level below
            nested_group = stack.pop()
            for element, count in nested_group.items():
                stack[-1][element] = stack[-1].get(element, 0) + count * multiplier
        elif token.isdigit():
            # Numbers should only follow elements or parentheses
            raise ValueError(f"Syntax error: number '{token}' is out of place.")
        else:
            # Token is an element name
            element = token
            if element not in ATOMIC_MASSES:
                raise ValueError(f"Unknown chemical element: '{element}'")
                
            # Check if element has a count suffix
            multiplier = 1
            if i + 1 < len(tokens) and tokens[i+1].isdigit():
                multiplier = int(tokens[i+1])
                i += 2  # skip element and the number token
            else:
                i += 1  # skip element
            
            stack[-1][element] = stack[-1].get(element, 0) + multiplier
            
    # The bottom dictionary on the stack holds the final parsed count
    return stack[0]

def calculate_molar_mass(formula: str) -> dict:
    """
    Calculates the molar mass of a chemical formula in g/mol.
    Returns the total mass and a step-by-step breakdown.
    """
    element_counts = parse_chemical_formula(formula)
    
    total_mass = 0.0
    steps = []
    
    # Calculate mass contribution for each element
    for element, count in sorted(element_counts.items()):
        atomic_weight = ATOMIC_MASSES[element]
        contribution = count * atomic_weight
        total_mass += contribution
        steps.append(
            f"{element}: {count} atoms × {atomic_weight} g/mol = {contribution:.4f} g/mol"
        )
        
    steps.append(f"Total Molar Mass = {total_mass:.4f} g/mol")
    
    return {
        "result": total_mass,
        "element_counts": element_counts,
        "steps": steps
    }

def calculate_ph_poh(value: float, input_type: str) -> dict:
    """
    Calculates pH, pOH, [H+] and [OH-] based on one input parameter.
    Available input_types: 'pH', 'pOH', 'H', 'OH'
    Where 'H' = [H+] in M, and 'OH' = [OH-] in M.
    Uses:
    - pH + pOH = 14
    - pH = -log10([H+])
    - [H+] = 10^(-pH)
    - [OH-] = 10^(-pOH)
    """
    if value <= 0:
        raise ValueError("Input value must be greater than 0.")
        
    steps = []
    
    if input_type == "pH":
        ph = value
        poh = 14.0 - ph
        h_conc = 10 ** (-ph)
        oh_conc = 10 ** (-poh)
        steps = [
            f"Input value: pH = {ph}",
            f"1. Calculate pOH: pOH = 14 - pH = 14 - {ph} = {poh:.4f}",
            f"2. Calculate [H+]: [H+] = 10^(-pH) = 10^(-{ph}) = {h_conc:.4e} M",
            f"3. Calculate [OH-]: [OH-] = 10^(-pOH) = 10^(-{poh:.2f}) = {oh_conc:.4e} M"
        ]
        
    elif input_type == "pOH":
        poh = value
        ph = 14.0 - poh
        h_conc = 10 ** (-ph)
        oh_conc = 10 ** (-poh)
        steps = [
            f"Input value: pOH = {poh}",
            f"1. Calculate pH: pH = 14 - pOH = 14 - {poh} = {ph:.4f}",
            f"2. Calculate [H+]: [H+] = 10^(-pH) = 10^(-{ph:.2f}) = {h_conc:.4e} M",
            f"3. Calculate [OH-]: [OH-] = 10^(-pOH) = 10^(-{poh}) = {oh_conc:.4e} M"
        ]
        
    elif input_type == "H":
        h_conc = value
        ph = -math.log10(h_conc)
        poh = 14.0 - ph
        oh_conc = 10 ** (-poh)
        steps = [
            f"Input value: [H+] = {h_conc:.4e} M",
            f"1. Calculate pH: pH = -log10([H+]) = -log10({h_conc:.4e}) = {ph:.4f}",
            f"2. Calculate pOH: pOH = 14 - pH = 14 - {ph:.4f} = {poh:.4f}",
            f"3. Calculate [OH-]: [OH-] = 10^(-pOH) = 10^(-{poh:.2f}) = {oh_conc:.4e} M"
        ]
        
    elif input_type == "OH":
        oh_conc = value
        poh = -math.log10(oh_conc)
        ph = 14.0 - poh
        h_conc = 10 ** (-ph)
        steps = [
            f"Input value: [OH-] = {oh_conc:.4e} M",
            f"1. Calculate pOH: pOH = -log10([OH-]) = -log10({oh_conc:.4e}) = {poh:.4f}",
            f"2. Calculate pH: pH = 14 - pOH = 14 - {poh:.4f} = {ph:.4f}",
            f"3. Calculate [H+]: [H+] = 10^(-pH) = 10^(-{ph:.2f}) = {h_conc:.4e} M"
        ]
    else:
        raise ValueError("Invalid input type selection.")
        
    return {
        "pH": ph,
        "pOH": poh,
        "H": h_conc,
        "OH": oh_conc,
        "steps": steps
    }

def calculate_percent_yield(actual: float, theoretical: float) -> dict:
    """
    Calculates the percentage yield of a chemical reaction.
    Formula: Percent Yield = (Actual Yield / Theoretical Yield) * 100
    """
    if actual < 0 or theoretical <= 0:
        raise ValueError("Actual yield must be positive, and theoretical yield must be greater than 0.")
    if actual > theoretical:
        # Note: sometimes impurities or moisture can make actual yield > theoretical, but we should inform the user
        warning = True
    else:
        warning = False
        
    pct_yield = (actual / theoretical) * 100
    
    steps = [
        "Formula: Percentage Yield = (Actual Yield / Theoretical Yield) * 100",
        f"Calculation: ({actual} / {theoretical}) * 100 = {pct_yield:.2f}%",
        f"Percentage Yield = {pct_yield:.2f}%"
    ]
    
    return {
        "result": pct_yield,
        "steps": steps,
        "exceeds_theoretical": warning
    }

def calculate_equivalent_weight(molar_mass: float, n_factor: float) -> dict:
    """
    Calculates the equivalent weight of a substance.
    Formula: Equivalent Weight = Molar Mass / n-factor (valency, charge, acidity, basicity)
    """
    if molar_mass <= 0:
        raise ValueError("Molar mass must be greater than 0.")
    if n_factor <= 0:
        raise ValueError("n-factor (valency) must be greater than 0.")
        
    eq_weight = molar_mass / n_factor
    
    steps = [
        "Formula: Equivalent Weight = Molar Mass / n-factor (equivalence factor)",
        f"Calculation: {molar_mass} g/mol / {n_factor} = {eq_weight:.4f} g/eq",
        f"Equivalent Weight = {eq_weight:.4f} g/eq"
    ]
    
    return {
        "result": eq_weight,
        "steps": steps
    }
