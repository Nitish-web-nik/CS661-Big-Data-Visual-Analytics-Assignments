# Imorting VTK Library
import vtk

# Create a reader for .vti file
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("Data/Isabel_3D.vti")  # Replace "your_file.vti" with the path to your .vti file
reader.Update()
# Get the output data


# Create a volume mapper
volume_mapper = vtk.vtkSmartVolumeMapper()
volume_mapper.SetInputConnection(reader.GetOutputPort())

# Create a volume property
volume_property = vtk.vtkVolumeProperty()
# Create a color transfer function
color_transfer_function = vtk.vtkColorTransferFunction()

# Set up the color transfer function with values
color_transfer_function.AddRGBPoint(-4931.54 , 0.0, 1.0, 1.0)  # Value, RGB color
color_transfer_function.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)
color_transfer_function.AddRGBPoint(-1873.9 , 0.0, 0.0, 0.5)
color_transfer_function.AddRGBPoint(-1027.16  , 1.0, 0.0, 0.0)  # Value, RGB color
color_transfer_function.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)
color_transfer_function.AddRGBPoint(2594.97 , 1.0, 1.0, 0.0)

# Create a piecewise function (opacity transfer function)
opacity_transfer_function = vtk.vtkPiecewiseFunction()

# Set up the opacity transfer function with values
opacity_transfer_function.AddPoint(-4931.54, 1.0)  # Value, Opacity
opacity_transfer_function.AddPoint(101.815, 0.002)
opacity_transfer_function.AddPoint(2594.97, 0.0)

# Set color and opacity transfer functions
volume_property.SetColor(color_transfer_function)
volume_property.SetScalarOpacity(opacity_transfer_function)

# Ask the user if they want Phong shading
phong_shading_choice = input("Do you want Phong shading? (yes/no): ")

# Enable Phong shading if user chooses 'yes'
if phong_shading_choice.lower() == 'yes':
    volume_property.ShadeOn()
    volume_property.SetAmbient(0.5)  # Set ambient coefficient
    volume_property.SetDiffuse(0.5)  # Set diffuse coefficient
    volume_property.SetSpecular(0.5)  # Set specular coefficient
    volume_property.SetSpecularPower(10)  # Set specular power
else:
    volume_property.ShadeOff()

# Create a volume
volume = vtk.vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Create an outline filter
outline_filter = vtk.vtkOutlineFilter()
outline_filter.SetInputConnection(reader.GetOutputPort())
# Create a mapper for the outline
outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

# Create an actor for the outline
outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0.0, 0.0, 0.0)  # Outline color (white)

# Create a renderer
renderer = vtk.vtkRenderer()
renderer.SetBackground(255, 237, 217)
#255, 237, 217
renderer.AddVolume(volume)
renderer.AddActor(outline_actor)  # Add outline actor to the renderer

# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(1000, 1000)

# Create an interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Start the rendering loop
interactor.Initialize()
interactor.Start()