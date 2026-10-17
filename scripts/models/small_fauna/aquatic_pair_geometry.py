# SPDX-License-Identifier: MIT
"""Original deterministic low-poly aquatic fauna geometry helpers.

Geometry is authored from dimensions and primary-reference observations, never
from a downloaded mesh or scan. Configurations and exact reference ledgers ship
beside each generated asset. This module has no animation or rigging features.
"""
from math import sin, cos, pi
from mathutils import Vector
import bpy
from asset_common import mesh_object

class Shape:
    def __init__(self): self.vertices=[]; self.faces=[]; self.material_indices=[]
    def add(self, vertices, faces, material=0):
        offset=len(self.vertices); self.vertices.extend(tuple(v) for v in vertices)
        self.faces.extend(tuple(offset+i for i in f) for f in faces)
        self.material_indices.extend([material]*len(faces))
    def object(self,name,collection,materials):
        obj=mesh_object(name,self.vertices,self.faces,materials,collection)
        for face,index in zip(obj.data.polygons,self.material_indices): face.material_index=index
        return obj
    def tube(self, points, radii, sides=6, material=0, flatten=1.0):
        points=[Vector(p) for p in points]; vertices=[]
        for i,(point,radius) in enumerate(zip(points,radii)):
            tangent=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized()
            reference=Vector((0,0,1)) if abs(tangent.z)<.92 else Vector((1,0,0))
            u=tangent.cross(reference).normalized(); v=tangent.cross(u).normalized()
            for j in range(sides):
                a=2*pi*j/sides
                vertices.append(point+radius*(cos(a)*u+sin(a)*v*flatten))
        faces=[tuple(range(sides-1,-1,-1))]
        for i in range(len(points)-1):
            for j in range(sides):
                k=i*sides+j; n=i*sides+(j+1)%sides
                faces.append((k,n,n+sides,k+sides))
        faces.append(tuple((len(points)-1)*sides+j for j in range(sides)))
        self.add(vertices,faces,material)
    def ellipsoid(self,center,radii,segments=10,rings=5,material=0):
        # Pole fans avoid degenerate coincident pole vertices.
        center=Vector(center); vertices=[center+Vector((0,0,radii[2]))]
        for i in range(1,rings):
            phi=pi*i/rings
            for j in range(segments):
                theta=2*pi*j/segments
                vertices.append(center+Vector((radii[0]*sin(phi)*cos(theta),radii[1]*sin(phi)*sin(theta),radii[2]*cos(phi))))
        vertices.append(center+Vector((0,0,-radii[2])))
        bottom=len(vertices)-1
        faces=[(0,1+j,1+(j+1)%segments) for j in range(segments)]
        for i in range(rings-2):
            for j in range(segments):
                a=1+i*segments+j; b=1+i*segments+(j+1)%segments
                faces.append((a,a+segments,b+segments,b))
        faces.extend((bottom,1+(rings-2)*segments+(j+1)%segments,1+(rings-2)*segments+j) for j in range(segments))
        self.add(vertices,faces,material)
    def plate(self, outline, thickness, material=0, ridge=None):
        # Closed plate, optionally with a gently raised central crown.
        outline=[Vector(p) for p in outline]; n=len(outline)
        vertices=[p+Vector((0,0,thickness/2)) for p in outline]+[p-Vector((0,0,thickness/2)) for p in outline]
        if ridge is None:
            faces=[tuple(range(n)),tuple(range(2*n-1,n-1,-1))]
        else:
            vertices.append(Vector(ridge)); faces=[(i,(i+1)%n,2*n) for i in range(n)]+[tuple(range(2*n-1,n-1,-1))]
        faces.extend((i,n+i,n+(i+1)%n,(i+1)%n) for i in range(n))
        self.add(vertices,faces,material)
    def side_fin(self, outline_yz, half_thickness, material=0):
        # Closed fin volume in the Y/Z plane, zero duplicated boundary vertices.
        n=len(outline_yz)
        vertices=[(-half_thickness,y,z) for y,z in outline_yz]+[(half_thickness,y,z) for y,z in outline_yz]
        faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
        faces.extend((i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n))
        self.add(vertices,faces,material)

def loft_y(sections, angles=12, material_for_face=None):
    """Closed elliptical profile loft. Section=(y,cx,cz,rx,rz)."""
    shape=Shape(); vertices=[]; faces=[]; mi=[]
    for y,cx,cz,rx,rz in sections:
        vertices.extend((cx+rx*cos(2*pi*j/angles),y,cz+rz*sin(2*pi*j/angles)) for j in range(angles))
    faces.append(tuple(range(angles-1,-1,-1))); mi.append(0)
    for i in range(len(sections)-1):
        for j in range(angles):
            faces.append((i*angles+j,i*angles+(j+1)%angles,(i+1)*angles+(j+1)%angles,(i+1)*angles+j))
            mi.append(material_for_face(i,j) if material_for_face else 0)
    faces.append(tuple((len(sections)-1)*angles+j for j in range(angles))); mi.append(0)
    shape.add(vertices,faces); shape.material_indices=mi
    return shape
