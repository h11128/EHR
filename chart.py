import vtk
import sys

max_record = 40
max_person = 10

class pointCallBack(object):
  def __init__(self, sliderRep, sliderRep2, points, max_record, max_person, actor):
    self.sliderRep = sliderRep
    self.sliderRep2 = sliderRep2
    self.points = points
    self.max_record = max_record
    self.max_person = max_person
    self.pointsActor = actor

    super().__init__()

  def __call__(self, caller, event):
    print("the value is " + str(self.sliderRep.GetValue()))
    person = int(self.sliderRep2.GetValue())
    record = int(self.sliderRep.GetValue())

    for i in range(max_person):
      for j in range(max_record):
        index = (i) * max_record + j
        if (i>person or j >record):
          points.SetPoint(index, 0,0,0)
        else:
          points.SetPoint(index, 0.01*i,0.01*i,0.01*j)
    pointsActor.GetProperty().SetColor(1,0,0)
    pointsActor.Modified()
    print("person: %d record: %d"% (person, record))
    print(points.GetNumberOfPoints())

def slider(renderer, maximum, x, y, renderWindowInteractor, title):
  sliderRep = vtk.vtkSliderRepresentation2D()
  sliderRep.SetRenderer(renderer)
  sliderRep.SetMinimumValue(0)
  sliderRep.SetMaximumValue(maximum)
  sliderRep.SetValue(0)
  sliderRep.SetTitleText(title)

  sliderRep.GetPoint1Coordinate().SetCoordinateSystemToDisplay()
  sliderRep.GetPoint1Coordinate().SetValue(x, y)
  sliderRep.GetPoint2Coordinate().SetCoordinateSystemToDisplay()
  sliderRep.GetPoint2Coordinate().SetValue(x+200, y)
  sliderRep.BuildRepresentation()

  sliderWidget = vtk.vtkSliderWidget()
  sliderWidget.SetInteractor(renderWindowInteractor)
  sliderWidget.SetRepresentation(sliderRep)
  sliderWidget.SetAnimationModeToAnimate()
  sliderWidget.EnabledOn()
  return sliderRep, sliderWidget



def getPointsActor():
  sphereSource = vtk.vtkSphereSource()
  # sphereSource.SetCenter(0.0, 0.0, 0.0)
  sphereSource.SetRadius(0.01)

  points = vtk.vtkPoints()
  points.SetNumberOfPoints(max_record*max_person)

  g = vtk.vtkPolyData()
  g.SetPoints(points)

  glyph3D = vtk.vtkGlyph3D()
  glyph3D.SetSourceConnection(sphereSource.GetOutputPort())
  glyph3D.SetInputData(g)
  glyph3D.Update()

  
  mapper = vtk.vtkPolyDataMapper()
  mapper.SetInputConnection(glyph3D.GetOutputPort())
  mapper.Update()
  actor = vtk.vtkActor()
  actor.SetMapper(mapper)

  return points, actor

def getLinesActor():
  linesPolyData = vtk.vtkPolyData()

  # Create three points
  origin = [0.0, 0.0, 0.0]
  p0 = [1.0, 1.0, 0.0]
  p1 = [0.0, 1.0, 1.0]

  # Create a vtkPoints container and store the points in it
  pts = vtk.vtkPoints()
  pts.InsertNextPoint(origin)
  pts.InsertNextPoint(p0)
  pts.InsertNextPoint(p1)

  # Add the points to the polydata container
  linesPolyData.SetPoints(pts)

  # Create the first line (between Origin and P0)
  line0 = vtk.vtkLine()
  line0.GetPointIds().SetId(0, 0)  # the second 0 is the index of the Origin in linesPolyData's points
  line0.GetPointIds().SetId(1, 1)  # the second 1 is the index of P0 in linesPolyData's points

  # Create the second line (between Origin and P1)
  line1 = vtk.vtkLine()
  line1.GetPointIds().SetId(0, 0)  # the second 0 is the index of the Origin in linesPolyData's points
  line1.GetPointIds().SetId(1, 2)  # 2 is the index of P1 in linesPolyData's points

  # Create a vtkCellArray container and store the lines in it
  lines = vtk.vtkCellArray()
  lines.InsertNextCell(line0)
  lines.InsertNextCell(line1)

  # Add the lines to the polydata container
  linesPolyData.SetLines(lines)

  namedColors = vtk.vtkNamedColors()

  # Create a vtkUnsignedCharArray container and store the colors in it
  colors = vtk.vtkUnsignedCharArray()
  colors.SetNumberOfComponents(3)
  try:
      colors.InsertNextTupleValue(namedColors.GetColor3ub("Tomato"))
      colors.InsertNextTupleValue(namedColors.GetColor3ub("Mint"))
  except AttributeError:
      # For compatibility with new VTK generic data arrays.
      colors.InsertNextTypedTuple(namedColors.GetColor3ub("Tomato"))
      colors.InsertNextTypedTuple(namedColors.GetColor3ub("Mint"))

  # Color the lines.
  # SetScalars() automatically associates the values in the data array passed as parameter
  # to the elements in the same indices of the cell data array on which it is called.
  # This means the first component (red) of the colors array
  # is matched with the first component of the cell array (line 0)
  # and the second component (green) of the colors array
  # is matched with the second component of the cell array (line 1)
  linesPolyData.GetCellData().SetScalars(colors)

  # Setup the visualization pipeline
  mapper = vtk.vtkPolyDataMapper()
  mapper.SetInputData(linesPolyData)

  actor = vtk.vtkActor()
  actor.SetMapper(mapper)
  actor.GetProperty().SetLineWidth(4)

  return actor
  

if __name__ == '__main__':
  EHRDataPath = sys.argv[1]

  reader = vtk.vtkDelimitedTextReader()
  reader.SetFileName(EHRDataPath)
  reader.DetectNumericColumnsOn()
  reader.SetFieldDelimiterCharacters(',')
  reader.Update()

  rootTable = reader.GetOutput()
  rowsCount = rootTable.GetNumberOfRows()
  colsCount = rootTable.GetNumberOfColumns()

  renderer = vtk.vtkRenderer()
  renderWindow = vtk.vtkRenderWindow()
  renderWindow.AddRenderer(renderer)
  renderer.SetBackground(.1, .2, .3)

  renderWindowInteractor = vtk.vtkRenderWindowInteractor()
  renderWindowInteractor.SetRenderWindow(renderWindow)

  
  sliderRep1, sliderWidget1 = slider(renderer, max_record, 40, 40, renderWindowInteractor, "record")
  sliderRep2, sliderWidget2 = slider(renderer, max_person, 40, 80, renderWindowInteractor, "person")
  
  points, pointsActor = getPointsActor()
  linesActor = getLinesActor()

  callback = pointCallBack(sliderRep1, sliderRep2, points,  max_record, max_person, pointsActor)
  sliderWidget1.AddObserver("InteractionEvent", callback)
  #callback2 = pointCallBack(sliderRep1, sliderRep2, points)
  sliderWidget2.AddObserver("InteractionEvent", callback)
  
  axes = vtk.vtkAxesActor()

  renderer.AddActor(axes)
  renderer.AddActor(pointsActor)
  renderer.AddActor(linesActor)
  renderer.ResetCamera()
  renderWindow.Render()
  renderWindow.SetSize(1000, 1000)
  renderWindowInteractor.Start()
