import arcpy

def polygon_2_line(featureClass, outputFC):
    memFC = arcpy.CreateFeatureclass_management("in_memory", "memFC", "POLYLINE", None, None, None,
                                                arcpy.Describe(featureClass).spatialReference)
    featureClass = arcpy.MultipartToSinglepart_management(featureClass)
    shapefieldname = arcpy.Describe(featureClass).ShapeFieldName
    cur = arcpy.da.InsertCursor(memFC, ["SHAPE@"])
    array = arcpy.Array()
    features = arcpy.UpdateCursor(featureClass)

    for feat in features:
        polygon = feat.getValue(shapefieldname)

        for vertices in polygon:
            linecoordinates = []
            for vert in vertices:
                vertTuple = (vert.X, vert.Y)
                linecoordinates.append(vertTuple)
                # # newline = LineString(linecoordinates)
                # for vert in linecoordinates #newline.coords:
                array.add(arcpy.Point(vert.X, vert.Y))
            cur.insertRow([arcpy.Polyline(array)])
            array.removeAll()

    arcpy.CopyFeatures_management(memFC, outputFC)