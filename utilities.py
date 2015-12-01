import arcpy
import ConversionUtils
import os
import datetime
import re

def create_layer_version(layer_multi_input):
    """
    Takes input layers, creates a shapefile or feature class, and re-sources the input layers to the new layer.

    :param layer_multi_input: Layer list separated by semicolons.
    :return:
    """
    layers = ConversionUtils.SplitMultiInputs(layer_multi_input)

    date_string = create_date_string()

    for layer in layers:
        desc = arcpy.Describe(layer)
        # arcpy.AddMessage(desc.dataElement.catalogPath)
        old_name = os.path.basename(desc.dataElement.catalogPath).split('.')[0]
        if re.search('_\d\d\d\d\d\d\d\d$', old_name) is not None:
            base_old_name = '_'.join(old_name.split('_')[:-1])
            new_name = '%s_%s' % (base_old_name, date_string)
        else:
            new_name = '%s_%s' % (old_name, date_string)
        arcpy.CopyFeatures_management(desc.dataElement.catalogPath, os.path.dirname(desc.dataElement.catalogPath) +
                                      '\\' + new_name)
        if '.shp' in desc.dataElement.catalogPath:
            arcpy.mapping.Layer(layer).replaceDataSource(os.path.dirname(desc.dataElement.catalogPath),
                                                         'SHAPEFILE_WORKSPACE', new_name)
        if '.gdb' in desc.dataElement.catalogPath:
            arcpy.mapping.Layer(layer).replaceDataSource(os.path.dirname(desc.dataElement.catalogPath),
                                                         'FILEGDB_WORKSPACE', new_name)
        if '.mdb' in desc.dataElement.catalogPath:
            arcpy.mapping.Layer(layer).replaceDataSource(os.path.dirname(desc.dataElement.catalogPath),
                                                         'ACCESS_WORKSPACE', new_name)


def create_date_string():
    current_year = str(datetime.date.today().year)

    if datetime.date.today().month < 10:
        current_month = "0" + str(datetime.date.today().month)
    else:
        current_month = str(datetime.date.today().month)

    if datetime.date.today().day < 10:
        current_day = "0" + str(datetime.date.today().day)
    else:
        current_day = str(datetime.date.today().day)

    return current_year + current_month + current_day
