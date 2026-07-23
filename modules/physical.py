"""
Physical Chemistry & Gas Laws Module
------------------------------------
This module handles calculations related to physical properties and gases.
Calculators included:
1. Ideal Gas Law (PV = nRT): solves for P, V, n, or T.
2. Density-Mass-Volume: solves D = M/V for any of the three.
3. Unit Conversions: converts Temperature, Pressure, and Volume units.
"""

def solve_gas_law(p: float | None = None, v: float | None = None, n: float | None = None, t: float | None = None) -> dict:
    """
    Solves the Ideal Gas Law equation: PV = nRT
    Where:
    - P = Pressure in atmospheres (atm)
    - V = Volume in Liters (L)
    - n = Amount of substance in moles (mol)
    - T = Temperature in Kelvin (K)
    - R = Universal Gas Constant = 0.0821 L·atm/(mol·K)
    
    Provide exactly three variables, leaving the unknown variable as None.
    """
    R = 0.0821  # Standard gas constant in L·atm/(mol·K)
    
    # Check that exactly 3 parameters are provided
    provided = [x for x in (p, v, n, t) if x is not None]
    if len(provided) != 3:
        raise ValueError("Exactly three variables must be provided to solve the gas law equation.")
        
    for val in provided:
        if val <= 0:
            raise ValueError("Values must be greater than 0. (Note: Temperature must be in Kelvin, which is > 0 K)")

    if p is None:
        assert n is not None and t is not None and v is not None
        # P = nRT / V
        result = (n * R * t) / v
        steps = [
            "Ideal Gas Equation: P * V = n * R * T",
            "Gas Constant (R) = 0.0821 L·atm/(mol·K)",
            "Solving for Pressure (P): P = (n * R * T) / V",
            f"Calculation: ({n} mol * 0.0821 * {t} K) / {v} L = {result:.4f} atm",
            f"Calculated Pressure = {result:.4f} atm"
        ]
        return {"result": result, "solved_for": "Pressure (P)", "steps": steps}
        
    elif v is None:
        assert n is not None and t is not None and p is not None
        # V = nRT / P
        result = (n * R * t) / p
        steps = [
            "Ideal Gas Equation: P * V = n * R * T",
            "Gas Constant (R) = 0.0821 L·atm/(mol·K)",
            "Solving for Volume (V): V = (n * R * T) / P",
            f"Calculation: ({n} mol * 0.0821 * {t} K) / {p} atm = {result:.4f} L",
            f"Calculated Volume = {result:.4f} L"
        ]
        return {"result": result, "solved_for": "Volume (V)", "steps": steps}
        
    elif n is None:
        assert p is not None and v is not None and t is not None
        # n = PV / RT
        result = (p * v) / (R * t)
        steps = [
            "Ideal Gas Equation: P * V = n * R * T",
            "Gas Constant (R) = 0.0821 L·atm/(mol·K)",
            "Solving for Moles (n): n = (P * V) / (R * T)",
            f"Calculation: ({p} atm * {v} L) / (0.0821 * {t} K) = {result:.4f} mol",
            f"Calculated Moles = {result:.4f} mol"
        ]
        return {"result": result, "solved_for": "Amount of substance (n)", "steps": steps}
        
    elif t is None:
        assert p is not None and v is not None and n is not None
        # T = PV / nR
        result = (p * v) / (n * R)
        steps = [
            "Ideal Gas Equation: P * V = n * R * T",
            "Gas Constant (R) = 0.0821 L·atm/(mol·K)",
            "Solving for Temperature (T): T = (P * V) / (n * R)",
            f"Calculation: ({p} atm * {v} L) / ({n} mol * 0.0821) = {result:.4f} K",
            f"Calculated Temperature = {result:.4f} K"
        ]
        return {"result": result, "solved_for": "Temperature (T)", "steps": steps}

    raise ValueError("Unable to solve gas law equation. Ensure exactly one variable is left blank.")

def calculate_density(mass: float | None = None, volume: float | None = None, density: float | None = None) -> dict:
    """
    Solves the Density equation: D = M / V
    Where:
    - D = Density (e.g., g/mL, g/cm³)
    - M = Mass (e.g., grams)
    - V = Volume (e.g., mL, L)
    
    Provide exactly two variables, leaving the unknown variable as None.
    """
    provided = [x for x in (mass, volume, density) if x is not None]
    if len(provided) != 2:
        raise ValueError("Exactly two variables must be provided to solve the density equation.")
        
    for val in provided:
        if val <= 0:
            raise ValueError("All inputs must be greater than 0.")

    if density is None:
        assert mass is not None and volume is not None
        # D = M / V
        result = mass / volume
        steps = [
            "Density Equation: Density = Mass / Volume",
            f"Calculation: {mass} g / {volume} mL = {result:.4f} g/mL",
            f"Calculated Density = {result:.4f} g/mL (or g/cm³)"
        ]
        return {"result": result, "solved_for": "Density", "steps": steps}
        
    elif mass is None:
        assert density is not None and volume is not None
        # M = D * V
        result = density * volume
        steps = [
            "Density Equation: Density = Mass / Volume",
            "Solving for Mass: Mass = Density * Volume",
            f"Calculation: {density} g/mL * {volume} mL = {result:.4f} g",
            f"Calculated Mass = {result:.4f} g"
        ]
        return {"result": result, "solved_for": "Mass", "steps": steps}
        
    elif volume is None:
        assert mass is not None and density is not None
        # V = M / D
        result = mass / density
        steps = [
            "Density Equation: Density = Mass / Volume",
            "Solving for Volume: Volume = Mass / Density",
            f"Calculation: {mass} g / {density} g/mL = {result:.4f} mL",
            f"Calculated Volume = {result:.4f} mL (or cm³)"
        ]
        return {"result": result, "solved_for": "Volume", "steps": steps}

    raise ValueError("Unable to solve density equation. Ensure exactly one variable is left blank.")

def convert_units(value: float, category: str, from_unit: str, to_unit: str) -> dict:
    """
    Converts units for Temperature, Pressure, and Volume.
    Supported units:
    - Temperature: Celsius (C), Fahrenheit (F), Kelvin (K)
    - Pressure: atm, kPa, bar, mmHg
    - Volume: L, mL, m3
    """
    if category.lower() == "temperature":
        # Convert from_unit to Kelvin first as baseline
        val_k = 0.0
        if from_unit == "C":
            val_k = value + 273.15
        elif from_unit == "F":
            val_k = (value - 32) * 5/9 + 273.15
        elif from_unit == "K":
            val_k = value
        else:
            raise ValueError(f"Unknown temperature unit: {from_unit}")
            
        if val_k < 0:
            raise ValueError("Temperature cannot be below Absolute Zero (0 Kelvin).")

        # Convert Kelvin baseline to target unit
        if to_unit == "C":
            result = val_k - 273.15
        elif to_unit == "F":
            result = (val_k - 273.15) * 9/5 + 32
        elif to_unit == "K":
            result = val_k
        else:
            raise ValueError(f"Unknown temperature unit: {to_unit}")
            
        steps = [
            f"Converting temperature: {value} °{from_unit} to °{to_unit}",
            f"1. Convert input to Kelvin: {val_k:.2f} K",
            f"2. Convert Kelvin to target: {result:.2f} °{to_unit}"
        ]
        return {"result": result, "steps": steps}

    elif category.lower() == "pressure":
        if value < 0:
            raise ValueError("Pressure cannot be negative.")
            
        # Conversion factors relative to 1 atm
        factors_to_atm = {
            "atm": 1.0,
            "kPa": 101.325,
            "bar": 1.01325,
            "mmHg": 760.0
        }
        
        if from_unit not in factors_to_atm or to_unit not in factors_to_atm:
            raise ValueError("Invalid pressure units.")
            
        # Convert to atm first, then to target
        val_atm = value / factors_to_atm[from_unit]
        result = val_atm * factors_to_atm[to_unit]
        
        steps = [
            f"Converting pressure: {value} {from_unit} to {to_unit}",
            f"1. Convert input to atm: {value} / {factors_to_atm[from_unit]} = {val_atm:.5f} atm",
            f"2. Convert atm to target: {val_atm:.5f} * {factors_to_atm[to_unit]} = {result:.4f} {to_unit}"
        ]
        return {"result": result, "steps": steps}

    elif category.lower() == "volume":
        if value < 0:
            raise ValueError("Volume cannot be negative.")
            
        # Conversion factors relative to 1 L
        factors_to_l = {
            "L": 1.0,
            "mL": 1000.0,
            "m3": 0.001
        }
        
        if from_unit not in factors_to_l or to_unit not in factors_to_l:
            raise ValueError("Invalid volume units.")
            
        # Convert to Liters first, then to target
        val_l = value / factors_to_l[from_unit]
        result = val_l * factors_to_l[to_unit]
        
        steps = [
            f"Converting volume: {value} {from_unit} to {to_unit}",
            f"1. Convert input to Liters: {value} / {factors_to_l[from_unit]} = {val_l:.5f} L",
            f"2. Convert Liters to target: {val_l:.5f} * {factors_to_l[to_unit]} = {result:.4f} {to_unit}"
        ]
        return {"result": result, "steps": steps}
        
    else:
        raise ValueError(f"Unknown category: {category}")
