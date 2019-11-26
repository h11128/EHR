import vtk
import sys
import math
import random
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

max_record = 1
max_person = 41

class PointSet():
  def __init__(self, person_id,  feature, points):
    self.sphereSource = vtk.vtkSphereSource()
    # sphereSource.SetCenter(0.0, 0.0, 0.0)
    self.sphereSource.SetRadius(0.01)
    self.person_id = person_id
    self.points = vtk.vtkPoints()
    self.points.SetDataTypeToFloat()
    
    if person_id == -1:
      num_points = len(feature)
    else:
      num_points = max_record
    self.points.SetNumberOfPoints(num_points)
    
    self.points.SetPoint(0,1,0,0)

    self.graph = vtk.vtkPolyData()
    self.graph.SetPoints(points)

    self.glyph3D = vtk.vtkGlyph3D()
    self.glyph3D.SetSourceConnection(self.sphereSource.GetOutputPort())
    self.glyph3D.SetInputData(self.graph)
    self.glyph3D.Update()

    self.mapper = vtk.vtkPolyDataMapper()
    self.mapper.SetInputConnection(self.glyph3D.GetOutputPort())
    self.mapper.Update()


class pointCallBack(object):
  def __init__(self, sliderRep, sliderRep2, sliderRep3, personlist, max_record, max_person, point_xyz, actorList):
    self.sliderRep = sliderRep
    self.sliderRep2 = sliderRep2
    self.sliderRep3 = sliderRep3
    self.personlist = personlist
    self.max_record = max_record
    self.max_person = max_person
    self.point_xyz = point_xyz
    self.actorList = actorList
    super().__init__()

  def __call__(self, caller, event):
    # print("the value is " + str(self.sliderRep.GetValue()))
    person = int(self.sliderRep2.GetValue())
    record = int(self.sliderRep.GetValue())
    pointSize = float(self.sliderRep3.GetValue())

    for i in range(max_person):
      self.personlist[i].sphereSource = vtk.vtkSphereSource()
      # # sphereSource.SetCenter(0.0, 0.0, 0.0)
      self.personlist[i].sphereSource.SetRadius(pointSize)

      for j in range(max_record):
        index = (i)*max_record + j
        #print(i, j, index)
        if (person ==0 or record ==0):
          self.personlist[i].points.SetPoint(0,0,0,0)
        elif (i>person or j >record):
          self.personlist[i].points.SetPoint(0, 0,0,0)
        else:
          self.personlist[i].points.SetPoint(j, self.point_xyz[index])

      # g = vtk.vtkPolyData()
      self.personlist[i].graph.SetPoints(self.personlist[i].points)

      # glyph3D = vtk.vtkGlyph3D()
      self.personlist[i].glyph3D.SetSourceConnection(self.personlist[i].sphereSource.GetOutputPort())
      self.personlist[i].glyph3D.SetInputData(self.personlist[i].graph)
      self.personlist[i].glyph3D.Update()

      self.personlist[i].mapper.SetInputConnection(self.personlist[i].glyph3D.GetOutputPort())
      self.personlist[i].mapper.Update()
      actor = actorList[i]
      actor.SetMapper(self.personlist[i].mapper)
      actor.GetProperty().SetColor(1-i/(person+1),i/(person+1),0)
      actor.Modified()
    # print("person: %d record: %d"% (person, record))
    # print(self.pointset.points.GetNumberOfPoints())

def slider(renderer, maximum, x, y, renderWindowInteractor, title):
  sliderRep = vtk.vtkSliderRepresentation2D()
  sliderRep.SetRenderer(renderer)
  sliderRep.SetMinimumValue(0)
  sliderRep.SetMaximumValue(maximum)
  if title == 'point size':
    sliderRep.SetValue(0.05)
  else:
    sliderRep.SetValue(0)
  sliderRep.SetTitleText(title)

  sliderRep.GetPoint1Coordinate().SetCoordinateSystemToDisplay()
  sliderRep.GetPoint1Coordinate().SetValue(x, y)
  sliderRep.GetPoint2Coordinate().SetCoordinateSystemToDisplay()
  sliderRep.GetPoint2Coordinate().SetValue(x+400, y)
  sliderRep.BuildRepresentation()

  sliderWidget = vtk.vtkSliderWidget()
  sliderWidget.SetInteractor(renderWindowInteractor)
  sliderWidget.SetRepresentation(sliderRep)
  sliderWidget.SetAnimationModeToAnimate()
  sliderWidget.EnabledOn()
  return sliderRep, sliderWidget


def getLinesActor(feature):
  linesPolyData = vtk.vtkPolyData()

  # Create three points
  origin = [0.0, 0.0, 0.0]

  # Create a vtkPoints container and store the points in it
  pts = vtk.vtkPoints()
  pts.InsertNextPoint(origin)
  linesPolyData.SetPoints(pts)
  lines = vtk.vtkCellArray()
  colors = vtk.vtkUnsignedCharArray()
  colors.SetNumberOfComponents(3)
  namedColors = vtk.vtkNamedColors()
  for i in range(len(feature)):
    pts.InsertNextPoint(feature[i])
      # Create the first line (between Origin and P0)
    line0 = vtk.vtkLine()
    line0.GetPointIds().SetId(0, 0)  # the second 0 is the index of the Origin in linesPolyData's points
    line0.GetPointIds().SetId(1, i+1)
    lines.InsertNextCell(line0)
    try:
        colors.InsertNextTupleValue(namedColors.GetColor3ub("White"))
    except AttributeError:
        # For compatibility with new VTK generic data arrays.
        colors.InsertNextTypedTuple(namedColors.GetColor3ub("White"))
  # Add the lines to the polydata container
  linesPolyData.SetLines(lines)
  linesPolyData.GetCellData().SetScalars(colors)

  # Setup the visualization pipeline
  mapper = vtk.vtkPolyDataMapper()
  mapper.SetInputData(linesPolyData)

  actor = vtk.vtkActor()
  actor.SetMapper(mapper)
  actor.GetProperty().SetLineWidth(4)

  return actor
  
def normalizeVector(original_vector):
  length = math.sqrt(sum([i*i for i in original_vector]))
  final_vector = [i/length for i in original_vector]
  return final_vector
  
def computeVector(vector_number, rho_x, rho_y, rho_z, angle1, angle2, mode):
  #angle mode
  if mode == 0:
    vector = [math.cos(angle1), math.sin(angle1), math.cos(angle2)]
  #disimilarity mode, where similar vector will far from each other
  elif mode == 1:
    vector = [-rho_x, -rho_y, -rho_z]
  #similarity mode, where similar vector will close to each other
  elif mode ==2:
    vector = [rho_x, rho_y, rho_z]
  #generative mode: where vector will equally divide the space in a generative manner
  elif mode ==3:
    base0 = [1,0,0]
    base1 = [0,1,0]
    base2 = [0,0,1]
    
    baseVector = [base0,base1,base2,[-1,0,0],[0,-1,0],[0,0,-1],[math.sqrt(1/2), math.sqrt(1/2), 0] ]
    vector = []
  
  final_vector = normalizeVector(vector)
  return final_vector

def featureVector(filename):
  pd_read = pd.read_csv(filename)
  num_feature = len(list(pd_read.iloc[0,:]))-1
  
  total_feature = [[1,0,0],[0,1,0],[0,0,1]]
  features = []
  angle1 = random.random()*math.pi
  angle2 = random.random()*math.pi
  
  for i in range(num_feature):
    features.append(list(pd_read.iloc[:,i+1]))
  rowsCount = len(features[0])
  colsCount = len(features)
  for i in range(num_feature-3):
    total_feature.append([0,0,0])
  # gender, age_group, date_of_injury, PRE_max_days, POST_max_days, and Symptom frequency

    rho_x, _ = pearsonr(features[0], features[i])
    rho_y, _ = pearsonr(features[1], features[i])
    rho_z, _ = pearsonr(features[2], features[i])
    print(rho_x, rho_y, rho_z)
    angle1 = (abs(rho_x) + 1) / (rho_x+1+rho_y+1) * math.pi
    angle2 = (abs(rho_z) +1)/ 2 * math.pi
    vector = computeVector(i, rho_x, rho_y, rho_z, angle1, angle2, 1)
    total_feature[i+3] = vector

  return total_feature
  
def pointCalculate(rootTable, feature):
  rowsCount = rootTable.GetNumberOfRows()
  colsCount = rootTable.GetNumberOfColumns()

  points_data = [tuple([0 for _ in range(colsCount-1)]) for _ in range(max_person*max_record)]
  
  patient_count = 0
  patient = {}
  for i in range(rowsCount):
    data =[0 for _ in range(colsCount)]
    # patient_id, gender, age_group, date_of_injury, PRE_max_days, POST_max_days, and Symptom frequency
    patient_id = 0
    point_id = 0
    for j in range(colsCount):
        data[j] = rootTable.GetValue(i,j).ToFloat()
    if data[0] not in patient:
      patient[data[0]] = [patient_count, 0]
      patient_id = patient_count
      patient_count += 1
      point_id = 0
    else:
      patient_id = patient[data[0]][0]
      point_id = patient[data[0]][1] +1
      patient[data[0]] = [patient_id, point_id]
    
    index = patient_id*max_record + point_id
    points_data[index] = tuple(data[1:])
  #print(points_data)
  #print(len(patient))
  points_array = np.array(points_data)
  feature_array = np.array(feature)
  print(points_array)
  point_coordinate = np.dot(points_array, feature).tolist()
  return point_coordinate


  
    
    



if __name__ == '__main__':
  EHRDataPath = sys.argv[1]

  reader = vtk.vtkDelimitedTextReader()
  reader.SetFileName(EHRDataPath)
  reader.DetectNumericColumnsOn()
  reader.SetFieldDelimiterCharacters(',')
  reader.Update()

  rootTable = reader.GetOutput()
  feature = featureVector(EHRDataPath)
  point_xyz = pointCalculate(rootTable, feature)
  renderer = vtk.vtkRenderer()
  renderWindow = vtk.vtkRenderWindow()
  renderWindow.AddRenderer(renderer)
  renderer.SetBackground(.1, .2, .3)

  renderWindowInteractor = vtk.vtkRenderWindowInteractor()
  renderWindowInteractor.SetRenderWindow(renderWindow)

  
  sliderRep1, sliderWidget1 = slider(renderer, max_record, 40, 540, renderWindowInteractor, "record")
  sliderRep2, sliderWidget2 = slider(renderer, max_person, 40, 340, renderWindowInteractor, "person")
  sliderRep3, sliderWidget3 = slider(renderer, 0.1, 40, 140, renderWindowInteractor, "point size")
  
  balloonRep = vtk.vtkBalloonRepresentation()
  balloonRep.SetBalloonLayoutToImageRight()
  balloonWidget = vtk.vtkBalloonWidget()
  balloonWidget.SetInteractor(renderWindowInteractor)
  balloonWidget.SetRepresentation(balloonRep)


  # points, pointsActor = getPointsActor()
  points = vtk.vtkPoints()
  personlist = []
  for i in range(max_person):
    personlist.append(PointSet(i, feature, points))
  linesActor = getLinesActor(feature)
  actorList = []
  for i in range(max_person):

    actor = vtk.vtkActor()
    actor.SetMapper(personlist[i].mapper)
    actor.GetProperty().SetColor(0,1,0)
    actor.Modified()
    actorList.append(actor)
    balloonWidget.AddBalloon(actor, 'Patient{}'.format(i))

  callback = pointCallBack(sliderRep1, sliderRep2, sliderRep3, personlist,  max_record, max_person, point_xyz, actorList)
  sliderWidget1.AddObserver("InteractionEvent", callback)
  sliderWidget2.AddObserver("InteractionEvent", callback)
  sliderWidget3.AddObserver("InteractionEvent", callback)
  
  axes = vtk.vtkAxesActor()

  #renderer.AddActor(axes)
  for i in range(max_person):
    renderer.AddActor(actorList[i])
  renderer.AddActor(linesActor)
  renderer.ResetCamera()
  renderWindow.Render()
  renderWindow.SetSize(2000, 1500)
  balloonWidget.EnabledOn()
  renderWindowInteractor.Start()
