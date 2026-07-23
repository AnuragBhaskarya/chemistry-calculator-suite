"""
Solutions Module
----------------
This module handles all concentration-related chemistry calculations.
Calculators included:
1. Molarity: moles of solute per liter of solution.
2. Molality: moles of solute per kilogram of solvent.
3. Normality: equivalent concentration (molarity * n-factor).
4. Dilution: M1 * V1 = M2 * V2 calculations.
"""

def calculate_molarity(solute_mass: float, molar_mass: float, volume_ml: float) -> dict:
    """
    Calculates Molarity (M) of a solution.
    Formula: Molarity = moles of solute / volume of solution in liters
             moles of solute = mass (g) / molar mass (g/mol)
             volume in liters = volume (mL) / 1000
    """
    if molar_mass <= 0:
        raise ValueError("Molar mass must be greater than 0.")
    if volume_ml <= 0:
        raise ValueError("Volume must be greater than 0.")
    
    # Step 1: Calculate moles of solute
    moles = solute_mass / molar_mass
    
    # Step 2: Convert volume from mL to Liters
    volume_liters = volume_ml / 1000
    
    # Step 3: Calculate molarity
    molarity = moles / volume_liters
    
    # Return both the result and step-by-step work to make it educational
    return {
        "result": molarity,
        "steps": [
            f"Step 1: Calculate moles of solute = Mass / Molar Mass = {solute_mass} g / {molar_mass} g/mol = {moles:.4f} moles",
            f"Step 2: Convert volume to Liters = {volume_ml} mL / 1000 = {volume_liters:.4f} L",
            f"Step 3: Calculate Molarity = Moles / Liters = {moles:.4f} mol / {volume_liters:.4f} L = {molarity:.4f} M"
        ]
    }

def calculate_molality(solute_mass: float, molar_mass: float, solvent_mass_g: float) -> dict:
    """
    Calculates Molality (m) of a solution.
    Formula: Molality = moles of solute / mass of solvent in kilograms
             moles of solute = mass (g) / molar mass (g/mol)
             solvent mass in kg = solvent mass (g) / 1000
    """
    if molar_mass <= 0:
        raise ValueError("Molar mass must be greater than 0.")
    if solvent_mass_g <= 0:
        raise ValueError("Solvent mass must be greater than 0.")
    
    # Step 1: Calculate moles of solute
    moles = solute_mass / molar_mass
    
    # Step 2: Convert solvent mass from grams to kilograms
    solvent_kg = solvent_mass_g / 1000
    
    # Step 3: Calculate molality
    molality = moles / solvent_kg
    
    return {
        "result": molality,
        "steps": [
            f"Step 1: Calculate moles of solute = Mass / Molar Mass = {solute_mass} g / {molar_mass} g/mol = {moles:.4f} moles",
            f"Step 2: Convert solvent mass to kg = {solvent_mass_g} g / 1000 = {solvent_kg:.4f} kg",
            f"Step 3: Calculate Molality = Moles / Solvent kg = {moles:.4f} mol / {solvent_kg:.4f} kg = {molality:.4f} mol/kg (m)"
        ]
    }

def calculate_normality(molarity: float, n_factor: float) -> dict:
    """
    Calculates Normality (N) of a solution.
    Formula: Normality = Molarity * n-factor
    Where n-factor represents:
    - Basicity for acids (number of H+ ions released, e.g., HCl = 1, H2SO4 = 2)
    - Acidity for bases (number of OH- ions released, e.g., NaOH = 1, Ca(OH)2 = 2)
    - Valence/charge of ions for salts (e.g., NaCl = 1, CaCl2 = 2)
    """
    if molarity < 0:
        raise ValueError("Molarity cannot be negative.")
    if n_factor <= 0:
        raise ValueError("n-factor (valence/acidity/basicity) must be greater than 0.")
        
    normality = molarity * n_factor
    
    return {
        "result": normality,
        "steps": [
            f"Step 1: Retrieve Molarity of the solution = {molarity:.4f} M",
            f"Step 2: Identify the n-factor (equivalence factor) = {n_factor}",
            f"Step 3: Calculate Normality = Molarity * n-factor = {molarity:.4f} M * {n_factor} = {normality:.4f} N"
        ]
    }

def calculate_dilution(m1: float | None = None, v1: float | None = None, m2: float | None = None, v2: float | None = None) -> dict:
    """
    Calculates the unknown variable in a dilution equation: M1 * V1 = M2 * V2
    Provide exactly three variables, leaving the unknown variable as None.
    """
    # Count how many variables are provided (not None)
    provided = [x for x in (m1, v1, m2, v2) if x is not None]
    if len(provided) != 3:
        raise ValueError("Exactly three variables must be provided to solve the dilution equation.")
    
    # Check that provided variables are positive
    for var in provided:
        if var <= 0:
            raise ValueError("All input values must be greater than 0.")

    if m1 is None:
        assert m2 is not None and v2 is not None and v1 is not None
        # Solve for M1: M1 = (M2 * V2) / V1
        result = (m2 * v2) / v1
        steps = [
            "Equation: M1 * V1 = M2 * V2",
            f"Solving for M1: M1 = (M2 * V2) / V1",
            f"Calculation: ({m2} * {v2}) / {v1} = {result:.4f}",
            f"Initial Concentration (M1) = {result:.4f} M"
        ]
        return {"result": result, "solved_for": "M1", "steps": steps}
        
    elif v1 is None:
        assert m2 is not None and v2 is not None and m1 is not None
        # Solve for V1: V1 = (M2 * V2) / M1
        result = (m2 * v2) / m1
        steps = [
            "Equation: M1 * V1 = M2 * V2",
            f"Solving for V1: V1 = (M2 * V2) / M1",
            f"Calculation: ({m2} * {v2}) / {m1} = {result:.4f}",
            f"Initial Volume (V1) = {result:.4f} mL/L"
        ]
        return {"result": result, "solved_for": "V1", "steps": steps}
        
    elif m2 is None:
        assert m1 is not None and v1 is not None and v2 is not None
        # Solve for M2: M2 = (M1 * V1) / V2
        result = (m1 * v1) / v2
        steps = [
            "Equation: M1 * V1 = M2 * V2",
            f"Solving for M2: M2 = (M1 * V1) / V2",
            f"Calculation: ({m1} * {v1}) / {v2} = {result:.4f}",
            f"Final Concentration (M2) = {result:.4f} M"
        ]
        return {"result": result, "solved_for": "M2", "steps": steps}
        
    elif v2 is None:
        assert m1 is not None and v1 is not None and m2 is not None
        # Solve for V2: V2 = (M1 * V1) / M2
        result = (m1 * v1) / m2
        steps = [
            "Equation: M1 * V1 = M2 * V2",
            f"Solving for V2: V2 = (M1 * V1) / M2",
            f"Calculation: ({m1} * {v1}) / {m2} = {result:.4f}",
            f"Final Volume (V2) = {result:.4f} mL/L"
        ]
        return {"result": result, "solved_for": "V2", "steps": steps}

    raise ValueError("Unable to solve dilution equation. Ensure exactly one variable is left blank.")
