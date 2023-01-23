import itertools
milestone1_source = 'Format_Source.txt'
milestone1_output = 'Format_Output.txt'

class polygon:
    def __init__(self, layer, datatype, numVertices, vertexList):
        self.layer = layer
        self.datatype = datatype
        self.numVertices = numVertices
        self.vertexList = vertexList

poly_objList = []

# Function to initialize a polygon object from a string
def initPolyObject(poly):
    poly = poly.split('\n')
    
    assert poly[0] == 'boundary'

    layer = poly[1].split(' ')[1]
    datatype = poly[2].split(' ')[1]
    
    string = poly[3].split('  ')[1:]
    numVertices = string[0]
    vertexList = []

    for xy in string[1:]:
        vertexList.append(xy)

    polygon_obj = polygon(layer, datatype, numVertices, vertexList)
    poly_objList.append(polygon_obj)

# Function to return first 'num' polygon objects as a string
def writePolyObjects(poly_objList, num=None):
    poly_strs = []

    if num == None:
        num = len(poly_objList)

    for i in range(num):
        str = ''
        str += 'boundary\n'
        str += f'layer {poly_objList[i].layer}\n'
        str += f'datatype {poly_objList[i].datatype}\n'
        str += f'xy  {poly_objList[i].numVertices}'

        for vertex in poly_objList[i].vertexList:
            str += f'  {vertex}'

        str += '\nendel\n'
        poly_strs.append(str)

    return poly_strs
        

with open(milestone1_source, 'r') as rf:
    data = rf.read()
    data = data.split('boundary')

    header = data[0]

    polygon_list = ['boundary' + x for x in data[1:-1]]

    last_poly, footer = data[-1].split('endstr')
    last_poly = 'boundary' + last_poly
    polygon_list.append(last_poly)

    footer = 'endstr' + footer
    
    for poly in polygon_list:
        initPolyObject(poly)

    # Specify number of polygons to print here
    polyStrings = writePolyObjects(poly_objList, num=2)

    with open(milestone1_output, 'w') as rw:
        rw.write(header)

        for polystr in polyStrings:
            for line in polystr:
                rw.write(line)

        rw.write(footer)


