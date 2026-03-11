import numpy as np
from .Spherocylinder import *

class Cell:
  def __init__(self, lattice_vectors, particles):
    self.lattice_vectors = np.array(lattice_vectors)
    self.particles = particles
    self.npart = len(particles)
    
  def fcc_cell(a, l): #This is clearly not a minimal cell, but it's what we need to tile with orthogonal vectors and with the rods aligned in the (0 0 1) direction
    ori = [0,0,l]
    h_step = l + np.sqrt(2/3) * a

    fcc_cell = Cell(
      lattice_vectors = [[2 * a, 0, 0],                        
                        [0, np.sqrt(3) * a, 0],                
                        [0, 0, 3*h_step]],
      particles=[
                  Spherocylinder([0, 0, 0], ori, 1, 'a'),
                  Spherocylinder([a, 0, 0], ori,1, 'a'),
                  Spherocylinder([0.5*a, np.sqrt(3)/2*a, 0], ori,a, 'a'),
                  Spherocylinder([1.5*a, np.sqrt(3)/2*a, 0], ori, a, 'a'),
                  Spherocylinder([0.5, np.sqrt(3)/6, h_step], ori, a ,'a'),
                  Spherocylinder([0, 2*np.sqrt(3)/3, h_step], ori, a ,'a'),
                  Spherocylinder([1.5, np.sqrt(3)/6, h_step], ori, a ,'a'),
                  Spherocylinder([1, 2*np.sqrt(3)/3, h_step], ori, a ,'a'),
                  Spherocylinder([0,         (np.sqrt(3)/3)*a,               2*h_step], ori, 1, 'a'),
                  Spherocylinder([1*a,       (np.sqrt(3)/3)*a,               2*h_step], ori, 1, 'a'),
                  Spherocylinder([0.5*a,     (np.sqrt(3)/2 + np.sqrt(3)/3)*a,2*h_step], ori, 1, 'a'),
                  Spherocylinder([1.5*a,     (np.sqrt(3)/2 + np.sqrt(3)/3)*a,2*h_step], ori, 1, 'a')]
      )
    return fcc_cell
    
    