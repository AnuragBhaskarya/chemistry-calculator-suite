# 🧪 Chemistry Calculator Suite

A clean, modular Streamlit web application for students, educators, and laboratory chemists. Provides interactive, step-by-step solutions for solution concentration, physical gas laws, and stoichiometry computations.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🌟 Key Features

- **Concentration Calculators**: Molarity, Molality, Normality, and Dilution ($M_1 V_1 = M_2 V_2$) solvers.
- **Physical Chemistry & Gas Laws**: Ideal Gas Law ($P \cdot V = n \cdot R \cdot T$) multi-variable solver, Density calculator, and Unit Converter.
- **Stoichiometry & Analytical Tools**:
  - Stack-based chemical formula parser handling nested formulas like `(NH4)2SO4` and `Ca(OH)2`.
  - Molar Mass calculator using standard atomic weights.
  - pH / pOH balance solver ($\text{pH} + \text{pOH} = 14$, $[\text{H}^+], [\text{OH}^-]$).
  - Reaction percentage yield and equivalent weight solvers.
- **Educational Explanations**: Displays clear, step-by-step intermediate calculation steps for every calculation.

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/AnuragBhaskarya/chemistry-calculator-suite.git
cd chemistry-calculator-suite
```

### 2. Set Up Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```

---

## 📁 Repository Structure

```
.
├── app.py                     # Streamlit web application frontend
├── calculators.py             # All backend chemistry math & logic
└── requirements.txt           # Application dependencies
```


---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
