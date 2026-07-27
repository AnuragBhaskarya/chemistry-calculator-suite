"""
Chemistry Calculator Suite
---------------------------
A clean, minimal, single-page Streamlit application.
No sidebar is used; page routing is handled via main-page button clicks.
"""

import streamlit as st

# Import calculator backend logic directly from calculators.py
from calculators import (
    calculate_molarity,
    calculate_molality,
    calculate_normality,
    calculate_dilution,
    solve_gas_law,
    calculate_density,
    convert_units,
    calculate_ph_poh,
    calculate_percent_yield,
    calculate_equivalent_weight
)


# Configure page to standard layout
st.set_page_config(
    page_title="Chemistry Calculator Suite",
    page_icon="🧪",
    layout="centered"
)

# Initialize navigation state if it doesn't exist
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Helper to print steps cleanly
def display_steps(steps_list):
    st.write("**Calculation Steps:**")
    for step in steps_list:
        st.info(step)

# Helper for "Back to Home" button
def back_button():
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()
    st.write("---")

# -------------------------------------------------------------
# Routing Logic
# -------------------------------------------------------------

# --- Page: Home ---
if st.session_state.page == "Home":
    st.title("🧪 Chemistry Calculator Suite")
    st.write("Select a calculator below to perform calculations with step-by-step explanations:")
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Concentration")
        if st.button("Molarity Calculator", use_container_width=True):
            st.session_state.page = "Molarity"
            st.rerun()
        if st.button("Molality Calculator", use_container_width=True):
            st.session_state.page = "Molality"
            st.rerun()
        if st.button("Normality Calculator", use_container_width=True):
            st.session_state.page = "Normality"
            st.rerun()
        if st.button("Dilution Solver", use_container_width=True):
            st.session_state.page = "Dilution"
            st.rerun()
            
    with col2:
        st.subheader("Physical & Gas")
        if st.button("Ideal Gas Law", use_container_width=True):
            st.session_state.page = "Ideal Gas"
            st.rerun()
        if st.button("Density Solver", use_container_width=True):
            st.session_state.page = "Density"
            st.rerun()
        if st.button("Unit Converter", use_container_width=True):
            st.session_state.page = "Converter"
            st.rerun()
            
    with col3:
        st.subheader("Stoichiometry")
        if st.button("pH & pOH Solver", use_container_width=True):
            st.session_state.page = "pH pOH"
            st.rerun()
        if st.button("Percentage Yield", use_container_width=True):
            st.session_state.page = "Yield"
            st.rerun()
        if st.button("Equivalent Weight", use_container_width=True):
            st.session_state.page = "Equivalent Weight"
            st.rerun()
            
    # Formulas table removed

# --- Page: Molarity ---
elif st.session_state.page == "Molarity":
    back_button()
    st.title("Molarity (M) Calculator")
    st.write("Calculates concentration in moles per liter.")
    st.latex(r"M = \frac{\text{Mass (g)}}{\text{Molar Mass (g/mol)} \times \text{Volume (L)}}")
    
    mass = st.number_input("Mass of Solute (grams)", min_value=0.0, value=5.84, step=0.1)
    molar_mass = st.number_input("Molar Mass of Solute (g/mol)", min_value=0.01, value=58.44, step=0.1)
    volume = st.number_input("Volume of Solution (mL)", min_value=0.01, value=1000.0, step=10.0)
    
    if st.button("Calculate", type="primary"):
        try:
            res = calculate_molarity(mass, molar_mass, volume)
            st.success(f"Molarity = {res['result']:.4f} M (mol/L)")
            display_steps(res['steps'])
        except Exception as e:
            st.error(e)

# --- Page: Molality ---
elif st.session_state.page == "Molality":
    back_button()
    st.title("Molality (m) Calculator")
    st.write("Calculates concentration in moles per kilogram of solvent.")
    st.latex(r"m = \frac{\text{Mass of Solute (g)}}{\text{Molar Mass (g/mol)} \times \text{Mass of Solvent (kg)}}")
    
    mass = st.number_input("Mass of Solute (grams)", min_value=0.0, value=10.0, step=0.1)
    molar_mass = st.number_input("Molar Mass of Solute (g/mol)", min_value=0.01, value=180.16, step=0.1)
    solvent = st.number_input("Mass of Solvent (grams)", min_value=0.01, value=500.0, step=10.0)
    
    if st.button("Calculate", type="primary"):
        try:
            res = calculate_molality(mass, molar_mass, solvent)
            st.success(f"Molality = {res['result']:.4f} m (mol/kg)")
            display_steps(res['steps'])
        except Exception as e:
            st.error(e)

# --- Page: Normality ---
elif st.session_state.page == "Normality":
    back_button()
    st.title("Normality (N) Calculator")
    st.write("Calculates equivalent concentration.")
    st.latex(r"N = \text{Molarity (M)} \times \text{n-factor}")
    
    molarity = st.number_input("Molarity of Solution (M)", min_value=0.0, value=0.5, step=0.1)
    n_factor = st.number_input("n-factor (valency, basicity or acidity)", min_value=0.1, value=2.0, step=1.0)
    
    if st.button("Calculate", type="primary"):
        try:
            res = calculate_normality(molarity, n_factor)
            st.success(f"Normality = {res['result']:.4f} N")
            display_steps(res['steps'])
        except Exception as e:
            st.error(e)

# --- Page: Dilution ---
elif st.session_state.page == "Dilution":
    back_button()
    st.title("Dilution Solver")
    st.latex(r"M_1 \cdot V_1 = M_2 \cdot V_2")
    
    solve_for = st.selectbox("Solve For:", ["M1", "V1", "M2", "V2"], index=2)
    m1 = st.number_input("M1 - Initial Concentration (M)", min_value=0.0, value=12.0, disabled=(solve_for == "M1"))
    v1 = st.number_input("V1 - Initial Volume (mL/L)", min_value=0.0, value=10.0, disabled=(solve_for == "V1"))
    m2 = st.number_input("M2 - Final Concentration (M)", min_value=0.0, value=1.0, disabled=(solve_for == "M2"))
    v2 = st.number_input("V2 - Final Volume (mL/L)", min_value=0.0, value=120.0, disabled=(solve_for == "V2"))
    
    if st.button("Solve Dilution", type="primary"):
        try:
            m1_val = None if solve_for == "M1" else m1
            v1_val = None if solve_for == "V1" else v1
            m2_val = None if solve_for == "M2" else m2
            v2_val = None if solve_for == "V2" else v2
            
            res = calculate_dilution(m1_val, v1_val, m2_val, v2_val)
            st.success(f"Calculated {res['solved_for']} = {res['result']:.4f}")
            display_steps(res['steps'])
        except Exception as e:
            st.error(e)

# --- Page: Ideal Gas ---
elif st.session_state.page == "Ideal Gas":
    back_button()
    st.title("Ideal Gas Law Solver")
    st.latex(r"P \cdot V = n \cdot R \cdot T")
    st.markdown(r"*(where $R = 0.0821\text{ L}\cdot\text{atm}/(\text{mol}\cdot\text{K})$)*")
    
    solve_for = st.selectbox("Solve For:", ["Pressure (P)", "Volume (V)", "Moles (n)", "Temperature (T)"])
    p = st.number_input("Pressure (atm)", min_value=0.0, value=1.0, disabled=(solve_for == "Pressure (P)"))
    v = st.number_input("Volume (L)", min_value=0.0, value=22.4, disabled=(solve_for == "Volume (V)"))
    n = st.number_input("Moles (n)", min_value=0.0, value=1.0, disabled=(solve_for == "Moles (n)"))
    t = st.number_input("Temperature (Kelvin)", min_value=0.01, value=273.15, disabled=(solve_for == "Temperature (T)"))
    
    if st.button("Solve Gas Law", type="primary"):
        try:
            p_arg = None if solve_for == "Pressure (P)" else p
            v_arg = None if solve_for == "Volume (V)" else v
            n_arg = None if solve_for == "Moles (n)" else n
            t_arg = None if solve_for == "Temperature (T)" else t
            
            res = solve_gas_law(p_arg, v_arg, n_arg, t_arg)
            st.success(f"Calculated {res['solved_for']} = {res['result']:.4f}")
            display_steps(res['steps'])
        except Exception as e:
            st.error(e)

# --- Page: Density ---
elif st.session_state.page == "Density":
    back_button()
    st.title("Density Solver")
    st.latex(r"\text{Density} = \frac{\text{Mass}}{\text{Volume}}")
    
    solve_for = st.selectbox("Solve For:", ["Density", "Mass", "Volume"])
    d = st.number_input("Density (g/mL)", min_value=0.0, value=1.0, disabled=(solve_for == "Density"))
    m = st.number_input("Mass (grams)", min_value=0.0, value=100.0, disabled=(solve_for == "Mass"))
    v = st.number_input("Volume (mL)", min_value=0.0, value=100.0, disabled=(solve_for == "Volume"))
    
    if st.button("Solve Density", type="primary"):
        try:
            d_arg = None if solve_for == "Density" else d
            m_arg = None if solve_for == "Mass" else m
            v_arg = None if solve_for == "Volume" else v
            
            res = calculate_density(m_arg, v_arg, d_arg)
            st.success(f"Calculated {res['solved_for']} = {res['result']:.4f}")
            display_steps(res['steps'])
        except Exception as e:
            st.error(e)

# --- Page: Converter ---
elif st.session_state.page == "Converter":
    back_button()
    st.title("Scientific Unit Converter")
    st.markdown("**Conversion Constants:** $0\\text{ }^\\circ\\text{C} = 273.15\\text{ K}$, $1\\text{ atm} = 101.325\\text{ kPa} = 760\\text{ mmHg}$")
    
    unit_type = st.selectbox("Select Conversion Category:", ["Temperature", "Pressure", "Volume"])
    value = st.number_input("Value to Convert", value=1.0)
    
    if unit_type == "Temperature":
        from_unit = st.selectbox("From Unit:", ["C", "F", "K"])
        to_unit = st.selectbox("To Unit:", ["C", "F", "K"], index=2)
    elif unit_type == "Pressure":
        from_unit = st.selectbox("From Unit:", ["atm", "kPa", "bar", "mmHg"])
        to_unit = st.selectbox("To Unit:", ["atm", "kPa", "bar", "mmHg"], index=1)
    else:
        from_unit = st.selectbox("From Unit:", ["L", "mL", "m3"])
        to_unit = st.selectbox("To Unit:", ["L", "mL", "m3"], index=1)
        
    if st.button("Convert", type="primary"):
        try:
            res = convert_units(value, unit_type, from_unit, to_unit)
            st.success(f"Result = {res['result']:.4f} {to_unit}")
            display_steps(res['steps'])
        except Exception as e:
            st.error(e)

# --- Page: pH pOH ---
elif st.session_state.page == "pH pOH":
    back_button()
    st.title("pH & pOH Balance Solver")
    st.latex(r"\text{pH} = -\log_{10}[H^+] \quad \text{pOH} = -\log_{10}[OH^-] \quad \text{pH} + \text{pOH} = 14")
    
    input_type = st.selectbox("Input Category:", ["pH", "pOH", "[H+] Concentration", "[OH-] Concentration"])
    type_code = {"pH": "pH", "pOH": "pOH", "[H+] Concentration": "H", "[OH-] Concentration": "OH"}[input_type]
    value = st.number_input("Input Value:", min_value=0.0 if "pH" in input_type else 1e-15, max_value=14.0 if "pH" in input_type else 10.0, value=7.0 if "pH" in input_type else 1e-7, format="%.2e" if "Concentration" in input_type else "%.2f")
    
    if st.button("Solve Balance", type="primary"):
        try:
            res = calculate_ph_poh(value, type_code)
            st.success("Calculated Parameters:")
            st.write(f"- **pH**: {res['pH']:.4f}")
            st.write(f"- **pOH**: {res['pOH']:.4f}")
            st.write(f"- **[H+]**: {res['H']:.4e} M")
            st.write(f"- **[OH-]**: {res['OH']:.4e} M")
            display_steps(res['steps'])
        except Exception as e:
            st.error(e)

# --- Page: Yield ---
elif st.session_state.page == "Yield":
    back_button()
    st.title("Percentage Yield Calculator")
    st.latex(r"\text{Percentage Yield} = \frac{\text{Actual Yield}}{\text{Theoretical Yield}} \times 100\%")
    
    theory = st.number_input("Theoretical Yield (grams)", min_value=0.01, value=50.0)
    actual = st.number_input("Actual Yield (grams)", min_value=0.0, value=42.5)
    
    if st.button("Calculate Yield", type="primary"):
        try:
            res = calculate_percent_yield(actual, theory)
            st.success(f"Percentage Yield = {res['result']:.2f}%")
            if res['exceeds_theoretical']:
                st.warning("Warning: Actual yield exceeds theoretical yield. Confirm product dryness/purity.")
            display_steps(res['steps'])
        except Exception as e:
            st.error(e)

# --- Page: Equivalent Weight ---
elif st.session_state.page == "Equivalent Weight":
    back_button()
    st.title("Equivalent Weight Calculator")
    st.latex(r"\text{Equivalent Weight} = \frac{\text{Molar Mass}}{\text{n-factor}}")
    
    molar_mass_val = st.number_input("Input Molar Mass (g/mol):", min_value=0.01, value=98.079, step=0.1)
        
    n_factor = st.number_input("n-factor (valency, acidity, basicity):", min_value=0.1, value=2.0)
    
    if st.button("Calculate Equivalent Weight", type="primary"):
        try:
            res = calculate_equivalent_weight(molar_mass_val, n_factor)
            st.success(f"Equivalent Weight = {res['result']:.4f} g/eq")
            display_steps(res['steps'])
        except Exception as e:
            st.error(e)
