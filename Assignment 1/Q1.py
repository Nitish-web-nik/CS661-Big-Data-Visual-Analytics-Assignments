# Imorting VTK Library
import vtk
from vtk import *


# Function to calculate the intersection point between two vertices in 3D space based on their associated scalar values and an isocontour value.
def Compute(p1, val1, p2, val2, C_value):
    x=(((val1-C_value)/(val1-val2))*(p2[0]-p1[0]))+p1[0]
    y=(((val1-C_value)/(val1-val2))*(p2[1]-p1[1]))+p1[1]
    z=(((val1-C_value)/(val1-val2))*(p2[2]-p1[2]))+p1[2]

    
    # Return the results
    return x,y,z

# Create a reader for .vti file
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("Data/Isabel_2D.vti")  # Replace "your_file.vti" with the path to your .vti file
reader.Update()

# Get the output data
image_data = reader.GetOutput()
print("Number of Cells",image_data.GetNumberOfCells()) #Printing the number of cells in image data


dims = image_data.GetDimensions()
print("Dimensions:", dims) #Printing the Dimension of the image data 


scalar_range = image_data.GetScalarRange()
print("Scalar Range:", scalar_range) #Printing the Scalar Range of min and max values 

C_value = float(input("Please Enter the C value: ")) # Taking the input of isovalue

### Create a polydata ######################

# Create a new instance of vtkPolyData to hold the extracted contour
pdata = vtkPolyData()

# Create a vtkPoints object to store the points of the contour
points = vtkPoints()

# Create a vtkFloatArray to store the scalar values (pressures) associated with the contour points
dataArray = vtkFloatArray()
dataArray.SetName('Pressure')

# Loop through each cell in the input grid
for i in range(image_data.GetNumberOfCells()):
    
    #Get the current cell
    cell=image_data.GetCell(i)
    
    # Get the point IDs of the vertices of the current cell counter clockwise
    pid1 = cell.GetPointId(0)
    pid2 = cell.GetPointId(1)
    pid3 = cell.GetPointId(3)
    pid4 = cell.GetPointId(2)
    
    # Get the scalar values (pressures) associated with the vertices of the current cell

    dataArr = image_data.GetPointData().GetArray('Pressure')
    val1 = dataArr.GetTuple1(pid1)
    val2 = dataArr.GetTuple1(pid2)
    val3 = dataArr.GetTuple1(pid3)
    val4 = dataArr.GetTuple1(pid4)
    # print()
    
    # Check conditions to determine if the current cell intersects the isocontour
    if(val1>C_value and val2>C_value and val3>C_value and val4>C_value):
        continue  # Skip the cell if all vertices have pressures above the isocontour value
    elif(val1<C_value and val2<C_value and val3<C_value and val4<C_value):
        continue  # Skip the cell if all vertices have pressures below the isocontour value
    else:
        # Compute intersection points and add them to the points list

        if(val1>C_value and val2<C_value and val3<C_value and val4<C_value):
            x1,y1,z1=Compute(image_data.GetPoint(pid1),val1,image_data.GetPoint(pid2),val2,C_value)
            x2,y2,z2=Compute(image_data.GetPoint(pid1),val1,image_data.GetPoint(pid4),val4,C_value)

        elif(val1<C_value and val2>C_value and val3<C_value and val4<C_value):
            x1,y1,z1=Compute(image_data.GetPoint(pid2),val2,image_data.GetPoint(pid1),val1,C_value)
            x2,y2,z2=Compute(image_data.GetPoint(pid2),val2,image_data.GetPoint(pid3),val3,C_value)
            
        elif(val1>C_value and val2>C_value and val3<C_value and val4<C_value):
            x1,y1,z1=Compute(image_data.GetPoint(pid1),val1,image_data.GetPoint(pid4),val4,C_value)
            x2,y2,z2=Compute(image_data.GetPoint(pid2),val2,image_data.GetPoint(pid3),val3,C_value)
           
        elif(val1<C_value and val2<C_value and val3>C_value and val4<C_value):
            x1,y1,z1=Compute(image_data.GetPoint(pid3),val3,image_data.GetPoint(pid2),val2,C_value)
            x2,y2,z2=Compute(image_data.GetPoint(pid3),val3,image_data.GetPoint(pid4),val4,C_value)
           
        elif(val1<C_value and val2>C_value and val3>C_value and val4<C_value):
            x1,y1,z1=Compute(image_data.GetPoint(pid2),val2,image_data.GetPoint(pid1),val1,C_value)
            x2,y2,z2=Compute(image_data.GetPoint(pid3),val3,image_data.GetPoint(pid4),val4,C_value)
        elif(val1>C_value and val2>C_value and val3>C_value and val4<C_value):
            x1,y1,z1=Compute(image_data.GetPoint(pid1),val1,image_data.GetPoint(pid4),val4,C_value)
            x2,y2,z2=Compute(image_data.GetPoint(pid3),val3,image_data.GetPoint(pid4),val4,C_value)
        elif(val1<C_value and val2<C_value and val3<C_value and val4>C_value):
            x1,y1,z1=Compute(image_data.GetPoint(pid4),val4,image_data.GetPoint(pid1),val1,C_value)
            x2,y2,z2=Compute(image_data.GetPoint(pid4),val4,image_data.GetPoint(pid3),val3,C_value)
                 
        elif(val1>C_value and val2<C_value and val3<C_value and val4>C_value):
            x1,y1,z1=Compute(image_data.GetPoint(pid1),val1,image_data.GetPoint(pid2),val2,C_value)
            x2,y2,z2=Compute(image_data.GetPoint(pid4),val4,image_data.GetPoint(pid3),val3,C_value)
        elif(val1>C_value and val2>C_value and val3<C_value and val4>C_value):
            x1,y1,z1=Compute(image_data.GetPoint(pid2),val2,image_data.GetPoint(pid3),val3,C_value)
            x2,y2,z2=Compute(image_data.GetPoint(pid4),val4,image_data.GetPoint(pid3),val3,C_value)
        elif(val1<C_value and val2<C_value and val3>C_value and val4>C_value):
            x1,y1,z1=Compute(image_data.GetPoint(pid3),val3,image_data.GetPoint(pid2),val2,C_value)
            x2,y2,z2=Compute(image_data.GetPoint(pid4),val4,image_data.GetPoint(pid1),val1,C_value)
        elif(val1>C_value and val2<C_value and val3>C_value and val4>C_value):
            x1,y1,z1=Compute(image_data.GetPoint(pid1),val1,image_data.GetPoint(pid2),val2,C_value)
            x2,y2,z2=Compute(image_data.GetPoint(pid3),val3,image_data.GetPoint(pid2),val2,C_value)
        elif(val1<C_value and val2>C_value and val3>C_value and val4>C_value):
            x1,y1,z1=Compute(image_data.GetPoint(pid2),val2,image_data.GetPoint(pid1),val1,C_value)
            x2,y2,z2=Compute(image_data.GetPoint(pid4),val4,image_data.GetPoint(pid1),val1,C_value)
        # Amibiguity Condition But we go counter clockwise
        elif(val1<C_value and val2>C_value and val3<C_value and val4>C_value):
            x1,y1,z1=Compute(image_data.GetPoint(pid2),val2,image_data.GetPoint(pid1),val1,C_value)
            x2,y2,z2=Compute(image_data.GetPoint(pid2),val2,image_data.GetPoint(pid3),val3,C_value)
        elif(val1>C_value and val2<C_value and val3>C_value and val4<C_value):
            x1,y1,z1=Compute(image_data.GetPoint(pid1),val1,image_data.GetPoint(pid2),val2,C_value)
            x2,y2,z2=Compute(image_data.GetPoint(pid3),val3,image_data.GetPoint(pid2),val2,C_value)
        
        
        # Insert computed points into the points list
        points.InsertNextPoint(x1,y1,z1)
        points.InsertNextPoint(x2,y2,z2)

        
        # Insert isocontour value into the data array for both points
        dataArray.InsertNextTuple1(C_value)
        dataArray.InsertNextTuple1(C_value)
        

# Create a vtkPolyLine to represent the contour line segments
poly_line = vtkPolyLine()

# Get the number of points in the vtkPoints object
num_of_points = points.GetNumberOfPoints()

## insert the points....
cells = vtkCellArray()

# Loop through the points in pairs to create line segments
for i in range(0,num_of_points,2):

    # Set the number of points for the polyLine to 2 (since it's a line segment)
    poly_line.GetPointIds().SetNumberOfIds(2)
    
    # Set the point IDs for the polyLine (start and end points)
    poly_line.GetPointIds().SetId(0,i)
    poly_line.GetPointIds().SetId(1,i+1)
    
    # insert the polyLine....
    cells.InsertNextCell(poly_line)
    
# Set the points and lines of the vtkPolyData object
pdata.SetPoints(points)
pdata.SetLines(cells)

# Add the scalar data array (pressures) to the point data of the vtkPolyData
pdata.GetPointData().AddArray(dataArray)

writer = vtkXMLPolyDataWriter()
writer.SetInputData(pdata)

# Set the filename for the output VTP file
writer.SetFileName('vtkpolydata1.vtp') 
writer.Write()
#After running the code, we will get a file with name vtkpolydata1.vtp which can be viewed on ParaView.


