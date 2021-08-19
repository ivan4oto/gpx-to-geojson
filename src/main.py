import os

from lxml import etree
from utils import haversine
import json


class GeoJsonTransformer():
    def __init__(self, path=None, in_memory_file=None):
        self.path = path
        self.file = in_memory_file
        self.parser = etree.XMLParser(remove_blank_text=True)
        self.json_data = None
        self._name = None
        self._coordinates_list = None
        self._elevations_list = None
        self._total_distance = None
        self._total_elevation = None
        self._point_ele_pairs = None
        self._ele_distance_pairs = None
    
    @property
    def name(self):
        if self._name:
            return self._name
        if self.path:
            self._name = os.path.basename(self.path).split('.')[-2]
            return self._name
        elif self.file:
            self._name = os.path.basename(self.file.name).split('.')[-2]
            return self._name

    @property
    def root(self):
        return self.tree.getroot()
    
    @property
    def tree(self):
        if self.path:            
            with open(self.path, 'r') as f:
                tree = etree.parse(f, self.parser)
                tree = self.strip_ns_prefix(tree)
            return tree
        elif self.file:
            tree = etree.parse(self.file, self.parser)
            tree = self.strip_ns_prefix(tree)
            return tree

    def strip_ns_prefix(self, tree):
        #xpath query for selecting all element nodes in namespace
        query = "descendant-or-self::*[namespace-uri()!='']"
        #for each element returned by the above xpath query...
        for element in tree.xpath(query):
            #replace element name with its local name
            element.tag = etree.QName(element).localname
        return tree

    @property
    def coordinates_list(self):
        if self._coordinates_list:
            return self._coordinates_list

        coordinates_list = []
        for element in self.root.iter('trkpt'):
            lon = float(element.attrib.get('lon'))
            lat = float(element.attrib.get('lat'))
            coordinates_list.extend([lon, lat])
        self._coordinates_list = coordinates_list
        return self._coordinates_list

    @property
    def elevation_list(self):
        if self._elevations_list:
            return self._elevations_list

        elevations_list = []
        for element in self.root.iter('ele'):
            ele = int(round(float(element.text)))
            elevations_list.append(ele)
        self._elevations_list = elevations_list
        return self._elevations_list

    @property
    def point_ele_pairs(self):
        if self._point_ele_pairs:
            return self._point_ele_pairs

        elevations_list = self.elevation_list
        coordinates_list = self.coordinates_list
        self._point_ele_pairs = [list(z) for z in zip(coordinates_list[::2], coordinates_list[1::2], elevations_list)]
        return self._point_ele_pairs

    @property
    def ele_distance_pairs(self):
        if self._ele_distance_pairs:
            return self._ele_distance_pairs

        cl = self.coordinates_list
        lines = list(zip(cl[::2], cl[1::2], cl[2::2], cl[3::2]))
        distance_steps = [0]
        for line in lines:
            distance_steps.append(distance_steps[-1] + round(haversine(line[0], line[1], line[2], line[3]), 2))            
        return list(zip(self.elevation_list, distance_steps))


    def make_geojson(self):
        with open('src/configs.json') as f:
            schema = json.load(f)
            schema["features"][0]["properties"]["name"] = self.name
            schema["features"][0]["geometry"]["coordinates"].extend(self.paired_data)
            self.json_data = schema
        return schema
    
    @property
    def total_elevation(self):
        if self._total_elevation:
            return self._total_elevation

        el = self.elevation_list
        total_elevation = 0
        elevation_pairs = list(zip(el[::2], el[1::2]))
        for e in elevation_pairs:
            if e[1] > e[0]:
                total_elevation += e[1]-e[0]
        self._total_elevation = total_elevation
        return self._total_elevation


    @property
    def total_distance(self):
        if self._total_distance:
            return self._total_distance

        cl = self.coordinates_list
        total_distance = 0
        lines = list(zip(cl[::2], cl[1::2], cl[2::2], cl[3::2]))
        for line in lines:
            total_distance += haversine(line[0], line[1], line[2], line[3])
        self._total_distance = round(total_distance, 2)
        return self._total_distance

    def save_geojson(self, filepath=None):
        if not filepath:
            filepath = self.path
            
        filepath = filepath.split('.')
        filepath[-1] = 'json'
        filepath = '.'.join(filepath)
        with open(filepath, 'w') as outfile:
            filepath = filepath.split('.')
            filepath[-1] = 'json'
            filepath = '.'.join(filepath)
            json.dump(self.make_geojson(), outfile)
