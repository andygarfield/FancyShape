import arcpy


def polygon_2_line(input_fc, output_fc):
    """
    Converts a polygon feature class (FC) into a polyline FC.

    Extracts the vertices of each polygon, converts to point objects, and populates a polyline FC.
    :param input_fc: Input FC
    :param output_fc: Output FC
    :return:
    """
    
    # Create a FC that lives in memory, using the input FC spatial reference
    mem_fc = arcpy.CreateFeatureclass_management('in_memory', 'mem_fc', 'POLYLINE', None, None, None,
                                                 arcpy.Describe(input_fc).spatialReference)

    input_fc = arcpy.MultipartToSinglepart_management(input_fc)
    shapefieldname = arcpy.Describe(input_fc).ShapeFieldName

    # Cursor to create polylines
    cur = arcpy.da.InsertCursor(mem_fc, ['SHAPE@'])

    polycursor = arcpy.SearchCursor(input_fc)
    array = arcpy.Array()
    with open('C:\\Users\\Andy\\PycharmProjects\\FancyShape\\testing\\test.csv', 'w+') as csv:
    # Iterate over features in polygon FC and save vertices to array
        for feat in polycursor:
            polygon = feat.getValue(shapefieldname)
            for vertices in polygon:
                for vert in vertices:
                    if vert is None:
                        cur.insertRow([arcpy.Polyline(array)])
                        array.removeAll()
                    else:
                        array.add(arcpy.Point(vert.X, vert.Y))
                        csv.write(str(vert.X) + ',' + str(vert.Y) + '\n')
                cur.insertRow([arcpy.Polyline(array)])
                array.removeAll()

    arcpy.CopyFeatures_management(mem_fc, output_fc)


def line_2_polygon(input_fc, output_fc):
    """
    Converts a polyline FC into a polygon FC.

    Extracts the vertices of each polyline and attaches the first vertex to the last. In the future, the goal is to make
    the process work in a similar way to ArcGIS' process. That process only makes polygons out of lines that make an
    enclosed area. Shown here:
    http://desktop.arcgis.com/en/desktop/latest/tools/data-management-toolbox/GUID-601BAA73-E5EE-4275-AA89-68190423C8D2-web.png

    Known issues:
        This tool rounds every vertex to 4 decimal places. This isn't desirable for meters and feet coordinate systems,
        but is a very bad thing indeed for coordinate systems such as WGS 84.
        Not sure why it's doing this. I've read that ArcGIS rounds geometry without a defined coordinate system, but the
        temporary FC, which is created on the first line, uses the input FC coordinate system. Furthermore, the
        'polygon_2_line' function does not have the same problem, though it uses almost exactly the same logic. I've
        narrowed down the issue as occurring when the InsertCursor writes the array using 'insertRow.' This may be an
        ArcGIS bug. I'll work on a workaround soon.

        Not currently able to process lines to create interior rings in polygons.
    :param input_fc:
    :param output_fc:
    :return:
    """

    # Create a FC that lives in memory, using the input FC spatial reference
    mem_fc = arcpy.CreateFeatureclass_management('in_memory', 'mem_fc', 'POLYGON', None, None, None,
                                                 arcpy.Describe(input_fc).spatialReference)
    input_fc = arcpy.MultipartToSinglepart_management(input_fc)
    shapefieldname = arcpy.Describe(input_fc).ShapeFieldName

    # Cursor to create polylines
    cur = arcpy.da.InsertCursor(mem_fc, ['SHAPE@'])

    linecursor = arcpy.SearchCursor(input_fc)
    array = arcpy.Array()

    # Iterate over features in polyline FC and save vertices to array
    for feat in linecursor:
        line = feat.getValue(shapefieldname)
        for vertices in line:
            initial_x = vertices[0].X
            initial_y = vertices[0].Y
            for vert in vertices:
                array.add(arcpy.Point(vert.X, vert.Y))
            array.add(arcpy.Point(initial_x, initial_y))
            cur.insertRow([arcpy.Polygon(array)])
            array.removeAll()

    arcpy.CopyFeatures_management(mem_fc, output_fc)
