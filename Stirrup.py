from PySide import QtCore, QtGui
from Rebarfunc import *
from PySide.QtCore import QT_TRANSLATE_NOOP
import FreeCAD, FreeCADGui, os, sys
import math

def getpointsOfStirrup(FacePRM, s_cover, bentAngle, diameter, rounding, facenormal):
    angle = 180 - bentAngle
    tangent_part_length = extendedTangentPartLength(rounding, diameter, angle)
    tangent_length = extendedTangentLength(rounding, diameter, angle)
    if round(facenormal[0]) in {1,-1}:
        x1 = FacePRM[1][0]
        y1 = FacePRM[1][1] - FacePRM[0][0]/2 + s_cover
        z1 = FacePRM[1][2] + FacePRM[0][1]/2 - s_cover + tangent_part_length
        x2 = x1 - diameter/4
        y2 = FacePRM[1][1] - FacePRM[0][0]/2 + s_cover
        z2 = FacePRM[1][2] - FacePRM[0][1]/2 + s_cover
        x3 = x2 - diameter/4
        y3 = FacePRM[1][1] + FacePRM[0][0]/2 - s_cover
        z3 = FacePRM[1][2] - FacePRM[0][1]/2 + s_cover
        x4 = x3 - diameter/4
        y4 = FacePRM[1][1] + FacePRM[0][0]/2 - s_cover
        z4 = FacePRM[1][2] + FacePRM[0][1]/2 - s_cover
        x5 = x4 - diameter/4
        y5 = FacePRM[1][1] - FacePRM[0][0]/2 + s_cover - tangent_part_length
        z5 = FacePRM[1][2] + FacePRM[0][1]/2 - s_cover
        x0 = x1
        y0 = y1 + (tangent_length+4*diameter)* math.sin(math.radians(angle))
        z0 = z1 - (tangent_length+4*diameter) * math.cos(math.radians(angle))
        x6 = x5
        y6 = y5 + (tangent_length+4*diameter) * math.sin(math.radians(90-angle))
        z6 = z5 - (tangent_length+4*diameter) * math.cos(math.radians(90-angle))
    elif round(facenormal[1]) in {1,-1}:
        x1 = FacePRM[1][0] - FacePRM[0][0]/2 + s_cover
        y1 = FacePRM[1][1]
        z1 = FacePRM[1][2] + FacePRM[0][1]/2 - s_cover + tangent_part_length
        x2 = FacePRM[1][0] - FacePRM[0][0]/2 + s_cover
        y2 = y1 - diameter/4
        z2 = FacePRM[1][2] - FacePRM[0][1]/2 + s_cover
        x3 = FacePRM[1][0] + FacePRM[0][0]/2 - s_cover
        y3 = y2 - diameter/4
        z3 = FacePRM[1][2] - FacePRM[0][1]/2 + s_cover
        x4 = FacePRM[1][0] + FacePRM[0][0]/2 - s_cover
        y4 = y3 - diameter/4
        z4 = FacePRM[1][2] + FacePRM[0][1]/2 - s_cover
        x5 = FacePRM[1][0] - FacePRM[0][0]/2 + s_cover - tangent_part_length
        y5 = y4 - diameter/4
        z5 = FacePRM[1][2] + FacePRM[0][1]/2 - s_cover
        x0 = x1 + (tangent_length+4*diameter)* math.sin(math.radians(angle))
        y0 = y1
        z0 = z1 - (tangent_length+4*diameter) * math.cos(math.radians(angle))
        x6 = x5 + (tangent_length+4*diameter) * math.sin(math.radians(90-angle))
        y6 = y5
        z6 = z5 - (tangent_length+4*diameter) * math.cos(math.radians(90-angle))
    elif round(facenormal[2]) in {1,-1}:
        x1 = FacePRM[1][0] - FacePRM[0][0]/2 + s_cover
        y1 = FacePRM[1][1] + FacePRM[0][1]/2 - s_cover + tangent_part_length
        z1 = FacePRM[1][2]
        x2 = FacePRM[1][0] - FacePRM[0][0]/2 + s_cover
        y2 = FacePRM[1][1] - FacePRM[0][1]/2 + s_cover
        z2 = z1 - diameter/4
        x3 = FacePRM[1][0] + FacePRM[0][0]/2 - s_cover
        y3 = FacePRM[1][1] - FacePRM[0][1]/2 + s_cover
        z3 = z2 - diameter/4
        x4 = FacePRM[1][0] + FacePRM[0][0]/2 - s_cover
        y4 = FacePRM[1][1] + FacePRM[0][1]/2 - s_cover
        z4 = z3 - diameter/4
        x5 = FacePRM[1][0] - FacePRM[0][0]/2 + s_cover - tangent_part_length
        y5 = FacePRM[1][1] + FacePRM[0][1]/2 - s_cover
        z5 = z4 - diameter/4
        x0 = x1 + (tangent_length+4*diameter)* math.sin(math.radians(angle))
        y0 = y1 - (tangent_length+4*diameter) * math.cos(math.radians(angle))
        z0 = z1
        x6 = x5 + (tangent_length+4*diameter) * math.sin(math.radians(90-angle))
        y6 = y5 - (tangent_length+4*diameter) * math.cos(math.radians(90-angle))
        z6 = z5
    return [FreeCAD.Vector(x0, y0, z0), FreeCAD.Vector(x1, y1, z1),\
            FreeCAD.Vector(x2, y2, z2), FreeCAD.Vector(x3, y3, z3),\
            FreeCAD.Vector(x4, y4, z4), FreeCAD.Vector(x5, y5, z5),\
            FreeCAD.Vector(x6, y6, z6)]

class _StirrupTaskPanel:
    def __init__(self, Rebar = None):
        self.form = FreeCADGui.PySideUic.loadUi(os.path.splitext(__file__)[0]+".ui")
        self.form.setWindowTitle(QtGui.QApplication.translate("Arch", "Stirrup Rebar", None))
        self.form.bentAngle.addItems(["135","90"])
        self.form.amount_radio.clicked.connect(self.amount_radio_clicked)
        self.form.spacing_radio.clicked.connect(self.spacing_radio_clicked)
        #self.form.image.setPixmap(QtGui.QPixmap(os.path.split(os.path.abspath(__file__))[0]+"/icons/UShapeRebar.svg"))
        self.Rebar = Rebar

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Ok) | int(QtGui.QDialogButtonBox.Cancel)

    def accept(self):
        s_cover = self.form.sideCover.text()
        s_cover = FreeCAD.Units.Quantity(s_cover).Value
        f_cover = self.form.frontCover.text()
        f_cover = FreeCAD.Units.Quantity(f_cover).Value
        diameter = self.form.diameter.text()
        diameter = FreeCAD.Units.Quantity(diameter).Value
        bentAngle = int(self.form.bentAngle.currentText())
        rounding = self.form.rounding.value()
        amount_check = self.form.amount_radio.isChecked()
        spacing_check = self.form.spacing_radio.isChecked()
        if not self.Rebar:
            if amount_check == True:
                amount = self.form.amount.value()
                makeStirrup(s_cover, f_cover, bentAngle, diameter, rounding, True, amount)
            elif spacing_check == True:
                spacing = self.form.spacing.text()
                spacing = FreeCAD.Units.Quantity(spacing).Value
                makeStirrup(s_cover, f_cover, bentAngle, diameter, rounding, False, spacing)
        else:
            if amount_check == True:
                amount = self.form.amount.value()
                editStirrup(self.Rebar, s_cover, f_cover, bentAngle, diameter, rounding, True, amount)
            elif spacing_check == True:
                spacing = self.form.spacing.text()
                spacing = FreeCAD.Units.Quantity(spacing).Value
                editStirrup(self.Rebar, s_cover, f_cover, bentAngle, diameter, rounding, False, spacing)
        FreeCAD.Console.PrintMessage("Done!\n")
        FreeCADGui.Control.closeDialog(self)

    def amount_radio_clicked(self):
        self.form.spacing.setEnabled(False)
        self.form.amount.setEnabled(True)

    def spacing_radio_clicked(self):
        self.form.amount.setEnabled(False)
        self.form.spacing.setEnabled(True)


def makeStirrup(s_cover, f_cover, bentAngle, diameter, rounding, amount_spacing_check, amount_spacing_value):
    """ makeStirrup(s_cover, f_cover, bentAngle, diameter, rounding, amount_spacing_check, amount_spacing_value):
    Adds the Stirrup reinforcement bar to the selected structural object"""
    selected_obj = FreeCADGui.Selection.getSelectionEx()[0]
    StructurePRM = getTrueParametersOfStructure(selected_obj.Object)
    FacePRM = getParametersOfFace(selected_obj.Object, selected_obj.SubObjects[0], False)
    FaceNormal = selected_obj.SubObjects[0].normalAt(0,0)
    FaceNormal = selected_obj.SubObjects[0].Placement.Rotation.inverted().multVec(FaceNormal)
    if not FacePRM:
        FreeCAD.Console.PrintError("Cannot identified shape or from which base object sturctural element is derived\n")
        return
    # Calculate the coordinate values of Stirrup
    points = getpointsOfStirrup(FacePRM, s_cover, bentAngle, diameter, rounding, FaceNormal)
    import Draft
    line = Draft.makeWire(points,closed=False,face=True,support=None)
    import Arch
    line.Support = [(selected_obj.Object, selected_obj.SubElementNames[0])]
    if amount_spacing_check == True:
        rebar = Arch.makeRebar(selected_obj.Object, line, diameter, amount_spacing_value, f_cover)
    else:
        rebar = Arch.makeRebar(selected_obj.Object, line, diameter, int((StructurePRM[1]-diameter)/amount_spacing_value), f_cover)
    rebar.Direction = FaceNormal.negative()
    rebar.Rounding = rounding
    # Adds properties to the rebar object
    rebar.ViewObject.addProperty("App::PropertyString","RebarShape","RebarDialog",QT_TRANSLATE_NOOP("App::Property","Shape of rebar")).RebarShape = "Stirrup"
    rebar.ViewObject.setEditorMode("RebarShape",2)
    rebar.addProperty("App::PropertyDistance","SideCover","RebarDialog",QT_TRANSLATE_NOOP("App::Property","Side cover of rebar")).SideCover = s_cover
    rebar.setEditorMode("SideCover",2)
    rebar.addProperty("App::PropertyDistance","FrontCover","RebarDialog",QT_TRANSLATE_NOOP("App::Property","Top cover of rebar")).FrontCover = f_cover
    rebar.setEditorMode("FrontCover",2)
    rebar.addProperty("App::PropertyInteger","BentAngle","RebarDialog",QT_TRANSLATE_NOOP("App::Property","Bent angle between at the end of rebar")).BentAngle = bentAngle
    rebar.setEditorMode("BentAngle",2)
    rebar.addProperty("App::PropertyInteger","TrueRounding","RebarDialog",QT_TRANSLATE_NOOP("App::Property","Bottom cover of rebar")).TrueRounding = rounding
    rebar.setEditorMode("TrueRounding",2)
    rebar.addProperty("App::PropertyBool","AmountCheck","RebarDialog",QT_TRANSLATE_NOOP("App::Property","Amount radio button is checked")).AmountCheck
    rebar.setEditorMode("AmountCheck",2)
    rebar.addProperty("App::PropertyDistance","TrueSpacing","RebarDialog",QT_TRANSLATE_NOOP("App::Property","Spacing between of rebars")).TrueSpacing = amount_spacing_value
    rebar.setEditorMode("TrueSpacing",2)
    if amount_spacing_check:
        rebar.AmountCheck = True
    else:
        rebar.AmountCheck = False
        rebar.TrueSpacing = amount_spacing_value
    FreeCAD.ActiveDocument.recompute()

def editStirrup(Rebar, s_cover, f_cover, bentAngle, diameter, rounding, amount_spacing_check, amount_spacing_value):
    sketch = Rebar.Base
    # Check if sketch support is empty.
    if not sketch.Support:
        showWarning("You have checked remove external geometry of base sketchs when needed.\nTo unchecked Edit->Preferences->Arch.")
        return
    # Assigned values
    facename = sketch.Support[0][1][0]
    structure = sketch.Support[0][0]
    face = structure.Shape.Faces[int(facename[-1])-1]
    StructurePRM = getTrueParametersOfStructure(structure)
    # Get parameters of the face where sketch of rebar is drawn
    FacePRM = getParametersOfFace(structure, face, False)
    FaceNormal = face.normalAt(0,0)
    FaceNormal = face.Placement.Rotation.inverted().multVec(FaceNormal)

    # Calculate the coordinates value of U-Shape rebar
    points = getpointsOfStirrup(FacePRM, s_cover, bentAngle, diameter, rounding, FaceNormal)
    Rebar.Base.Points = points
    FreeCAD.ActiveDocument.recompute()
    Rebar.OffsetStart = f_cover
    Rebar.OffsetEnd = f_cover
    Rebar.BentAngle = bentAngle
    Rebar.Rounding = rounding
    Rebar.Diameter = diameter
    if amount_spacing_check == True:
        Rebar.Amount = amount_spacing_value
        FreeCAD.ActiveDocument.recompute()
        Rebar.AmountCheck = True
    else:
        Rebar.Amount = int((StructurePRM[1]-diameter)/amount_spacing_value)
        FreeCAD.ActiveDocument.recompute()
        Rebar.AmountCheck = False
    Rebar.FrontCover = f_cover
    Rebar.SideCover = s_cover
    Rebar.TrueRounding = rounding
    Rebar.TrueSpacing = amount_spacing_value
    FreeCAD.ActiveDocument.recompute()

def editDialog(vobj):
    FreeCADGui.Control.closeDialog()
    obj = _StirrupTaskPanel(vobj.Object)
    obj.form.frontCover.setText(str(vobj.Object.FrontCover))
    obj.form.sideCover.setText(str(vobj.Object.SideCover))
    obj.form.diameter.setText(str(vobj.Object.Diameter))
    obj.form.bentAngle.setCurrentIndex(obj.form.bentAngle.findText(str(vobj.Object.BentAngle)))
    obj.form.rounding.setValue(vobj.Object.TrueRounding)
    if vobj.Object.AmountCheck == True:
        obj.form.amount.setValue(vobj.Object.Amount)
    else:
        obj.form.amount_radio.setChecked(False)
        obj.form.spacing_radio.setChecked(True)
        obj.form.amount.setDisabled(True)
        obj.form.spacing.setEnabled(True)
        obj.form.spacing.setText(str(vobj.Object.TrueSpacing))
    FreeCADGui.Control.showDialog(obj)

def CommandStirrup():
    selected_obj = check_selected_face()
    if selected_obj:
        FreeCADGui.Control.showDialog(_StirrupTaskPanel())