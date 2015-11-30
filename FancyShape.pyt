import arcpy
import ConversionUtils
import utilities
import conversion


class Toolbox(object):
    def __init__(self):
        self.label = "FancyShape"
        self.alias = "fancyshape"

        # List of tool classes associated with this toolbox
        self.tools = [Polygon2Line, Line2Polygon, NewLayerVersion]


class Polygon2Line(object):
    def __init__(self):
        self.label = "Polygon to Line"
        self.description = "Converts a polygon feature class into a polyline feature class."
        self.canRunInBackground = False
        self.category = 'Feature Management'

    def getParameterInfo(self):
        in_features = arcpy.Parameter(
            displayName='Input Features',
            name='in_features',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Input'
        )
        out_features = arcpy.Parameter(
            displayName='Output Features',
            name='out_features',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Output'
        )
        parameters = [in_features, out_features]
        return parameters

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        in_features = parameters[0].valueAsText
        out_features = parameters[1].valueAsText

        conversion.polygon_2_line(in_features, out_features)


class Line2Polygon(object):
    def __init__(self):
        self.label = "Line to Polygon"
        self.description = "Converts a polyline feature class into a polygon feature class."
        self.canRunInBackground = False
        self.category = 'Feature Management'

    def getParameterInfo(self):
        in_features = arcpy.Parameter(
            displayName='Input Features',
            name='in_features',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Input'
        )
        out_features = arcpy.Parameter(
            displayName='Output Features',
            name='out_features',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Output'
        )
        parameters = [in_features, out_features]
        return parameters

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        in_features = parameters[0].valueAsText
        out_features = parameters[1].valueAsText

        conversion.line_2_polygon(in_features, out_features)


class NewLayerVersion(object):
    def __init__(self):
        self.label = "Create New Layer Version"
        self.description = "Creates a dated new version of the input layers."
        self.canRunInBackground = False
        self.category = 'Utilities'

    def getParameterInfo(self):
        in_features = arcpy.Parameter(
            displayName='Input Features',
            name='in_features',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Input',
            multiValue=True)
        parameters = [in_features]
        return parameters

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        in_layers = ConversionUtils.gp.GetParameterAsText(0)
        arcpy.AddMessage(in_layers)
        utilities.create_layer_version(in_layers)
