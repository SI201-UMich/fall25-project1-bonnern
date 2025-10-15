# Made by Noah Bonner
# student id: 7318 1748
# email: bonnern@umich.edu
# Collaborators: Worked by myself, used Gen Ai for some assistance, such as helping me with some errors reading in the code, and CSV Path was used to help me. Also helped me with an outline of the project, used it for some debugging too


import csv

from pathlib import Path

HERE = Path(__file__).parent
CSV_PATH = HERE / "penguins-2.csv"


# READ IN FILE
def read_penguins_csv(filename):
    data = []
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            for k, v in row.items():
                if v == "NA":
                    row[k] = None
            if row["bill_length_mm"]:
                row["bill_length_mm"] = float(row["bill_length_mm"])
            if row["bill_depth_mm"]:
                row["bill_depth_mm"] = float(row["bill_depth_mm"])
            if row["flipper_length_mm"]:
                row["flipper_length_mm"] = int(row["flipper_length_mm"])
            if row["body_mass_g"]:
                row["body_mass_g"] = int(row["body_mass_g"])
            if row["year"]:
                row["year"] = int(row["year"])
            data.append(row)
    return data
# FIRST CALCULATION
def calc_avg_flipper_by_species_island(data):
    totals = {}
    counts = {}

    for row in data:
        species = row["species"]
        island = row["island"]
        flipper = row["flipper_length_mm"]

        if species and island and flipper:
            key = (species, island)
            totals[key] = totals.get(key, 0) + flipper
            counts[key] = counts.get(key, 0) + 1
    averages = {}
    for key in totals:
        averages[key] = round(totals[key] / counts[key], 2)
    return averages
#SECOND CALC

def calc_pct_highmass_shallowbill_by_sex_latest_year(data, mass_threshold=4500, depth_threshold=18.0):
    years = [row["year"] for row in data if row["year"]]
    if not years:
        return {}
    latest = max(years)

    counts = {}
    matches = {}

    for row in data:
        if row["year"] != latest:
            continue
        sex = row["sex"]
        mass = row["body_mass_g"]
        depth = row["bill_depth_mm"]
        if not sex or not mass or not depth:
            continue
        
        counts[sex] = counts.get(sex, 0) + 1
        if mass >= mass_threshold and depth < depth_threshold:
            matches[sex] = matches.get(sex, 0) + 1
    results = {}
    for sex in counts:
        num = matches.get(sex, 0)
        den = counts[sex]
        percent = round((num / den) * 100, 2)
        results[sex] = {"year": latest, "numerator": num, "denominator": den, "percent": percent}

    return results



#WRITE results to file

def write_dict_to_csv(data_dict, filename, headers):

    with open(filename, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(headers)
        for key, value in data_dict.items():
            if isinstance(key, tuple):
                w.writerow(list(key) + [value])
            elif isinstance(value, dict):
                w.writerow([key, value["year"], value["numerator"], value["denominator"], value["percent"]])
            else:
                w.writerow([key, value])

def main():
    filename = "penguins-2.csv"
    data = read_penguins_csv(str(CSV_PATH))

    avg_flipper = calc_avg_flipper_by_species_island(data)
    percent_mass = calc_pct_highmass_shallowbill_by_sex_latest_year(data)

    write_dict_to_csv(avg_flipper, "avg_flipper.csv", ["Species", "Island", "Average_Flipper_mm"])
    write_dict_to_csv(percent_mass, "percent_mass.csv", ["Sex", "Year", "Numerator", "Denominator", "Percent"])

if __name__ == "__main__":
    main()

    




# Test Cases 

import unittest

class TestAvgFlipperBySpeciesIsland(unittest.TestCase):
    def test_usual_multiple_groups(self):
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
            {"sex": "female", "body_mass_g": 4600, "bill_depth_mm": 17.5, "year": 2009},  # yes
            {"sex": "female", "body_mass_g": 4300, "bill_depth_mm": 17.5, "year": 2009},  # no
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
            {"sex": None,   "body_mass_g": 5000, "bill_depth_mm": 17.0, "year": 2009},  # shouldnt work no sex
            {"sex": "male", "body_mass_g": None, "bill_depth_mm": 17.0, "year": 2009},  # shouldnt work no mass
        ]
        res = calc_pct_highmass_shallowbill_by_sex_latest_year(data)
        self.assertEqual(res, {})

    def test_edge_threshold_boundaries(self):
        data = [
            {"sex": "male",   "body_mass_g": 4500, "bill_depth_mm": 17.99, "year": 2009},  # yes
            {"sex": "male",   "body_mass_g": 4499, "bill_depth_mm": 17.00, "year": 2009},  # no too light
            {"sex": "male",   "body_mass_g": 5000, "bill_depth_mm": 18.00, "year": 2009},  # depth not < 18
            {"sex": "female", "body_mass_g": 4500, "bill_depth_mm": 17.00, "year": 2009},  # yes
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

    
