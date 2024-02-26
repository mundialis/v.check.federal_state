#!/usr/bin/env python3
#
############################################################################
#
# MODULE:      v.check.federal_state test
# AUTHOR(S):   Lina Krisztian

# PURPOSE:     Tests v.check.federal_state
# COPYRIGHT:   (C) 2022 by mundialis GmbH & Co. KG and the GRASS Development
#              Team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
#############################################################################

import os
from itertools import product

from grass.gunittest.case import TestCase
from grass.gunittest.main import test
from grass.gunittest.gmodules import SimpleModule
import grass.script as grass


class TestVCheckFederalState(TestCase):
    polygon_files = [
        file for file in os.listdir("data") if file.endswith(".geojson")
    ]
    pid = os.getpid()
    # map names for importing geojson-data including filename and pid
    polygon_grass = [
        f"{x.split('.')[0]}_{pid_}"
        for x, pid_ in product(polygon_files, [pid])
    ]
    # names of polygons for different cases
    polygon_notDE = f"polygon_notDE_{pid}"
    # name for saving case
    output_name = f"federal_states_{pid}"

    @classmethod
    def setUpClass(self):
        """Ensures expected computational region and generated data"""
        # import polygons for testing
        [
            self.runModule("v.import", input=f"data/{x}", output=y)
            for x, y in zip(self.polygon_files, self.polygon_grass)
        ]

    @classmethod
    def tearDownClass(self):
        """Remove the temporary region and generated data"""
        [
            self.runModule("g.remove", type="vector", name=x, flags="f")
            for x in self.polygon_grass
        ]

    def tearDown(self):
        """Remove the outputs created
        This is executed after each test run.
        """
        self.runModule(
            "g.remove", type="vector", name=self.output_name, flags="f"
        )

    def test_create_output_map(self):
        """Tests creation of output (if desired)"""
        v_check = SimpleModule(
            "v.check.federal_state",
            aoi=self.polygon_grass[0],
            output=self.output_name,
        )
        self.assertModule(v_check)
        self.assertVectorExists(self.output_name)

    def test_poly_match_correct_fs(self):
        """Tests if federal state of polygon is correctly found.
        For polygon in single federal state-case
        """
        fs_list = [
            ("BB", "Brandenburg"),
            ("BE", "Berlin"),
            ("BW", "Baden-Württemberg"),
            ("BY", "Bayern"),
            ("HB", "Bremen"),
            ("HE", "Hessen"),
            ("HH", "Hamburg"),
            ("MV", "Mecklenburg-Vorpommern"),
            ("NI", "Niedersachsen"),
            ("NW", "Nordrhein-Westfalen"),
            ("RP", "Rheinland-Pfalz"),
            ("SH", "Schleswig-Holstein"),
            ("SL", "Saarland"),
            ("SN", "Sachsen"),
            ("ST", "Sachsen-Anhalt"),
            ("TH", "Thüringen"),
        ]
        for fs_abb, fs_name in fs_list:
            print(f"Running test for {fs_abb}...")
            federal_state_out = grass.parse_command(
                "v.check.federal_state",
                aoi=f"polygon_{fs_abb}_{self.pid}",
                flags="g",
            )
            self.assertEqual(
                federal_state_out["FEDERAL_STATE"],
                fs_name,
                f"FEDERAL_STATE is not {fs_name}",
            )
            self.assertEqual(
                federal_state_out["FS"],
                fs_abb,
                f"FEDERAL_STATE is not {fs_abb}",
            )
            print(f"Running test for {fs_abb} DONE.")

    def test_poly_not_in_DE(self):
        """Tests the case when polygon is not in Germany.
        Should return message, that polygon is not in Germany.
        """
        message = list(
            grass.parse_command(
                "v.check.federal_state", aoi=self.polygon_notDE
            ).keys()
        )[0]
        self.assertEqual(
            message,
            "Not in Germany",
            "Analyzed polygon should be detected as: Not in Germany",
        )

    def test_multiple_fs(self):
        """Tests the case when polygon lies in multiple federal states.
        Should return the multiple federal states.
        """
        polygon_multi = f"polygon_HB_NI_{self.pid}"
        federal_state_out = grass.parse_command(
            "v.check.federal_state", aoi=polygon_multi, flags="g"
        )
        self.assertEqual(
            federal_state_out["FEDERAL_STATE"],
            "Niedersachsen,Bremen",
            "Detected federal states should be Niedersachsen and Bremen",
        )
        self.assertEqual(
            federal_state_out["FS"],
            "NI,HB",
            "Detected federal states should be NI and HB",
        )

    def test_multiple_notDe(self):
        """Tests the case when polygon lies partly in Germany"""
        polygon_multi_land = f"polygon_nrw_notDe_multi_{self.pid}"
        federal_state_out = grass.parse_command(
            "v.check.federal_state", aoi=polygon_multi_land, flags="g"
        )
        self.assertEqual(
            federal_state_out["FEDERAL_STATE"],
            "Nordrhein-Westfalen",
            "Detected federal states should be Nordrhein-Westfalen",
        )
        self.assertEqual(
            federal_state_out["FS"],
            "NW",
            "Detected federal states should be NW",
        )

    def test_wrong_fs_input(self):
        """Tests the case when wrong input for the 'federal_state'-input is
        given
        Should fail and return error message
        """
        # take one of the polygon-test-data as wrong vector input
        poly = self.polygon_grass[0]
        wrong_input = poly
        v_check = SimpleModule(
            "v.check.federal_state", aoi=poly, federal_states=wrong_input
        )
        self.assertModuleFail(v_check)

    def test_correct_fs_input(self):
        """Tests the case when correct input for the 'federal_state'-input is
        given
        Should run succesfully
        """
        # run module a first time, to generate correct federal_state input
        poly = self.polygon_grass[0]
        grass.run_command(
            "v.check.federal_state", aoi=poly, output=self.output_name
        )
        # check case when (correct) federal-state is given as input
        v_check = SimpleModule(
            "v.check.federal_state",
            aoi=poly,
            federal_states=self.output_name,
        )
        self.assertModule(v_check)

    def test_saving_file(self):
        filepath_ = grass.tempdir()
        filepath_cs1 = os.path.join(filepath_, f"cs1{self.pid}")
        filepath_cs2 = os.path.join(filepath_, f"cs1{self.pid}")
        filepath_cs4 = os.path.join(filepath_, "testfolder", f"cs1{self.pid}")
        # polygon not in Germany: run succesfull + no file created
        # (even though filepath given)
        v_check_cs1 = SimpleModule(
            "v.check.federal_state",
            aoi=self.polygon_notDE,
            federal_state_file=filepath_cs1,
        )
        self.assertModule(
            v_check_cs1,
            "v.check.federal_state fails for test case:"
            " federal_state_file-input given + polygon not in Germany",
        )
        self.assertFalse(
            os.path.isfile(filepath_cs1),
            "File was created even though" "polygon is not located in Germany",
        )
        # polygon in federal state found: run sucessful and create file
        v_check_cs2 = SimpleModule(
            "v.check.federal_state",
            aoi=self.polygon_grass[0],
            federal_state_file=filepath_cs2,
        )
        self.assertModule(
            v_check_cs2,
            "v.check.federal_state fails for test case:"
            " federal_state_file-input given and polygon in Germany",
        )
        self.assertFileExists(filepath_cs2, "No output file was created")
        # no filepath given: run successful
        v_check_cs3 = SimpleModule(
            "v.check.federal_state",
            aoi=self.polygon_notDE,
        )
        self.assertModule(
            v_check_cs3,
            "v.check.federal_state fails for test case:"
            " no federal_state_file-input given",
        )
        # no valid filepath: run succesful + no file created
        v_check_cs4 = SimpleModule(
            "v.check.federal_state",
            aoi=self.polygon_notDE,
            federal_state_file=filepath_cs4,
        )
        self.assertModule(
            v_check_cs4,
            "v.check.federal_state fails for test case:"
            " no valid federal_state_file-input given",
        )
        self.assertFalse(
            os.path.isfile(filepath_cs4),
            "File was created even though"
            "a non valid federal_state_file was given",
        )


if __name__ == "__main__":
    test()
