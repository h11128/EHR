import vtk
import sys

class pointCallBack(object):
  def __init__(self, sliderRep, sliderRep2, points, max_record, max_person):
    self.sliderRep = sliderRep
    self.sliderRep2 = sliderRep2
    self.points = points
    self.max_record = max_record
    self.max_person = max_person

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
    points.Modified()
    gActor.GetProperty().SetColor(1,0,0)
    print("person: %d record: %d"% (person, record))
    print(points.GetNumberOfPoints())


# def getPointsActor(table):

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
  
  max_record = 40
  max_person = 10
  sliderRep1, sliderWidget1 = slider(renderer, max_record, 40, 40, renderWindowInteractor, "record")
  sliderRep2, sliderWidget2 = slider(renderer, max_person, 40, 80, renderWindowInteractor, "person")



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
  gActor = vtk.vtkActor()
  gActor.SetMapper(mapper)

  callback = pointCallBack(sliderRep1, sliderRep2, points,  max_record, max_person)
  sliderWidget1.AddObserver("InteractionEvent", callback)
  #callback2 = pointCallBack(sliderRep1, sliderRep2, points)
  sliderWidget2.AddObserver("InteractionEvent", callback)
  
  axes = vtk.vtkAxesActor()


  renderer.AddActor(axes)
  renderer.AddActor(gActor)
  renderer.ResetCamera()
  renderWindow.Render()
  renderWindow.SetSize(1000, 600)
  renderWindowInteractor.Start()
