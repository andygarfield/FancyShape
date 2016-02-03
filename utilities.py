import arcpy
import ConversionUtils
import os
import datetime
import re
from os.path import split


def create_layer_version(layer_multi_input):
    """
    Takes input layers, creates a shapefile or feature class, and re-sources the input layers to the new layer. If the
    layer already exists. Re-source the layer to the existing one.

    :param layer_multi_input: Layer list separated by semicolons.
    :return:
    """
    layers = ConversionUtils.SplitMultiInputs(layer_multi_input)

    for layer in layers:
        desc = arcpy.Describe(layer)
        old_name = os.path.basename(desc.dataElement.catalogPath).split('.')[0]
        new_name = create_new_name(old_name)

        if new_name == old_name:
            pass
        else:
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


def create_new_name(old_name):
    """
    Process the previous file name and make a new name.
    :param old_name: Unprocessed name
    :return:
    """
    # Check for name conditions
    if re.search('_\d\d\d\d\d\d\d\d$', old_name) is not None:
        has_date = True
    else:
        has_date = False

    # Strip old date
    if has_date:
        stripped_name = old_name[:-9]
    else:
        stripped_name = old_name

    new_name = '%s_%s' % (stripped_name, create_date_string())

    return new_name


def create_date_string():
    current_year = str(datetime.date.today().year)

    if datetime.date.today().month < 10:
        current_month = '0' + str(datetime.date.today().month)
    else:
        current_month = str(datetime.date.today().month)

    if datetime.date.today().day < 10:
        current_day = '0' + str(datetime.date.today().day)
    else:
        current_day = str(datetime.date.today().day)

    return current_year + current_month + current_day


if __name__ == '__main__':
    in_layers = ConversionUtils.gp.GetParameterAsText(0)
    create_layer_version(in_layers)


def project_better(in_dataset, out_dataset, spatial_reference):
    # Script borrowed from http://joshwerts.com/blog/2015/09/10/arcpy-dot-project-in-memory-featureclass/
    # Can project a dataset and put the output in an 'in_memory' workspace

    path, name = split(out_dataset)
    arcpy.CreateFeatureclass_management(path, name, arcpy.Describe(in_dataset).shapeType,
                                        template=in_dataset,
                                        spatial_reference=spatial_reference)

    # specify copy of all fields from source to destination
    fields = ["Shape@"] + [f.name for f in arcpy.ListFields(in_dataset) if not f.required]

    # project source geometries on the fly while inserting to destination featureclass
    with arcpy.da.SearchCursor(in_dataset, fields, spatial_reference=spatial_reference) as source_curs, \
         arcpy.da.InsertCursor(out_dataset, fields) as ins_curs:
        for row in source_curs:
          ins_curs.insertRow(row)
