"""
Gmsh python tutorial 2
Transformaton, extruded geometries, volumes
"""

import gmsh
import sys
import math

# If sys.argv is passed to gmsh.initialize, Gmsh will parse the command line.
gmsh.initialize(sys.argv)

gmsh.model.add("t2")

# copied from the first tutorial..
lc = 1e-2
gmsh.model.geo.addPoint(0, 0, 0, lc, 1)
gmsh.model.geo.addPoint(.1, 0, 0, lc, 2)
gmsh.model.geo.addPoint(.1, .3, 0, lc, 3)
gmsh.model.geo.addPoint(0, .3, 0, lc, 4)
gmsh.model.geo.addLine(1, 2, 1)
gmsh.model.geo.addLine(3, 2, 2)
gmsh.model.geo.addLine(3, 4, 3)
gmsh.model.geo.addLine(4, 1, 4)
gmsh.model.geo.addCurveLoop([4, 1, -2, 3], 1)
gmsh.model.geo.addPlaneSurface([1], 1)
gmsh.model.geo.synchronize()
gmsh.model.addPhysicalGroup(1, [1, 2, 4], 5)
gmsh.model.addPhysicalGroup(2, [1], name="My surface")

# We can add new points and curves in the same way as we did in tutorial 1.
gmsh.model.geo.addPoint(0, .4,0, lc,5)
gmsh.model.geo.addLine(4,5,5)

# Gmsh also provides tools to transform
# elementary entities or copies of elementary entities. 
# Geometrical transformations take a vector of pairs of integers 
# as first argument, which contains the list of entities, 
# represented by pairs. For example, the point 5 can be moved by 0.02 to the left
# with the command below 
gmsh.model.geo.translate([(0,5)],-0.02,0,0)

# It can be further rotated by -Pi/4 around using the command below. 
gmsh.model.geo.rotate([(0,5)],0,.3,0,0,0,1,-math.pi/4)

# Note that there are no units in gmsh 
# coordinates are just numbers it is up to the user to associate a meaning to them
# Point 3 can be duplicated and translated by 0.05 along the y-axis by using the copy function
# which takes a vector of pairs as input and returns vector of (dim,tag) pairs.
ov=gmsh.model.geo.copy([(0,3)])
gmsh.model.geo.translate(ov,0,0.05,0)

# The new point tag is available on ov[0][1] and can be used to create new lines.
# this copy function will return vector of (dim,tag) pairs
#print(ov) >>> [(0,6)] Therefore, the index(tag) could be fetched by ov[0][1]
gmsh.model.geo.addLine(3,ov[0][1],7)
gmsh.model.geo.addLine(ov[0][1],5,8)
gmsh.model.geo.addCurveLoop([5,-8,-7,3],10)
gmsh.model.geo.addPlaneSurface([10],11)

# In the same way, we can translate copies of the two surfaces 1 and 11 to the
# right with the following command.
ov=gmsh.model.geo.copy([(2,1),(2,11)]) # Dimension=2
gmsh.model.geo.translate(ov,0.12,0,0)

print("New Surfaces"+str(ov[0][1])+"and"+str(ov[0][1]))

"""
volumes are the fourth type of elementary entities in mesh. In the same way one 
defines the curve loops to build surfaces, one has to define surface loops 
to build volumes. The following volume does not have holes and thus consists
of a single surface loop.
"""

gmsh.model.geo.addPoint(0.,.3,.12,lc,100)
gmsh.model.geo.addPoint(0.1,.3,.12,lc,101)
gmsh.model.geo.addPoint(0.1,.35,.12,lc,102)

"""
We would like to retrieve the coordinates of point 5 to create point 103, so
we synchronize the model, and use getValue.
"""
gmsh.model.geo.synchronize()
xyz=gmsh.model.getValue(0,5,[])
"""
gmsh.model.getValue(dim,tag,parametricCoord)
Evaluate the parametrization of the entity of dimension and tag.
"""
gmsh.model.geo.addPoint(xyz[0],xyz[1],0.12,lc,103)

gmsh.model.geo.addLine(4,100,110)
gmsh.model.geo.addLine(3,101,111)
gmsh.model.geo.addLine(6,102,112)
gmsh.model.geo.addLine(5,103,113)
gmsh.model.geo.addLine(103,100,114)
gmsh.model.geo.addLine(100,101,115)
gmsh.model.geo.addLine(101,102,116)
gmsh.model.geo.addLine(102,103,117)

gmsh.model.geo.addCurveLoop([115,-111,3,110],118)
# Loop should be closed
gmsh.model.geo.addPlaneSurface([118],119)
"""
Add a plane surface in the built in CAD, defined by one or more curve loops wireTags.
"""
gmsh.model.geo.addCurveLoop([111, 116, -112, -7], 120)
gmsh.model.geo.addPlaneSurface([120], 121)
gmsh.model.geo.addCurveLoop([112, 117, -113, -8], 122)
gmsh.model.geo.addPlaneSurface([122], 123)
gmsh.model.geo.addCurveLoop([114, -110, 5, 113], 124)
gmsh.model.geo.addPlaneSurface([124], 125)
gmsh.model.geo.addCurveLoop([115, 116, 117, 114], 126)
gmsh.model.geo.addPlaneSurface([126], 127)
gmsh.model.geo.addSurfaceLoop([127, 119, 121, 123, 125, 11], 128)
gmsh.model.geo.addVolume([128], 129)

"""
when a volume can be extruded from a surface, it is usually easier to use the
extrude() function directly instead of creating all the points, curves and 
surfaces by hand. For example,  the following command extrudes the surface 11
along the z axis and automatically creates a new volume. As expected, the function
takes a vector of (dim,tag) pairs as input as  well as the translation vector, and 
returns a vector of (dim,tag) pairs as output
"""
ov2 = gmsh.model.geo.extrude([ov[1]], 0, 0, 0.12)

"""
Mesh sizes associated dto geometrical points can be set by passing a vector of
dim,tag pairs for the corresponding points
"""
gmsh.model.geo.mesh.setSize([(0, 103), (0, 105), (0, 109), (0, 102), (0, 28),
                             (0, 24), (0, 6), (0, 5)], lc * 3)

gmsh.model.geo.synchronize()

# We group volumes 129 and 130 in a single physical group with tag `1' and name
# "The volume":
gmsh.model.addPhysicalGroup(3, [129, 130], 1, "The volume")

# We finally generate and save the mesh:
gmsh.model.mesh.generate(3)
gmsh.write("t2.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()