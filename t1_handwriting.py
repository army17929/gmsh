"""
The python API is entierly defined in the gms.py module, which contains the full 
documentation of all the functions in the API
"""
import gmsh
import sys

# Before using any functions in the API, gmsh must be initialized.
gmsh.initialize()

# Next we add a new model named "t1" 
# If gmsh.model.add() is not called, a new unnamed model will be created on the fly,
# If necessary. 
gmsh.model.add("t1")

# The python api provides direct access to each supported geometry(CAD) kernel.
# The built in CAD kernel, the python API function is 
# gmsh.model.geo.addPoint():
# The first 3 args are the point coordinates.
# the next argument is the target mesh size close to the point 
# the last argument is the point tag (a strictly positive integer that 
# uniquely identifies the point)
lc=1e-4 # Mesh size
gmsh.model.geo.addPoint(0,0,0,lc,1)

"""
The distribution of the mesh element sizes will be obtained by interpolation of
these mesh sizes throughout the geometry. Another method to specify mesh sizes 
is to use general mesh size Fields. 

If no target mesh size is provided, a default uniform coarse size will be used
for the model, based on the overall model size.
"""
gmsh.model.geo.addPoint(.1,0,0,lc,2)
gmsh.model.geo.addPoint(.1,.3,0,lc,3) # Note that the point index is increasing.
p4=gmsh.model.geo.addPoint(0,.5,0,lc)

"""
Curves are gmsh's second type of elementary entitiees, and amongst curves, straight
lines are the simplest. The API to create straight line segments with the built in
kernel follows the same conventions.
"""
gmsh.model.geo.addLine(1,2,1)
gmsh.model.geo.addLine(2,3,2)
gmsh.model.geo.addLine(3,p4,3)
gmsh.model.geo.addLine(p4,1,4)

"""
The third elementary entity is the surface. In order to define a simple rectangular
surface from the four curves defined above, a curve loop has first to be defined.
"""
gmsh.model.geo.addCurveLoop([1, 2, 3,4],1)
gmsh.model.geo.addPlaneSurface([1],1)
gmsh.model.geo.synchronize()

"""
An optionanl step is needed if we want to group elementary geometrical entities
into more meaningful groups, to define some mathematical functional or material 
properties. 
"""
gmsh.model.addPhysicalGroup(1,[1,2,4],5)
gmsh.model.addPhysicalGroup(2,[1],name="My surface")

# Generate 2D mesh
gmsh.model.mesh.generate(2)

# save it to disk 
gmsh.write("t1_handwriting.msh")

"""
To visualize the model we can run the graphical user interface with 
``gmsh.fltk.run()`` Here we run it only if nopopup is not provided in the 
command line.
"""
if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()