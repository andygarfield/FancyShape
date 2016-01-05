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
    input_spatial_ref = arcpy.Describe(input_fc).spatialReference

    mem_fc = arcpy.CreateFeatureclass_management('in_memory', 'mem_fc', 'POLYLINE', None, None, None, input_spatial_ref)

    input_fc = arcpy.MultipartToSinglepart_management(input_fc)
    shapefieldname = arcpy.Describe(input_fc).ShapeFieldName

    # Cursor to create polylines
    cur = arcpy.da.InsertCursor(mem_fc, ['SHAPE@'])

    polycursor = arcpy.SearchCursor(input_fc)
    array = arcpy.Array()
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
            cur.insertRow([arcpy.Polyline(array, input_spatial_ref)])
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
        Not currently able to process lines to create interior rings in polygons.
    :param input_fc: Input FC
    :param output_fc: Output FC
    :return:
    """

    # Create a FC that lives in memory, using the input FC spatial reference
    input_spatial_ref = arcpy.Describe(input_fc).spatialReference

    mem_fc = arcpy.CreateFeatureclass_management('in_memory', 'mem_fc', 'POLYGON', None, None, None, input_spatial_ref)
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
                if vert is None:
                    continue
                else:
                    array.add(arcpy.Point(vert.X, vert.Y))
            array.add(arcpy.Point(initial_x, initial_y))
            cur.insertRow([arcpy.Polygon(array, input_spatial_ref)])
            array.removeAll()

    arcpy.CopyFeatures_management(mem_fc, output_fc)


def feature_2_point(input_fc, output_fc):
    """
    Converts a polyline FC into a point FC.

    :param input_fc: Input FC
    :param output_fc: Output FC
    :return:
    """

    input_spatial_ref = arcpy.Describe(input_fc).spatialReference

    mem_fc = arcpy.CreateFeatureclass_management('in_memory', 'mem_fc', 'POINT', None, None, None, input_spatial_ref)
    shapefieldname = arcpy.Describe(input_fc).ShapeFieldName

    # Cursor to create points
    pointcur = arcpy.da.InsertCursor(mem_fc, ['SHAPE@'])

    linecursor = arcpy.SearchCursor(input_fc)
    # array = arcpy.Array()

    # Iterate over features in polyline FC and save vertices to array
    points_using = []

    for feat in linecursor:
        shape = feat.getValue(shapefieldname)
        for vertices in shape:
            for vert in vertices:
                if vert is None:
                    continue
                else:
                    xy_tuple = (vert.X, vert.Y)
                    if xy_tuple not in points_using:
                        points_using.append(xy_tuple)

    for point in points_using:
        pointcur.insertRow([point])

    arcpy.CopyFeatures_management(mem_fc, output_fc)
