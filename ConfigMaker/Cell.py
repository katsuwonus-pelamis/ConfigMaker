import numpy as np
from .Particles import *

class Cell:
  def __init__(self, lattice_vectors, particles):
    self.lattice_vectors = np.array(lattice_vectors)
    self.particles = particles
    self.npart = len(particles)
  
  def cubic_cell(a, l, diam=1):
    ori = [0,0,l]
    cubic_cell = Cell(
    lattice_vectors = [[a, 0, 0],                        
                        [0, a, 0],                
                        [0,0, l+a]],
    particles=[Spherocylinder([0, 0, 0],ori, diam, 'a')]
    )
    return cubic_cell
  
  def hex_cell(a, l, diam=1): #This is clearly not a minimal cell, but it's what we need to tile with orthogonal vectors and with the rods aligned in the (0 0 1) direction
    ori = [0,0,l]
    h_step = l + np.sqrt(2/3) * a

    hex_cell = Cell(
      lattice_vectors = [[2 * a, 0, 0],                        
                        [0, np.sqrt(3) * a, 0],                
                        [0, 0, 3*h_step]],
      particles=[
                  Spherocylinder([0, 0, 0], ori, diam, 'a'),
                  Spherocylinder([a, 0, 0], ori, diam, 'a'),
                  Spherocylinder([0.5*a, np.sqrt(3)/2*a, 0], ori, diam, 'a'),
                  Spherocylinder([1.5*a, np.sqrt(3)/2*a, 0],ori,  diam, 'a'),
                  Spherocylinder([0.5, np.sqrt(3)/6, h_step],ori, diam,'a'),
                  Spherocylinder([0, 2*np.sqrt(3)/3, h_step],ori, diam,'a'),
                  Spherocylinder([1.5, np.sqrt(3)/6, h_step],ori, diam,'a'),
                  Spherocylinder([1, 2*np.sqrt(3)/3, h_step],ori, diam,'a'),
                  Spherocylinder([0,         (np.sqrt(3)/3)*a,               2*h_step], ori, diam, 'a'),
                  Spherocylinder([1*a,       (np.sqrt(3)/3)*a,               2*h_step], ori, diam, 'a'),
                  Spherocylinder([0.5*a,     (np.sqrt(3)/2 + np.sqrt(3)/3)*a,2*h_step], ori, diam, 'a'),
                  Spherocylinder([1.5*a,     (np.sqrt(3)/2 + np.sqrt(3)/3)*a,2*h_step], ori, diam, 'a')]
      )
    return hex_cell
    
    