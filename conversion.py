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
    # Iterate over features in polygon FC and save vertices to array
    for feat in polycursor:
        polygon = feat.getValue(shapefieldname)
        for vertices in polygon:
            for vert in vertices:
                array.add(arcpy.Point(vert.X, vert.Y))
            cur.insertRow([arcpy.Polyline(array)])
            array.removeAll()
    arcpy.CopyFeatures_management(mem_fc, output_fc)
