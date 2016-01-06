"""
Works like the Near tool in ArcGIS, though currently with less features.
"""

import arcpy


def near_tool(input_fc, near_fc):
    input_spatial_ref = arcpy.Describe(input_fc).spatialReference

    arcpy.AddField_management(input_fc, 'NEAR_FID', 'LONG')
    arcpy.AddField_management(input_fc, 'NEAR_DIST', 'DOUBLE')

    in_cursor = arcpy.da.UpdateCursor(input_fc, ['SHAPE@', 'Near_FID', 'Near_Dist'])
    near_cursor = arcpy.da.SearchCursor(near_fc, ['SHAPE@', 'OID@'])
    for in_row in in_cursor:
        nearest_fid = -1
        nearest_distance = -1.0
        for near_row in near_cursor:
            near_projected = near_row[0].projectAs(input_spatial_ref)
            if all([nearest_fid == -1, nearest_distance == -1.0]):
                nearest_distance = in_row[0].distanceTo(near_projected)
                nearest_fid = near_row[1]
                if nearest_distance == 0:
                    break
            elif in_row[0].distanceTo(near_projected) < nearest_distance:
                nearest_distance = in_row[0].distanceTo(near_projected)
                nearest_fid = near_row[1]
                if nearest_distance == 0:
                    break
        near_cursor.reset()
        in_row[1] = nearest_fid
        in_row[2] = nearest_distance
        in_cursor.updateRow(in_row)
