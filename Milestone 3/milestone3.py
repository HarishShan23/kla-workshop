from itertools import pairwise
import math
from collections import Counter

compare_list = lambda x, y: Counter(x) == Counter(y)

milestone2_source = 'Source.txt'
milestone2_poi = 'POI.txt'
milestone2_output = 'MileStone3_Result.txt'

class polygon:
    def __init__(self, layer, datatype, numVertices, vertexList):
        self.layer = layer
        self.datatype = datatype
        self.numVertices = numVertices
        self.vertexList = vertexList

poly_objList = []
poi_objList = []

# Function to initialize a polygon object from a string
def initPolyObject(poly, poi):
    poly = poly.split('\n')
    
    assert poly[0] == 'boundary'

    layer = poly[1].split(' ')[1]
    datatype = poly[2].split(' ')[1]
    
    string = poly[3].split('  ')[1:]
    numVertices = int(string[0])
    vertexList = []

    for xy in string[1:]:
        vert1, vert2 = xy.split(' ')
        vertexList.append([int(vert1), int(vert2)])

    polygon_obj = polygon(layer, datatype, numVertices, vertexList)

    if poi == False:
        poly_objList.append(polygon_obj)
    else:
        poi_objList.append(polygon_obj)

# Function to return first 'num' polygon objects as a string
def writePolyObjects(poly_objList, matched_indx):
    poly_strs = []

    for i in matched_indx:
        str = ''
        str += 'boundary\n'
        str += f'layer {poly_objList[i].layer}\n'
        str += f'datatype {poly_objList[i].datatype}\n'
        str += f'xy  {poly_objList[i].numVertices}  '

        for vertex in poly_objList[i].vertexList:
            for point in vertex:
                str += f'{point} '
            str += ' '

        str += '\nendel\n'
        poly_strs.append(str)

    return poly_strs

# Function to check if two polygons are equal with distance
def matchVertices(poly_vertexList, poi_vertexList):
    poly_diff_x = []
    poly_diff_y = []
    poi_diff_x = []
    poi_diff_y = []

    poly_diff = []
    poi_diff = []

    count = 0
    for x,y in pairwise(poly_vertexList):
        count += 1
        diff = [(x1 - x2)**2 for (x1, x2) in zip(x, y)]
        poly_diff_x.append(diff[0])
        poly_diff_y.append(diff[1])
        poly_diff.append(diff[0] + diff[1])

    for x,y in pairwise(poi_vertexList):
        diff = [(x1 - x2)**2 for (x1, x2) in zip(x, y)]
        poi_diff_x.append(diff[0])
        poi_diff_y.append(diff[1])
        poi_diff.append(diff[0] + diff[1])

    return compare_list(poly_diff, poi_diff)

# Function to match POI with polygon objects
def matchPolygons(poly_objList, poi_objList):
    matched_indx = []
    for i in range(len(poi_objList)):
        for j in range(len(poly_objList)):
            
            if poi_objList[i].numVertices == poly_objList[j].numVertices:
                poi_vertexList = poi_objList[i].vertexList
                poly_vertexList = poly_objList[j].vertexList

                if matchVertices(poly_vertexList, poi_vertexList):
                    matched_indx.append(j)
    return matched_indx


with open(milestone2_source, 'r') as rf:
    data = rf.read()
    data = data.split('boundary')

    header = data[0]

    polygon_list = ['boundary' + x for x in data[1:-1]]

    last_poly, footer = data[-1].split('endstr')
    last_poly = 'boundary' + last_poly
    polygon_list.append(last_poly)

    footer = 'endstr' + footer

with open(milestone2_poi, 'r') as rf_poi:
    data_poi = rf_poi.read()
    data_poi = data_poi.split('boundary')

    header_poi = data_poi[0]

    poi_list = ['boundary' + x for x in data_poi[1:-1]]

    last_poly, footer_poi = data[-1].split('endstr')
    last_poly = 'boundary' + last_poly
    poi_list.append(last_poly)

    footer_poi = 'endstr' + footer_poi

    
for poly in polygon_list:
    initPolyObject(poly, poi=False)

for poi in poi_list:
    initPolyObject(poly, poi=True)

# Match Polygons of Interest with Source file
matched_indx = matchPolygons(poly_objList, poi_objList)

# Specify number of polygons to print here
polyStrings = writePolyObjects(poly_objList, matched_indx)

with open(milestone2_output, 'w') as rw:
    rw.write(header)

    for polystr in polyStrings:
        for line in polystr:
            rw.write(line)

    rw.write(footer)


