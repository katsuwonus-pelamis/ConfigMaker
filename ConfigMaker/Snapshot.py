from .Particles import * 
import numpy as np

class Snapshot:
  def __init__(self, NPart, box, particles):
    self.NPart = NPart
    self.box = box
    self.particles = particles

  def read(f, particle_type):
    npart_line = f.readline()
    if not npart_line.strip():
        return None
    npart = int(npart_line.strip())
    box = [float(x) for x in f.readline().strip().split()]
    if particle_type == 'spherocylinder':
        particles = [Spherocylinder.read(f.readline()) for _ in range(npart)]
    elif particle_type == 'sphere':
        particles = [Sphere.read(f.readline()) for _ in range(npart)]
    else:
        raise ValueError("Unknown particle type")
    return Snapshot(npart, box, particles)
  
  def write(self, filename):
    with open(filename, 'a') as f:
        box_str = " ".join(str(x) for x in self.box)
        f.write(f"{self.NPart}\n")
        f.write(f"{box_str}\n")
    for part in self.particles:
      part.write(filename)
  
  def stretch_config(self, factor, axis): 
    if axis < 0 or axis > 2:
      print("Invalid axis count")
    
    self.box[axis] *= factor
    for part in self.particles:
      part.pos[axis] *= factor
      
  def scale_config(self, factor):
    for i, _ in enumerate(self.box):
      self.stretch_config(factor, i)
  
  
  # Missing a labeling of the particles, I will work on it when samples are purer
  def csv_to_rod(panda_csv):
    particles = []
    for _, row in panda_csv.iterrows():
      particles.append(Spherocylinder.csv_to_rod(row))
    box = np.array((np.max(panda_csv["POSITION_X"]), np.max(panda_csv["POSITION_Y"]), 1))
    return Snapshot(len(particles), box, particles)
  
  def get_boxvol(self):
    return self.box[0]*self.box[1]*self.box[2]
  
  def get_ndensity(self):
    return self.NPart/self.get_boxvol()
  
  def get_packfrac(self):
    occ_vol = 0
    for part in self.particles:
      occ_vol+= part.get_volume()
    return occ_vol/self.get_boxvol()
  
  def tile(cell, nx, ny, nz):
    a1, a2, a3 = cell.lattice_vectors
    new_particles = []
    for ix in range(nx):
      for iy in range(ny):
        for iz in range(nz):
          shift = ix * a1 + iy * a2 + iz * a3
          for part in cell.particles:
            new_pos = [part.pos[j] + shift[j] for j in range(3)]
            new_particles.append(Spherocylinder(new_pos, list(part.ori), part.diameter, part.specie))
    box = nx * a1 + ny * a2 + nz * a3
    return Snapshot(len(new_particles), box.tolist(), new_particles)
  
  def sph_to_rod(sph_snapshot, length, ori_axis = 2):
    rods = []
    rmax = 0
    for sph in sph_snapshot.particles:
      rods.append(Spherocylinder.from_sphere(sph, length, ori_axis=2))
      if sph.radius > rmax:
        rmax = sph.radius
    box = sph_snapshot.box
    box[ori_axis] = length+rmax*2 
    return Snapshot(sph_snapshot.NPart,box, rods)
  
  # now giving every single layer, will implement a version that does the same over and over
  
  def pile(layers, layer_height, layering_axis = 2):
    nlayers = len(layers)
    heights = np.arange(0,  nlayers * layer_height, layer_height)
    box = np.zeros(3)
    particles = []
    for i, layer in enumerate(layers):
      for j, x in enumerate(layer.box):
        if box[j]< x:
          box[j] = x
          
      for _, part in enumerate(layer.particles):
        particles.append(part)
        particles[-1].pos[layering_axis] = heights[i]
        
    box[layering_axis] = heights[-1] + layers[-1].box[layering_axis]
    NPart = len(particles)
    return Snapshot(NPart, box, particles)
    
  ## Never tested, it most likely needs a function "rotate lattice" to be an effective """crystallographic""" tool  
 #   def apply_pbc(self):
 ##     for i, part in enumerate(self.particles):
  #      part.pos = np.mod(part.pos, self.box)
      
  ## esoteric pythonic syntax    
        
  def erase_externals(self):
    self.particles = [
      p for p in self.particles 
      if all(0 <= p.pos[i] < self.box[i] for i in range(3))
    ]
    self.NPart = len(self.particles)
    