import vtk
from paraview.simple import *

ct = FindSource("CT-2019.stl") 
mri = FindSource("Aorta MRI.stl")

ctData = servermanager.Fetch(ct)
mriData = servermanager.Fetch(mri)

icp = vtk.vtkIterativeClosestPointTransform()
icp.SetSource(ctData)
icp.SetTarget(mriData)
icp.GetLandmarkTransform().SetModeToRigidBody()
icp.SetMaximumNumberOfIterations(50)
icp.StartByMatchingCentroidsOn()
icp.Update()

transformFilter = vtk.vtkTransformPolyDataFilter()
transformFilter.SetInputData(ctData)
transformFilter.SetTransform(icp)
transformFilter.Update()

alignedCT = TrivialProducer()
alignedCT.GetClientSideObject().SetOutput(transformFilter.GetOutput())
alignedCT.UpdatePipeline()
