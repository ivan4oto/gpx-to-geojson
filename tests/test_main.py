import unittest
from src.main import GeoJsonTransformer


class GeoJsonTransformerTestCase(unittest.TestCase):
    def setUp(self):
        self.file_path = 'tests/fixtures/gpx_file_short.gpx'
        self.gpx_file = open(self.file_path, 'r')
        self.short_coordinates_list = [23.250621557235718, 42.59468181547034, 23.250718116760254, 42.59461863032628,
                                       23.250889778137207, 42.59451990341043, 23.250980973243713, 42.59442907450971]
        self.short_elevation_list = [1737.71, 1740.42, 1744.88, 1747.91]
        self.short_paired_data = [[23.250621557235718, 42.59468181547034, 1737.71], [23.250718116760254, 42.59461863032628, 1740.42],
                                  [23.250889778137207, 42.59451990341043, 1744.88], [23.250980973243713, 42.59442907450971, 1747.91]]

    def test_object_name_correct(self):
        obj = GeoJsonTransformer(in_memory_file=self.gpx_file)
        self.assertEqual(obj.name, 'gpx_file_short')

    def test_object_name_correct_path(self):
        obj = GeoJsonTransformer(path=self.file_path)
        self.assertEqual(obj.name, 'gpx_file_short')

    def test_coordinate_list_correct(self):
        obj = GeoJsonTransformer(in_memory_file=self.gpx_file)
        result = obj.coordinates_list
        self.assertEqual(result, self.short_coordinates_list)

    def test_coordinate_list_correct_path(self):
        obj = GeoJsonTransformer(path=self.file_path)
        result = obj.coordinates_list
        self.assertEqual(result, self.short_coordinates_list)

    def test_elevation_list_correct(self):
        obj = GeoJsonTransformer(in_memory_file=self.gpx_file)
        result = obj.elevation_list
        self.assertEqual(result, self.short_elevation_list)

    def test_elevation_list_correct_path(self):
        obj = GeoJsonTransformer(path=self.file_path)
        result = obj.elevation_list
        self.assertEqual(result, self.short_elevation_list)

    def test_total_elevation_correct(self):
        obj = GeoJsonTransformer(in_memory_file=self.gpx_file)
        result = obj.total_elevation
        self.assertEqual(result, 10)

    def test_total_distance_correct(self):
        obj = GeoJsonTransformer(in_memory_file=self.gpx_file)
        result = obj.total_distance
        self.assertEqual(result, 0.04)

    def test_starting_point_correct(self):
        obj = GeoJsonTransformer(in_memory_file=self.gpx_file)
        expected = (self.short_coordinates_list[0], self.short_coordinates_list[1])
        result = obj.starting_point
        self.assertEqual(result, expected)
    
    def test_ele_distance_pairs(self):
        obj = GeoJsonTransformer(in_memory_file=self.gpx_file)
        expected = [(1737.71, 0), (1740.42, 0.01), (1744.88, 0.03), (1747.91, 0.04)]
        result = obj.ele_distance_pairs
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
