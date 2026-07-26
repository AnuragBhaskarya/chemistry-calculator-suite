"""
Chemistry Calculators Module
----------------------------
This single file contains all the chemistry math and logic for the application.
It is organized into 3 main sections:
1. Solutions & Concentration Calculators
2. Physical Chemistry & Gas Law Solvers
3. Stoichiometry & Analytical Tools
"""

import math
import re

# ==============================================================================
# SECTION 1: SOLUTIONS & CONCENTRATION CALCULATORS
# ==============================================================================

def calculate_molarity(solute_mass, molar_mass, volume_ml):
    """Calculates Molarity (M) = Moles of Solute / Volume in Liters"""
    if molar_mass <= 0 or volume_ml <= 0:
        raise ValueError("Molar mass and volume must be greater than 0.")
    #calculations for molatity
    moles = solute_mass / molar_mass
    volume_liters = volume_ml / 1000.0
    molarity = moles / volume_liters
    
    #return the results
    return {
        "result": molarity,
        "steps": [
            f"Step 1: Moles of solute = Mass / Molar Mass = {solute_mass} g / {molar_mass} g/mol = {moles:.4f} mol",
            f"Step 2: Convert volume to Liters = {volume_ml} mL / 1000 = {volume_liters:.4f} L",
            f"Step 3: Molarity = Moles / Liters = {moles:.4f} mol / {volume_liters:.4f} L = {molarity:.4f} M"
        ]
    }


def calculate_molality(solute_mass, molar_mass, solvent_mass_g):
    """Calculates Molality (m) = Moles of Solute / Mass of Solvent in kg"""
    if molar_mass <= 0 or solvent_mass_g <= 0:
        raise ValueError("Molar mass and solvent mass must be greater than 0.")
    
    moles = solute_mass / molar_mass
    solvent_kg = solvent_mass_g / 1000.0
    molality = moles / solvent_kg
    
    return {
        "result": molality,
        "steps": [
            f"Step 1: Moles of solute = Mass / Molar Mass = {solute_mass} g / {molar_mass} g/mol = {moles:.4f} mol",
            f"Step 2: Convert solvent mass to kg = {solvent_mass_g} g / 1000 = {solvent_kg:.4f} kg",
            f"Step 3: Molality = Moles / Solvent kg = {moles:.4f} mol / {solvent_kg:.4f} kg = {molality:.4f} m"
        ]
    }


def calculate_normality(molarity, n_factor):
    """Calculates Normality (N) = Molarity * n-factor"""
    if molarity < 0 or n_factor <= 0:
        raise ValueError("Molarity cannot be negative and n-factor must be greater than 0.")
    
    normality = molarity * n_factor
    
    return {
        "result": normality,
        "steps": [
            f"Step 1: Retrieve solution Molarity = {molarity:.4f} M",
            f"Step 2: Identify the n-factor = {n_factor}",
            f"Step 3: Calculate Normality = Molarity * n-factor = {molarity:.4f} M * {n_factor} = {normality:.4f} N"
        ]
    }


def calculate_dilution(m1=None, v1=None, m2=None, v2=None):
    """
    Solves the Dilution equation: M1 * V1 = M2 * V2
    Pass 3 numbers and leave the 1 unknown variable as None.
    """
    provided = [x for x in (m1, v1, m2, v2) if x is not None]
    if len(provided) != 3:
        raise ValueError("Provide exactly three values to solve the dilution equation.")
    
    for val in provided:
        if val <= 0:
            raise ValueError("All input values must be greater than 0.")

    if m1 is None:
        assert m2 is not None and v2 is not None and v1 is not None
        result = (m2 * v2) / v1
        solved_for = "M1"
    elif v1 is None:
        assert m2 is not None and v2 is not None and m1 is not None
        result = (m2 * v2) / m1
        solved_for = "V1"
    elif m2 is None:
        assert m1 is not None and v1 is not None and v2 is not None
        result = (m1 * v1) / v2
        solved_for = "M2"
    else:  # v2 is None
        assert m1 is not None and v1 is not None and m2 is not None
        result = (m1 * v1) / m2
        solved_for = "V2"

    return {
        "result": result,
        "solved_for": solved_for,
        "steps": [
            "Formula: M1 * V1 = M2 * V2",
            f"Solving for {solved_for}: Result = {result:.4f}"
        ]
    }


# ==============================================================================
# SECTION 2: PHYSICAL CHEMISTRY & GAS LAW SOLVERS
# ==============================================================================

def solve_gas_law(p=None, v=None, n=None, t=None):
    """
    Solves Ideal Gas Law: P * V = n * R * T  (where R = 0.0821)
    Pass 3 numbers and leave the 1 unknown variable as None.
    """
    R = 0.0821
    provided = [x for x in (p, v, n, t) if x is not None]
    if len(provided) != 3:
        raise ValueError("Provide exactly three values to solve the gas law.")
    
    for val in provided:
        if val <= 0:
            raise ValueError("Values must be greater than 0 (Temperature in Kelvin).")

    if p is None:
        assert n is not None and t is not None and v is not None
        result = (n * R * t) / v
        solved_for = "Pressure (P)"
    elif v is None:
        assert n is not None and t is not None and p is not None
        result = (n * R * t) / p
        solved_for = "Volume (V)"
    elif n is None:
        assert p is not None and v is not None and t is not None
        result = (p * v) / (R * t)
        solved_for = "Moles (n)"
    else:  # t is None
        assert p is not None and v is not None and n is not None
        result = (p * v) / (n * R)
        solved_for = "Temperature (T)"

    return {
        "result": result,
        "solved_for": solved_for,
        "steps": [
            "Formula: P * V = n * R * T  (R = 0.0821 L·atm/(mol·K))",
            f"Calculated {solved_for} = {result:.4f}"
        ]
    }


def calculate_density(mass=None, volume=None, density=None):
    """
    Solves Density equation: Density = Mass / Volume
    Pass 2 numbers and leave 1 unknown variable as None.
    """
    provided = [x for x in (mass, volume, density) if x is not None]
    if len(provided) != 2:
        raise ValueError("Provide exactly two values to solve the density equation.")
    
    for val in provided:
        if val <= 0:
            raise ValueError("Values must be greater than 0.")

    if density is None:
        assert mass is not None and volume is not None
        result = mass / volume
        solved_for = "Density"
    elif mass is None:
        assert density is not None and volume is not None
        result = density * volume
        solved_for = "Mass"
    else:  # volume is None
        assert mass is not None and density is not None
        result = mass / density
        solved_for = "Volume"

    return {
        "result": result,
        "solved_for": solved_for,
        "steps": [
            "Formula: Density = Mass / Volume",
            f"Calculated {solved_for} = {result:.4f}"
        ]
    }


def convert_units(value, category, from_unit, to_unit):
    """Converts units for Temperature, Pressure, and Volume."""
    cat = category.lower()
    
    if cat == "temperature":
        # 1. Convert input to Kelvin baseline
        if from_unit == "C":
            val_k = value + 273.15
        elif from_unit == "F":
            val_k = (value - 32) * 5 / 9 + 273.15
        else:
            val_k = value
            
        if val_k < 0:
            raise ValueError("Temperature cannot be below Absolute Zero (0 K).")

        # 2. Convert Kelvin baseline to target unit
        if to_unit == "C":
            result = val_k - 273.15
        elif to_unit == "F":
            result = (val_k - 273.15) * 9 / 5 + 32
        else:
            result = val_k

    elif cat == "pressure":
        if value < 0:
            raise ValueError("Pressure cannot be negative.")
        factors = {"atm": 1.0, "kPa": 101.325, "bar": 1.01325, "mmHg": 760.0}
        val_atm = value / factors[from_unit]
        result = val_atm * factors[to_unit]

    elif cat == "volume":
        if value < 0:
            raise ValueError("Volume cannot be negative.")
        factors = {"L": 1.0, "mL": 1000.0, "m3": 0.001}
        val_l = value / factors[from_unit]
        result = val_l * factors[to_unit]

    else:
        raise ValueError(f"Unknown conversion category: {category}")

    return {
        "result": result,
        "steps": [f"Converted {value} {from_unit} to {result:.4f} {to_unit}"]
    }


# ==============================================================================
# SECTION 3: STOICHIOMETRY & ANALYTICAL CHEMISTRY
# ==============================================================================

# Standard atomic weights dictionary
ATOMIC_MASSES = {
    "H": 1.008, "He": 4.0026, "Li": 6.94, "Be": 9.0122, "B": 10.81, "C": 12.011,
    "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180, "Na": 22.990, "Mg": 24.305,
    "Al": 26.982, "Si": 28.085, "P": 30.974, "S": 32.06, "Cl": 35.45, "Ar": 39.948,
    "K": 39.098, "Ca": 40.078, "Fe": 55.845, "Cu": 63.546, "Zn": 65.38, "Ag": 107.87,
    "I": 126.90, "Ba": 137.33, "Au": 196.97, "Pb": 207.2, "U": 238.03
}


def parse_chemical_formula(formula):
    """
    Parses chemical formulas like H2O, Ca(OH)2, or (NH4)2SO4 into atom counts.
    Example: 'Ca(OH)2' -> {'Ca': 1, 'O': 2, 'H': 2}
    """
    formula = formula.strip().replace(" ", "")
    if not formula:
        raise ValueError("Formula string cannot be empty.")
    if formula.count('(') != formula.count(')'):
        raise ValueError("Mismatched parentheses in formula.")
    
    tokens = re.findall(r'([A-Z][a-z]*|\(|\)|\d+)', formula)
    if sum(len(t) for t in tokens) != len(formula):
        raise ValueError("Invalid characters in formula or elements must start with Capital letters.")

    stack = [{}]
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '(':
            stack.append({})
            i += 1
        elif token == ')':
            multiplier = 1
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                multiplier = int(tokens[i + 1])
                i += 2
            else:
                i += 1
            group = stack.pop()
            for elem, count in group.items():
                stack[-1][elem] = stack[-1].get(elem, 0) + count * multiplier
        elif token.isdigit():
            raise ValueError(f"Syntax error: unexpected number '{token}'")
        else:
            elem = token
            if elem not in ATOMIC_MASSES:
                raise ValueError(f"Unknown element: '{elem}'")
            multiplier = 1
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                multiplier = int(tokens[i + 1])
                i += 2
            else:
                i += 1
            stack[-1][elem] = stack[-1].get(elem, 0) + multiplier

    return stack[0]


def calculate_molar_mass(formula):
    """Calculates Molar Mass of a formula in g/mol."""
    atom_counts = parse_chemical_formula(formula)
    total_mass = 0.0
    steps = []
    
    for elem, count in sorted(atom_counts.items()):
        mass = ATOMIC_MASSES[elem]
        subtotal = count * mass
        total_mass += subtotal
        steps.append(f"{elem}: {count} × {mass} g/mol = {subtotal:.4f} g/mol")
        
    steps.append(f"Total Molar Mass = {total_mass:.4f} g/mol")
    
    return {
        "result": total_mass,
        "element_counts": atom_counts,
        "steps": steps
    }


def calculate_ph_poh(value, input_type):
    """Calculates pH, pOH, [H+], and [OH-] given one parameter."""
    if value <= 0:
        raise ValueError("Input value must be greater than 0.")
        
    if input_type == "pH":
        ph = value
        poh = 14.0 - ph
        h_conc = 10 ** (-ph)
        oh_conc = 10 ** (-poh)
    elif input_type == "pOH":
        poh = value
        ph = 14.0 - poh
        h_conc = 10 ** (-ph)
        oh_conc = 10 ** (-poh)
    elif input_type == "H":
        h_conc = value
        ph = -math.log10(h_conc)
        poh = 14.0 - ph
        oh_conc = 10 ** (-poh)
    elif input_type == "OH":
        oh_conc = value
        poh = -math.log10(oh_conc)
        ph = 14.0 - poh
        h_conc = 10 ** (-ph)
    else:
        raise ValueError("Invalid input type selection.")

    return {
        "pH": ph,
        "pOH": poh,
        "H": h_conc,
        "OH": oh_conc,
        "steps": [
            f"pH = {ph:.4f}",
            f"pOH = {poh:.4f}",
            f"[H+] = {h_conc:.4e} M",
            f"[OH-] = {oh_conc:.4e} M"
        ]
    }


def calculate_percent_yield(actual, theoretical):
    """Calculates reaction Percentage Yield = (Actual / Theoretical) * 100%"""
    if actual < 0 or theoretical <= 0:
        raise ValueError("Actual yield must be >= 0 and theoretical yield must be > 0.")
        
    yield_pct = (actual / theoretical) * 100.0
    
    return {
        "result": yield_pct,
        "exceeds_theoretical": actual > theoretical,
        "steps": [
            f"Percentage Yield = ({actual} / {theoretical}) * 100 = {yield_pct:.2f}%"
        ]
    }


def calculate_equivalent_weight(molar_mass, n_factor):
    """Calculates Equivalent Weight = Molar Mass / n-factor"""
    if molar_mass <= 0 or n_factor <= 0:
        raise ValueError("Molar mass and n-factor must be greater than 0.")
        
    eq_weight = molar_mass / n_factor
    
    return {
        "result": eq_weight,
        "steps": [
            f"Equivalent Weight = {molar_mass} g/mol / {n_factor} = {eq_weight:.4f} g/eq"
        ]
    }
