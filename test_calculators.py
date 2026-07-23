"""
Unit Tests for Chemistry Calculator Suite
------------------------------------------
Run these tests using: python -m unittest test_calculators.py
This file verifies the mathematical correctness of our modular backend.
"""

import unittest
import math

from modules.solutions import (
    calculate_molarity,
    calculate_molality,
    calculate_normality,
    calculate_dilution
)
from modules.physical import (
    solve_gas_law,
    calculate_density,
    convert_units
)
from modules.stoichiometry import (
    calculate_molar_mass,
    calculate_ph_poh,
    calculate_percent_yield,
    calculate_equivalent_weight
)

class TestSolutions(unittest.TestCase):
    def test_molarity(self):
        # 58.44g of NaCl (molar mass 58.44) in 1000 mL (1 L) should be 1.0 M
        res = calculate_molarity(58.44, 58.44, 1000.0)
        self.assertAlmostEqual(res["result"], 1.0, places=4)
        
        # Test invalid inputs
        with self.assertRaises(ValueError):
            calculate_molarity(10, 0, 1000)
        with self.assertRaises(ValueError):
            calculate_molarity(10, 58.44, -500)

    def test_molality(self):
        # 180.16g glucose (molar mass 180.16) in 1000g solvent should be 1.0 m
        res = calculate_molality(180.16, 180.16, 1000.0)
        self.assertAlmostEqual(res["result"], 1.0, places=4)

    def test_normality(self):
        # 0.5 M solution of H2SO4 (n-factor = 2) should be 1.0 N
        res = calculate_normality(0.5, 2.0)
        self.assertAlmostEqual(res["result"], 1.0, places=4)

    def test_dilution(self):
        # Solve for V2: M1=10, V1=1, M2=1 => V2 should be 10
        res = calculate_dilution(m1=10.0, v1=1.0, m2=1.0, v2=None)
        self.assertEqual(res["solved_for"], "V2")
        self.assertAlmostEqual(res["result"], 10.0, places=4)
        
        # Solve for M1: V1=2, M2=3, V2=4 => M1 should be 6
        res = calculate_dilution(m1=None, v1=2.0, m2=3.0, v2=4.0)
        self.assertEqual(res["solved_for"], "M1")
        self.assertAlmostEqual(res["result"], 6.0, places=4)


class TestPhysicalChemistry(unittest.TestCase):
    def test_ideal_gas_law(self):
        # Solve for n: P=1.0, V=22.414, T=273.15, R=0.0821 => n should be ~1.0
        res = solve_gas_law(p=1.0, v=22.414, n=None, t=273.15)
        self.assertAlmostEqual(res["result"], 1.0, places=2)
        
        # Solve for P: V=10.0, n=1.0, T=300.0
        res = solve_gas_law(p=None, v=10.0, n=1.0, t=300.0)
        expected_p = (1.0 * 0.0821 * 300.0) / 10.0
        self.assertAlmostEqual(res["result"], expected_p, places=4)

    def test_density(self):
        # Solve for Density: M=100.0, V=50.0 => D should be 2.0
        res = calculate_density(mass=100.0, volume=50.0, density=None)
        self.assertAlmostEqual(res["result"], 2.0, places=4)

    def test_unit_conversions(self):
        # Temp: 0 C to K => 273.15 K
        res = convert_units(0.0, "temperature", "C", "K")
        self.assertAlmostEqual(res["result"], 273.15, places=2)
        
        # Temp: 100 C to F => 212.0 F
        res = convert_units(100.0, "temperature", "C", "F")
        self.assertAlmostEqual(res["result"], 212.0, places=2)
        
        # Pressure: 1 atm to kPa => 101.325 kPa
        res = convert_units(1.0, "pressure", "atm", "kPa")
        self.assertAlmostEqual(res["result"], 101.325, places=3)
        
        # Volume: 1 m3 to L => 1000 L
        res = convert_units(1.0, "volume", "m3", "L")
        self.assertAlmostEqual(res["result"], 1000.0, places=2)


class TestStoichiometry(unittest.TestCase):
    def test_molar_mass_parser(self):
        # Simple formula
        res = calculate_molar_mass("H2O")
        # H: 2 * 1.008 + O: 1 * 15.999 = 18.015
        self.assertAlmostEqual(res["result"], 18.015, places=3)
        
        # Grouped formula
        res = calculate_molar_mass("Ca(OH)2")
        # Ca: 40.078 + 2 * (O: 15.999 + H: 1.008) = 74.092
        self.assertAlmostEqual(res["result"], 74.092, places=3)
        
        # Nested groups
        res = calculate_molar_mass("(NH4)2SO4")
        # N: 2*14.007 + H: 8*1.008 + S: 32.06 + O: 4*15.999 = 132.134
        self.assertAlmostEqual(res["result"], 132.134, places=3)

        # Invalid element checks
        with self.assertRaises(ValueError):
            calculate_molar_mass("Xy2")
        # Case sensitivity validation
        with self.assertRaises(ValueError):
            calculate_molar_mass("h2o")

    def test_ph_poh(self):
        # pH = 3.0 => pOH = 11.0, [H+] = 1e-3, [OH-] = 1e-11
        res = calculate_ph_poh(3.0, "pH")
        self.assertAlmostEqual(res["pH"], 3.0, places=4)
        self.assertAlmostEqual(res["pOH"], 11.0, places=4)
        self.assertAlmostEqual(res["H"], 1e-3, places=6)
        self.assertAlmostEqual(res["OH"], 1e-11, places=13)

    def test_percent_yield(self):
        # Actual=40.0, Theoretical=50.0 => 80.0%
        res = calculate_percent_yield(40.0, 50.0)
        self.assertAlmostEqual(res["result"], 80.0, places=2)

    def test_equivalent_weight(self):
        # H2SO4 molar mass ~98.08, basicity=2 => Eq wt = 49.04
        res = calculate_equivalent_weight(98.08, 2.0)
        self.assertAlmostEqual(res["result"], 49.04, places=2)

if __name__ == "__main__":
    unittest.main()
