import json
import csv
import unittest
import tempfile
import os
from tests.fixtures.example_data import ExpectedData
from src.gpx_geojson_py import GeoJsonTransformer


class GeoJsonTransformerTestCase(unittest.TestCase):
    def setUp(self):
        self.path_short = 'tests/fixtures/gpx_file_short.gpx'
        self.json_path = 'tests/gpx_file_short.json'
        self.lion_heart_path = 'tests/fixtures/LionHeartUltraCrossTriathlon-Run2017.gpx'
        self.short_gpx_file = open(self.path_short, 'r')
        self.lion_heart_file = open(self.lion_heart_path, 'r')
        self.short_coordinates_list = [23.250621557235718, 42.59468181547034, 23.250718116760254, 42.59461863032628,
                                       23.250889778137207, 42.59451990341043, 23.250980973243713, 42.59442907450971]
        self.short_elevation_list = [1737.71, 1740.42, 1744.88, 1747.91]
        self.short_paired_data = [[23.250621557235718, 42.59468181547034, 1737.71], [23.250718116760254, 42.59461863032628, 1740.42],
                                  [23.250889778137207, 42.59451990341043, 1744.88], [23.250980973243713, 42.59442907450971, 1747.91]]

    def tearDown(self) -> None:
        self.short_gpx_file.close()
        self.lion_heart_file.close()

    def test_object_name_correct(self):
        obj = GeoJsonTransformer(in_memory_file=self.short_gpx_file)
        self.assertEqual(obj.name, 'gpx_file_short')

    def test_object_name_correct_path(self):
        obj = GeoJsonTransformer(path=self.path_short)
        self.assertEqual(obj.name, 'gpx_file_short')

    def test_coordinate_list_correct(self):
        obj = GeoJsonTransformer(in_memory_file=self.short_gpx_file)
        result = obj.coordinates_list
        self.assertEqual(result, self.short_coordinates_list)

    def test_coordinate_list_correct_path(self):
        obj = GeoJsonTransformer(path=self.path_short)
        result = obj.coordinates_list
        self.assertEqual(result, self.short_coordinates_list)

    def test_elevation_list_correct(self):
        obj = GeoJsonTransformer(in_memory_file=self.short_gpx_file)
        result = obj.elevation_list
        self.assertEqual(result, self.short_elevation_list)

    def test_elevation_list_correct_path(self):
        obj = GeoJsonTransformer(path=self.path_short)
        result = obj.elevation_list
        self.assertEqual(result, self.short_elevation_list)

    def test_total_elevation_correct(self):
        obj = GeoJsonTransformer(in_memory_file=self.short_gpx_file)
        result = obj.total_elevation
        self.assertEqual(result, 10)

    # def test_total_elevation_correct__lion_heart(self):
    #     obj = GeoJsonTransformer(in_memory_file=self.lion_heart_file)
    #     result = obj.total_elevation
    #     self.assertEqual(result, 10)

    def test_total_distance_correct__lion_heart(self):
        obj = GeoJsonTransformer(in_memory_file=self.lion_heart_file)
        result = obj.total_distance
        self.assertEqual(result, 20.96)

    def test_starting_point_correct(self):
        obj = GeoJsonTransformer(in_memory_file=self.short_gpx_file)
        expected = (self.short_coordinates_list[0], self.short_coordinates_list[1])
        result = obj.starting_point
        self.assertEqual(result, expected)
    
    def test_ele_distance_pairs(self):
        obj = GeoJsonTransformer(in_memory_file=self.short_gpx_file)
        expected = [(1737.71, 0), (1740.42, 0.01), (1744.88, 0.03), (1747.91, 0.04)]
        result = obj.ele_distance_pairs
        self.assertEqual(result, expected)

    def test_save_geojson(self):
        obj = GeoJsonTransformer(in_memory_file=self.short_gpx_file)
        temp_filepath = tempfile.mkstemp(suffix='.json')
        try:
            obj.save_geojson(temp_filepath[1])
            self.assertTrue(os.path.isfile(temp_filepath[1]))
            test_geojson = open(temp_filepath[1])
            result_dict = json.load(test_geojson)
            self.assertEqual(ExpectedData().GEOJSON_DICT, result_dict)
        finally:
            test_geojson.close()
            os.remove(temp_filepath[1])

    def test_to_csv(self):
        obj = GeoJsonTransformer(in_memory_file=self.short_gpx_file)
        temp_filepath = tempfile.mkstemp(suffix='.csv')
        try:
            obj.to_csv(temp_filepath[1])
            self.assertTrue(os.path.isfile(temp_filepath[1]))
            csv_file = open(temp_filepath[1], 'r')
            csv_reader = csv.reader(temp_filepath[1], delimiter=',')
            csv_reader = csv.DictReader(csv_file)
            result_list = [row for row in csv_reader]
            self.assertEqual(ExpectedData().CSV_DICT, result_list)
        finally:
            csv_file.close()
            os.remove(temp_filepath[1])


if __name__ == '__main__':
    unittest.main()
