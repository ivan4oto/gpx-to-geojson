class ExpectedData():
    GEOJSON_DICT = {
                    "type":"FeatureCollection",
                    "features":[
                        {
                            "type":"Feature",
                            "properties":{
                                "name":"gpx_file_short"
                            },
                            "geometry":{
                                "type":"LineString",
                                "coordinates":[
                                [
                                    23.250621557235718,
                                    42.59468181547034,
                                    1737.71
                                ],
                                [
                                    23.250718116760254,
                                    42.59461863032628,
                                    1740.42
                                ],
                                [
                                    23.250889778137207,
                                    42.59451990341043,
                                    1744.88
                                ],
                                [
                                    23.250980973243713,
                                    42.59442907450971,
                                    1747.91
                                ]
                                ]
                            }
                        }
                    ]
                    }
    CSV_DICT = [{'elevation': '1737.71', 'distance': '0'},
                {'elevation': '1740.42', 'distance': '0.01'},
                {'elevation': '1744.88', 'distance': '0.03'},
                {'elevation': '1747.91', 'distance': '0.04'}]