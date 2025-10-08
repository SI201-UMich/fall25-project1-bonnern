# Made by Noah Bonner

# Test Cases first

import unittest

class TestAvgFlipperBySpeciesIsland(unittest.TestCase):
    def est_usual_multiple_groups(self):
        data = [
            {"species": "Adelie", "island": "Biscoe",   "flipper_length_mm": 180},
            {"species": "Adelie", "island": "Biscoe",   "flipper_length_mm": 200},
            {"species": "Gentoo", "island": "Dream",    "flipper_length_mm": 210},
        ]

        result = calc_avg_flipper_by_species_island(data)
        self.assertAlmostEqual(result[("Adelie", "Biscoe")], 190.0)
        self.assertAlmostEqual(result[("Gentoo", "Dream")], 210.0)

    def test_usual_single_group(self):
        data = [
            {"species": "Adelie", "island": "Torgersen", "flipper_length_mm": 190},
            {"species": "Adelie", "island": "Torgersen", "flipper_length_mm": 195},
        ]
        result = calc_avg_flipper_by_species_island(data)
        self.assertEqual(len(result), 1)
        self.assertAlmostEqual(result[("Adelie", "Torgersen")], 192.5)

    def test_edge_empty_input(self):
        result = calc_avg_flipper_by_species_island([])
        self.assertEqual(result, {})

    def test_edge_missing_values_ignored(self):
        data = [
            {"species": "Adelie", "island": "Biscoe", "flipper_length_mm": 180},
            {"species": None,     "island": "Biscoe", "flipper_length_mm": 999},   # ignore
            {"species": "Adelie", "island": None,     "flipper_length_mm": 999},   # ignore
            {"species": "Adelie", "island": "Biscoe", "flipper_length_mm": None},  # ignore
        ]
        result = calc_avg_flipper_by_species_island(data)
        self.assertEqual(len(result), 1)
        self.assertAlmostEqual(result[("Adelie", "Biscoe")], 180.0)

class TestPctHighMassShallowBillLatestYear(unittest.TestCase):
    def test_usual_two_sexes_latest_year(self):
        data = [
            {"sex": "male",   "body_mass_g": 4600, "bill_depth_mm": 17.5, "year": 2008},  
            # latest year = 2009
            {"sex": "male",   "body_mass_g": 4700, "bill_depth_mm": 17.0, "year": 2009},  
            {"sex": "male",   "body_mass_g": 4400, "bill_depth_mm": 17.0, "year": 2009},  
            {"sex": "female", "body_mass_g": 4550, "bill_depth_mm": 18.2, "year": 2009},  
            {"sex": "female", "body_mass_g": 5000, "bill_depth_mm": 17.9, "year": 2009},  
        ]
        res = calc_pct_highmass_shallowbill_by_sex_latest_year(data, 4500, 18.0)
        self.assertEqual(res["male"]["numerator"], 1)
        self.assertEqual(res["male"]["denominator"], 2)
        self.assertAlmostEqual(res["male"]["percent"], 50.0, places=2)
        self.assertEqual(res["male"]["year"], 2009)

        self.assertEqual(res["female"]["numerator"], 1)
        self.assertEqual(res["female"]["denominator"], 2)
        self.assertAlmostEqual(res["female"]["percent"], 50.0, places=2)
        self.assertEqual(res["female"]["year"], 2009)

    def test_usual_only_one_sex_in_latest_year(self):
        data = [
            {"sex": "female", "body_mass_g": 4600, "bill_depth_mm": 17.5, "year": 2009},  # qualifies
            {"sex": "female", "body_mass_g": 4300, "bill_depth_mm": 17.5, "year": 2009},  # not qualify
            {"sex": "male",   "body_mass_g": 6000, "bill_depth_mm": 17.0, "year": 2008},  # older year
        ]
        res = calc_pct_highmass_shallowbill_by_sex_latest_year(data)
        self.assertIn("female", res)
        self.assertNotIn("male", res)
        self.assertEqual(res["female"]["numerator"], 1)
        self.assertEqual(res["female"]["denominator"], 2)
        self.assertAlmostEqual(res["female"]["percent"], 50.0, places=2)
        self.assertEqual(res["female"]["year"], 2009)

    def test_edge_latest_year_rows_invalid(self):
        data = [
            {"sex": "male", "body_mass_g": 4800, "bill_depth_mm": 17.5, "year": 2008},
            {"sex": None,   "body_mass_g": 5000, "bill_depth_mm": 17.0, "year": 2009},  # invalid (no sex)
            {"sex": "male", "body_mass_g": None, "bill_depth_mm": 17.0, "year": 2009},  # invalid (no mass)
        ]
        res = calc_pct_highmass_shallowbill_by_sex_latest_year(data)
        self.assertEqual(res, {})

    def test_edge_threshold_boundaries(self):
        data = [
            {"sex": "male",   "body_mass_g": 4500, "bill_depth_mm": 17.99, "year": 2009},  # qualifies
            {"sex": "male",   "body_mass_g": 4499, "bill_depth_mm": 17.00, "year": 2009},  # too light
            {"sex": "male",   "body_mass_g": 5000, "bill_depth_mm": 18.00, "year": 2009},  # depth not < 18
            {"sex": "female", "body_mass_g": 4500, "bill_depth_mm": 17.00, "year": 2009},  # qualifies
        ]
        res = calc_pct_highmass_shallowbill_by_sex_latest_year(data, 4500, 18.0)
        self.assertEqual(res["male"]["numerator"], 1)
        self.assertEqual(res["male"]["denominator"], 3)
        self.assertAlmostEqual(res["male"]["percent"], (1/3)*100, places=2)
        self.assertEqual(res["female"]["numerator"], 1)
        self.assertEqual(res["female"]["denominator"], 1)
        self.assertAlmostEqual(res["female"]["percent"], 100.0, places=2)
        self.assertEqual(res["female"]["year"], 2009)

if __name__ == "__main__":
    unittest.main()

    
