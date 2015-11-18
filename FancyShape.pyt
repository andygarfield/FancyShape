import arcpy
from conversion import polygon_2_line

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "FancyShape"
        self.alias = "fancyshape"

        # List of tool classes associated with this toolbox
        self.tools = [Polygon2Line]


class Polygon2Line(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Polygon to Line"
        self.description = "Converts a polygon feature class into a line feature class."
        self.canRunInBackground = False

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
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        in_features = parameters[0].valueAsText
        out_features = parameters[1].valueAsText

        polygon_2_line(in_features, out_features)
