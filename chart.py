import vtk
import sys
import math
import random
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

max_record = 1
max_person = 41
max_point_per_person = 15

class PointSet():
  def __init__(self, person_id,  feature, frequency_count, radius):
    self.sphereSource = vtk.vtkSphereSource()
    # sphereSource.SetCenter(0.0, 0.0, 0.0)
    self.sphereSource.SetRadius(radius)
    self.person_id = person_id
    self.points = vtk.vtkPoints()
    self.points.SetDataTypeToFloat()
    self.frequency_count = frequency_count
    if person_id >= -1:
      self.frequency = frequency_count[person_id][-1]
    
    if person_id == -1:
      num_points = len(feature)
      self.feature = feature
      
      self.points.SetNumberOfPoints(num_points)
      for i in range(num_points):
        
        self.points.SetPoint(i,feature[i])
      self.sphereSource.SetRadius(radius)
    elif person_id < -1:
      self.points.SetNumberOfPoints(max_point_per_person - 1)
      for i in range(max_point_per_person - 1):
        self.points.SetPoint(i,0,0,0)
    else:
      self.points.SetNumberOfPoints(max_record)
      self.points.SetPoint(0,point_xyz[person_id])

    self.graph = vtk.vtkPolyData()
    self.graph.SetPoints(self.points)

    self.glyph3D = vtk.vtkGlyph3D()
    self.glyph3D.SetSourceConnection(self.sphereSource.GetOutputPort())
    self.glyph3D.SetInputData(self.graph)
    self.glyph3D.Update()

    self.mapper = vtk.vtkPolyDataMapper()
    self.mapper.SetInputConnection(self.glyph3D.GetOutputPort())
    self.mapper.Update()


class pointCallBack(object):
  def __init__(self, sliderRep, sliderRep2, sliderRep3, personlist, person_middle_list,
                point_xyz, middle_points, actorList, middlePointsActorList, tActor):
    self.sliderRep = sliderRep
    self.sliderRep2 = sliderRep2
    self.sliderRep3 = sliderRep3
    self.personlist = personlist
    self.person_middle_list = person_middle_list
    self.point_xyz = point_xyz
    self.middle_points = middle_points
    self.actorList = actorList
    self.middlePointsActorList = middlePointsActorList
    self.tActor = tActor
    super().__init__()

  def __call__(self, caller, event):
    # print("the value is " + str(self.sliderRep.GetValue()))
    person = int(self.sliderRep2.GetValue())
    record = int(self.sliderRep.GetValue())
    pointSize = float(self.sliderRep3.GetValue())
    _, self.tActor[1] = drawtrajectory(person, self.middle_points, self.personlist[0].frequency_count)
    print("KKK", self.tActor[1].GetLines().GetSize())
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(self.tActor[1])
    mapper.Update()
    self.tActor[0] = vtk.vtkActor()
    self.tActor[0].SetMapper(mapper)
    self.tActor[0].GetProperty().SetLineWidth(2)
    self.tActor[0].Modified()
    for i in range(max_person):
      self.personlist[i].sphereSource = vtk.vtkSphereSource()
      # # sphereSource.SetCenter(0.0, 0.0, 0.0)
      self.personlist[i].sphereSource.SetRadius(pointSize)

      for j in range(max_record):
        index = (i)*max_record + j
        if (person ==0 or record ==0):
          self.personlist[i].points.SetPoint(0,0,0,0)
        elif (i>person or j >record):
          self.personlist[i].points.SetPoint(0,0,0,0)
        else:
          self.personlist[i].points.SetPoint(j, self.point_xyz[index])
      
      self.personlist[i].graph = vtk.vtkPolyData()
      self.personlist[i].graph.SetPoints(self.personlist[i].points)
      self.personlist[i].glyph3D = vtk.vtkGlyph3D()
      self.personlist[i].glyph3D.SetSourceConnection(self.personlist[i].sphereSource.GetOutputPort())
      self.personlist[i].glyph3D.SetInputData(self.personlist[i].graph)
      self.personlist[i].glyph3D.Update()
      
      self.personlist[i].mapper.SetInputConnection(self.personlist[i].glyph3D.GetOutputPort())
      self.personlist[i].mapper.Update()
      self.actorList[i].SetMapper(self.personlist[i].mapper)
      self.actorList[i].GetProperty().SetColor(1, 1, 1)
      self.actorList[i].GetProperty().SetEdgeColor(self.personlist[i].frequency_count[i][-1]/(10),
        1 - self.personlist[i].frequency_count[i][-1]/(10),0)
      self.actorList[i].GetProperty().EdgeVisibilityOn()
      self.actorList[i].Modified()

      # Handle middle points
      self.person_middle_list[i].sphereSource = vtk.vtkSphereSource()
      self.person_middle_list[i].sphereSource.SetRadius(pointSize * 0.5)

      tmp_len = len(self.middle_points[i])
      # The last point is not middle point, so don't show it
      for j in range(tmp_len - 1):
        x, y, z = self.middle_points[i][j]
        if person == 0 or i > person:
          self.person_middle_list[i].points.SetPoint(j, 0, 0, 0)
        else:
          self.person_middle_list[i].points.SetPoint(j, x, y, z)
          

      self.person_middle_list[i].graph = vtk.vtkPolyData()
      self.person_middle_list[i].graph.SetPoints(self.person_middle_list[i].points)
      self.person_middle_list[i].glyph3D = vtk.vtkGlyph3D()
      self.person_middle_list[i].glyph3D.SetSourceConnection(self.person_middle_list[i].sphereSource.GetOutputPort())
      self.person_middle_list[i].glyph3D.SetInputData(self.person_middle_list[i].graph)
      self.person_middle_list[i].glyph3D.Update()
      self.person_middle_list[i].mapper.SetInputConnection(self.person_middle_list[i].glyph3D.GetOutputPort())
      self.person_middle_list[i].mapper.Update()
      self.middlePointsActorList[i].SetMapper(self.person_middle_list[i].mapper)
      self.middlePointsActorList[i].GetProperty().SetColor(1, 1, 1)
      self.middlePointsActorList[i].GetProperty().SetEdgeColor(self.personlist[i].frequency_count[i][-1]/(10),
        1 - self.personlist[i].frequency_count[i][-1]/(10),0)
      self.middlePointsActorList[i].GetProperty().EdgeVisibilityOn()
      self.middlePointsActorList[i].Modified()

def slider(renderer, maximum, x, y, renderWindowInteractor, title):
  sliderRep = vtk.vtkSliderRepresentation2D()
  sliderRep.SetRenderer(renderer)
  sliderRep.SetMinimumValue(0)
  sliderRep.SetMaximumValue(maximum)
  if title == 'point size':
    sliderRep.SetValue(0.05)
  elif title == 'record':
    sliderRep.SetValue(max_record)
  elif title == 'person':
    sliderRep.SetValue(max_person)
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


def getCoordinatesActor(feature):
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
    
    baseVector = [base0,base1,base2,[-1,0,0],[0,-1,0],[0,0,-1]]
    value = 1/math.sqrt(3)
    baseVector.append([value, value, value])
    baseVector.append([-value, value, value])
    baseVector.append([value, -value, value])
    baseVector.append([value, value, -value])
    baseVector.append([1, 1, 0])
    baseVector.append([-value, -value, value])
    baseVector.append([-value, value, -value])
    baseVector.append([value, -value, -value])
    baseVector.append([-value, -value, -value])
    vector = baseVector[vector_number]
  
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
    angle1 = (abs(rho_x) + 1) / (rho_x+1+rho_y+1) * math.pi
    angle2 = (abs(rho_z) +1)/ 2 * math.pi
    vector = computeVector(i+3, rho_x, rho_y, rho_z, angle1, angle2, 3)
    total_feature[i+3] = vector
  return total_feature
  
def pointCalculate(rootTable, feature):
  rowsCount = rootTable.GetNumberOfRows()
  colsCount = rootTable.GetNumberOfColumns()
  #print(rowsCount, colsCount)
  feature_array = np.array(feature)
  # delete feature stress since not useful, not need first column person_id
  points_data = [tuple([0 for _ in range(colsCount-1)]) for _ in range(max_person*max_record)]
  #print(len(points_data))
  all_middle_points = []
  patient_count = 0
  patient = {}
  frequency_count = [[0 for _ in range(len(feature)+1)] for _ in range(max_person*max_record)]
  for i in range(rowsCount):
    data =[0 for _ in range(colsCount)]
    # original feature: patient_id, gender, age_group, date_of_injury, PRE_max_days, POST_max_days, and Symptom frequency
    # changed feature: 1st_sympton_duration, 2nd_symptom_duration, ......, 15th_symptom_duration
    # symptom duration is calculated from (symptom_occurence_date - date_injury) and 
    #   do normalization under the same scale for all patients
    # change the allocation of vector to be equally divide the space
    patient_id = 0
    point_id = 0
    for j in range(colsCount):
        
      data[j] = rootTable.GetValue(i,j).ToFloat()
      if data[j] < 0.0001:
        data[j] = 0
    if data[0] not in patient:
      patient[data[0]] = [patient_count, 0]
      patient_id = patient_count
      patient_count += 1
      point_id = 0
    else:
      patient_id = patient[data[0]][0]
      point_id = patient[data[0]][1] +1
      patient[data[0]] = [patient_id, point_id]
    
    index = patient_id*max_record
    #print(rowsCount)
    #print(index)
    points_data[index] = data[1:]

    middle_points = []
    temp = [0,0,0]
    for k in range(colsCount -1):
      middle_point = [j * points_data[index][k] for j in feature[k]]
      if points_data[index][k] != 0:
        frequency_count[i][k] += 1
      temp = [sum(x) for x in zip(temp, middle_point)]
      middle_points.append(temp)
    frequency_count[i][-1] = sum(frequency_count[i])
    all_middle_points.append(middle_points)
    points_data[index] = tuple(data[1:])

  points_array = np.array(points_data)
  
  point_coordinate = np.dot(points_array, feature).tolist()


  return point_coordinate, all_middle_points, frequency_count


def drawText(featurePoints, featureText):
  textActorList = []

  #print(len(featureText))
  #print(featurePoints)
  #print(len(featurePoints))
  for i in range(len(featurePoints)):
    atext = vtk.vtkVectorText()
    atext.SetText(featureText[i])
    textMapper = vtk.vtkPolyDataMapper()
    textMapper.SetInputConnection(atext.GetOutputPort())

    textActor = vtk.vtkFollower()
    textActor.SetMapper(textMapper)
    textActor.SetScale(0.05, 0.05, 0.05)
    textActor.AddPosition(featurePoints[i])
    textActorList.append(textActor)
  return textActorList

def drawtrajectory(num_of_person, points, frequency_count):
  linesPolyData = vtk.vtkPolyData()
  
  # Create three points
  origin = [0.0, 0.0, 0.0]

  # Create a vtkPoints container and store the points in it
  zeroPoint = list()
  pts = vtk.vtkPoints()
  pts.InsertNextPoint(origin)
  tempid = 1
  
  for personIdx in range(len(points)):
    for pointIdx in range(len(points[personIdx])):
      x, y, z = points[personIdx][pointIdx]
      pts.InsertNextPoint([x, y, z])
      if x == 0 and y == 0 and z == 0:
        zeroPoint.append(tempid)
      
      tempid += 1
  
  linesPolyData.SetPoints(pts)
  lines = vtk.vtkCellArray()
  lines.Initialize()
  colors = vtk.vtkUnsignedCharArray()
  colors.SetNumberOfComponents(3)
  namedColors = vtk.vtkNamedColors()
  for personIdx in range(num_of_person):

    numPoint = len(points[personIdx])
    prevPointIndex = 0
    for pointIdx in range(numPoint):
      # Create the first line (between Origin and P0)
      curPointIndex = personIdx * numPoint + pointIdx + 1
      if curPointIndex in zeroPoint:
        continue
      line0 = vtk.vtkLine()
      line0.GetPointIds().SetId(0, prevPointIndex)  # the second 0 is the index of the Origin in linesPolyData's points
      line0.GetPointIds().SetId(1, curPointIndex)
      lines.InsertNextCell(line0)
      colorTuple = [int(frequency_count[personIdx][-1]*255/(10)), int(255 - frequency_count[personIdx][-1]*255/(10)), 0]

      try:
          colors.InsertNextTupleValue(colorTuple)
      except AttributeError:
          # For compatibility with new VTK generic data arrays.
          colors.InsertNextTypedTuple(colorTuple)
      
      # Update current point index
      prevPointIndex = curPointIndex
  # Add the lines to the polydata container
  linesPolyData.SetLines(lines)
  linesPolyData.GetCellData().SetScalars(colors)
  print(len(zeroPoint) , 15* len(points) - len(zeroPoint) , lines.GetSize ())
  # Setup the visualization pipeline
  mapper = vtk.vtkPolyDataMapper()
  mapper.SetInputData(linesPolyData)
  actor = vtk.vtkActor()
  actor.SetMapper(mapper)
  actor.GetProperty().SetLineWidth(2)

  return actor, linesPolyData
    
    



if __name__ == '__main__':
  EHRDataPath = sys.argv[1]

  reader = vtk.vtkDelimitedTextReader()
  reader.SetFileName(EHRDataPath)
  reader.DetectNumericColumnsOn()
  reader.SetFieldDelimiterCharacters(',')
  reader.Update()

  rootTable = reader.GetOutput()
  feature = featureVector(EHRDataPath)
  point_xyz, middle_points, frequency_count = pointCalculate(rootTable, feature)
  #print(frequency_count)
  renderer = vtk.vtkRenderer()
  renderWindow = vtk.vtkRenderWindow()
  renderWindow.AddRenderer(renderer)
  renderer.SetBackground(.1, .2, .3)
  
  renderWindowInteractor = vtk.vtkRenderWindowInteractor()
  renderWindowInteractor.SetRenderWindow(renderWindow)

  feature_text = "PTSD	Speech	Anxiety	Depression	Headache	Sleep	Audiology	Vision	Neurologic	\
    Alzheimer	Cognitive	PCS	Endocrine	Skull_inj	NON_skull_inj"
  featureText = feature_text.split("	")
  featureText = [i.strip(" ") for i in featureText]

  sliderRep1, sliderWidget1 = slider(renderer, max_record, 40, 540, renderWindowInteractor, "record")
  sliderRep2, sliderWidget2 = slider(renderer, max_person, 40, 340, renderWindowInteractor, "person")
  sliderRep3, sliderWidget3 = slider(renderer, 0.1, 40, 140, renderWindowInteractor, "point size")
  
  balloonRep = vtk.vtkBalloonRepresentation()
  balloonRep.SetBalloonLayoutToImageRight()
  balloonRep.GetTextProperty().SetFontSize(15)
  balloonWidget = vtk.vtkBalloonWidget()
  balloonWidget.SetInteractor(renderWindowInteractor)
  balloonWidget.SetRepresentation(balloonRep)

  personlist = []
  person_middle_list = []
  for i in range(max_person):
    personlist.append(PointSet(i, feature, frequency_count, 0.05) )
    person_middle_list.append(PointSet(-i-2, [0 for _ in range(max_point_per_person - 1)], frequency_count, 0.05))

  linesActor = getCoordinatesActor(feature)
  trajactoryActor, linesPolyData = drawtrajectory(41, middle_points, frequency_count)
  tActor = [trajactoryActor, linesPolyData]
  mapper = vtk.vtkPolyDataMapper()
  mapper.SetInputData(tActor[1])
  mapper.Update()
  tActor[0] = vtk.vtkActor()
  tActor[0].SetMapper(mapper)
  tActor[0].GetProperty().SetLineWidth(2)
  tActor[0].Modified()
  
  
  faeturePoint = PointSet(-1, feature, frequency_count, 0.03)
  featureActor = vtk.vtkActor()
  featureActor.SetMapper(faeturePoint.mapper)
  featureActor.GetProperty().SetColor(0 ,0 ,0)
  featureActor.Modified()
  
  BigSphereFeature =[[0,0,0]]
  BigSphere = PointSet(-1, BigSphereFeature, frequency_count, 1)
  BigSphereActor = vtk.vtkActor()
  BigSphereActor.SetMapper(BigSphere.mapper)
  BigSphereActor.GetProperty().SetColor(1 ,1 ,1)
  BigSphereActor.GetProperty().SetEdgeColor(1,1,1)
  BigSphereActor.GetProperty().EdgeVisibilityOn()
  BigSphereActor.GetProperty().SetOpacity(0.05)
  BigSphereActor.Modified()
  

  actorList = []
  for i in range(max_person):
    actor = vtk.vtkActor()
    actor.SetMapper(personlist[i].mapper)
    actor.GetProperty().SetEdgeColor(frequency_count[i][-1]/(10),1 - frequency_count[i][-1]/(10),0)
    actor.GetProperty().EdgeVisibilityOn()
    actor.GetProperty().SetColor(1,1,1)
    actor.Modified()
    actorList.append(actor)
    ballonText = 'Patient{}'.format(i)
    for k in range(len(frequency_count[i]) -1 ):
      if frequency_count[i][k] != 0:
        ballonText += "\nFrequency {} ".format(featureText[k])
    balloonWidget.AddBalloon(actor, ballonText)

  middlePointsActorList = []
  for i in range(max_person):
    actor = vtk.vtkActor()
    actor.SetMapper(person_middle_list[i].mapper)
    actor.GetProperty().SetColor(0,1,0)
    actor.Modified()
    middlePointsActorList.append(actor)
  if len(sys.argv) == 3 and sys.argv[2] == 'track':
    renderer.AddActor(tActor[0])
  callback = pointCallBack(sliderRep1, 
                           sliderRep2, 
                           sliderRep3, 
                           personlist,  
                           person_middle_list,
                           point_xyz, 
                           middle_points,
                           actorList,
                           middlePointsActorList,
                           tActor)
  sliderWidget1.AddObserver("InteractionEvent", callback)
  sliderWidget2.AddObserver("InteractionEvent", callback)
  sliderWidget3.AddObserver("InteractionEvent", callback)
  
  axes = vtk.vtkAxesActor()

  textActorList = drawText(feature, featureText)
  for i in range(len(feature)):
    renderer.AddActor(textActorList[i])
    textActorList[i].SetCamera( renderer.GetActiveCamera() )

  renderer.AddActor(BigSphereActor)
  renderer.AddActor(featureActor)
  #renderer.AddActor(axes)
  for i in range(max_person):
    renderer.AddActor(actorList[i])
    renderer.AddActor(middlePointsActorList[i])
  
  renderer.AddActor(linesActor)

  renderer.ResetCamera()
  renderWindow.Render()
  renderWindow.SetSize(2000, 1500)
  balloonWidget.EnabledOn()
  renderWindowInteractor.Start()
