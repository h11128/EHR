import vtk
import sys

# def getPointsActor(table):
  

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
  
  sphereSource = vtk.vtkSphereSource()
  # sphereSource.SetCenter(0.0, 0.0, 0.0)
  sphereSource.SetRadius(0.1)


  points = vtk.vtkPoints()

  for i in range(3):
    for j in range(3):
      points.InsertNextPoint(i,j,i*j/2)

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

  renderWindowInteractor = vtk.vtkRenderWindowInteractor()
  renderWindowInteractor.SetRenderWindow(renderWindow)

  axes = vtk.vtkAxesActor()


  renderer.AddActor(axes)
  renderer.AddActor(gActor)
  renderer.ResetCamera()
  renderWindow.Render()
  renderWindow.SetSize(1000, 1000)
  renderWindowInteractor.Start()
