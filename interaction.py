import vtk
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import math
df=pd.read_excel('D:\Google\CSE5544DataVisua/assign4/EHRdataSample.xlsx')
df['PatientID']=df['PatientID'].astype('object')
symptom_attrs = [
    'Stress', 'PTSD','Speech', 'Anxiety', 'Depression', 'Headache', 'Sleep', 'Audiology',
    'Vision', 'Neurologic', 'Alzheimer', 'Cognitive', 'PCS', 'Endocrine','Skull_inj', 'NON_skull_inj']
SymptomNum=df['Stress']
for j in symptom_attrs:
    SymptomNum=SymptomNum+df[j]
SymptomNum=SymptomNum-df['Stress']
df['SymptomNum']=SymptomNum


PatientID=df['PatientID'].unique()
#total number of symptoms
totalNum=[] 
for p in PatientID:
    totalNum.append(df[df['PatientID']==p]['SymptomNum'].sum())
totalUniqueNum=[]
for p in PatientID:
    df_p=df[df['PatientID']==p]
    count=0;
    for s in symptom_attrs:
        if any(df_p[s]!=0):
            count=count+1
    totalUniqueNum.append(count)
    
    
currentAge=[]
diagnoAge=[]
gender=[]
preMax=[]
postMax=[]
for p in PatientID:
    currentAge.append(df[df['PatientID']==p]['Age'].max())
    diagnoAge.append(df[df['PatientID']==p].loc[df['Days_From1stTBI']==0]['Age'].iloc[0])
    gender.append(df[df['PatientID']==p]['Gender'].iloc[0])
    preMax.append(abs(df[df['PatientID']==p]['PRE_max_days'].iloc[0]))
    postMax.append(abs(df[df['PatientID']==p]['POST_max_days'].iloc[0]))
df_patient=pd.DataFrame({'ID':PatientID,'totalNum':totalNum,'totalSympNum':totalUniqueNum,'diagnoAge':diagnoAge,
                         'currentAge':currentAge,'gender':gender,'preMax':preMax,'postMax':postMax})
df_patient.gender=df_patient.gender.replace(to_replace=['MALE','FEMALE'],value=[1,0])


X_pre=df_patient.drop('ID',axis=1)
scaler= MinMaxScaler()
X_scaled = scaler.fit_transform(X_pre)
#016345
X_coor=X_scaled[0:,0]*1+(X_scaled[0:,1]+X_scaled[0:,5])*0.5+(X_scaled[0:,6]+X_scaled[0:,4])*(-0.5)+X_scaled[0:,3]*(-1)
Y_coor=(X_scaled[0:,1]+X_scaled[0:,6])*math.sqrt(3)/2+(X_scaled[0:,4]+X_scaled[0:,5])*(-math.sqrt(3))/2


colors = vtk.vtkNamedColors()
NUMBER_OF_SPHERES = 41
def SliderCallbackMidPoint(obj, event):
    
    rep = obj.GetRepresentation()
    pointSize = rep.GetValue()
    for i in collection:
        i.GetProperty().SetPointSize(pointSize)
def MakeRep(text, vrange, v, x, dx):
    rep = vtk.vtkSliderRepresentation2D()
    rep.SetMinimumValue(vrange[0])
    rep.SetMaximumValue(vrange[1])
    rep.SetValue(float(v))
    rep.SetTitleText(text)
    rep.SetLabelFormat("%0.2f")
    rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
    rep.GetPoint1Coordinate().SetValue(x, 0.07)
    rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
    rep.GetPoint2Coordinate().SetValue(x+dx, 0.07)
    rep.SetSliderLength(0.005)
    rep.SetSliderWidth(0.02)
    rep.SetEndCapLength(0.002)
    rep.SetEndCapWidth(0.03)
    rep.SetTubeWidth(0.002)
    rep.GetTubeProperty().SetColor(0.9, 0.9, 0.9)
    rep.GetCapProperty().SetColor(0.9, 0.9, 0.9)
    rep.GetSliderProperty().SetColor(1, 1, 0)
    rep.GetTitleProperty().SetColor(1, 1, 1)
    rep.GetTitleProperty().ShadowOff()
    rep.GetTitleProperty().SetFontFamilyToTimes()
    rep.SetTitleHeight(0.02)
    rep.GetTitleProperty().BoldOff()
    rep.GetLabelProperty().SetColor(1, 1, 1)
    rep.SetLabelHeight(0.02)
    rep.GetLabelProperty().SetFontFamilyToTimes()
    rep.GetLabelProperty().BoldOff()
    rep.GetLabelProperty().ShadowOff()
    return rep

class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)

        self.LastPickedActor = None
        self.LastPickedProperty = vtk.vtkProperty()

    def leftButtonPressEvent(self, obj, event):
        clickPos = self.GetInteractor().GetEventPosition()

        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())

        # get the new
        self.NewPickedActor = picker.GetActor()

        # If something was selected
        if self.NewPickedActor:
            # If we picked something before, reset its property
            if self.LastPickedActor:
                self.LastPickedActor.GetProperty().DeepCopy(self.LastPickedProperty)

            # Save the property of the picked actor so that we can
            # restore it next time
            self.LastPickedProperty.DeepCopy(self.NewPickedActor.GetProperty())
            # Highlight the picked actor by changing its properties
            self.NewPickedActor.GetProperty().SetColor(colors.GetColor3d('Red'))
            self.NewPickedActor.GetProperty().SetDiffuse(1.0)
            self.NewPickedActor.GetProperty().SetSpecular(0.0)

            # save the last picked actor
            self.LastPickedActor = self.NewPickedActor

        self.OnLeftButtonDown()
        return


def main():
    # A renderer and render window
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(colors.GetColor3d('SteelBlue'))

    renwin = vtk.vtkRenderWindow()
    renwin.AddRenderer(renderer)

    # An interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renwin)

    # add the custom style
    style = MouseInteractorHighLightActor()
    style.SetDefaultRenderer(renderer)
    interactor.SetInteractorStyle(style)

    balloonRep = vtk.vtkBalloonRepresentation()
    balloonRep.SetBalloonLayoutToImageRight()
    balloonWidget = vtk.vtkBalloonWidget()
    balloonWidget.SetInteractor(interactor)
    balloonWidget.SetRepresentation(balloonRep)
    for i in range(NUMBER_OF_SPHERES):
       
        x = X_coor[i]
        y = Y_coor[i]
        z = 0
        points = vtk.vtkPoints()
        p = [x,y,z]

        # Create the topology of the point (a vertex)
        vertices = vtk.vtkCellArray()

        id = points.InsertNextPoint(p)
        vertices.InsertNextCell(1)
        vertices.InsertCellPoint(id)

        # Create a polydata object
        point = vtk.vtkPolyData()

        # Set the points and vertices we created as the geometry and topology of the polydata
        point.SetPoints(points)
        point.SetVerts(vertices)
        

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(point)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        balloonWidget.AddBalloon(actor, 'Patient{}'.format(PatientID[i]))

        r = vtk.vtkMath.Random(.4, 1.0)
        g = vtk.vtkMath.Random(.4, 1.0)
        b = vtk.vtkMath.Random(.4, 1.0)
        actor.GetProperty().SetDiffuseColor(r, g, b)
        actor.GetProperty().SetDiffuse(.8)
        actor.GetProperty().SetSpecular(.5)
        actor.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
        actor.GetProperty().SetSpecularPower(30.0)
        actor.GetProperty().SetPointSize(10)

        renderer.AddActor(actor)

    rep_mid = MakeRep("PointSize", (5, 30), 10, 0.025, 0.45) 
    widget_mid = vtk.vtkSliderWidget()
    widget_mid.SetInteractor(interactor)
    widget_mid.SetRepresentation(rep_mid)
    widget_mid.SetAnimationModeToJump()
    widget_mid.AddObserver("InteractionEvent", SliderCallbackMidPoint)
    widget_mid.EnabledOn()
    global collection #=vtkActorCollection()
    collection=renderer.GetActors();
    # Start
    interactor.Initialize()
    renwin.Render()
    balloonWidget.EnabledOn()
    interactor.Start()


if __name__ == '__main__':
    main()
