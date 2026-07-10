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
    lattice_vectors = [np.asarray([a, 0, 0]),                        
                        np.asarray([0, a, 0]),                
                       np.asarray([0,0, l+a])],
    particles=[Spherocylinder([0, 0, 0],ori, diam, 'a')]
    )
    return cubic_cell
  
  def fcc_cell(a, l, diam=1): #This is clearly not a minimal cell, but it's what we need to tile with orthogonal vectors and with the rods aligned in the (0 0 1) direction
    ori = [0,0,l]
    h_step = l + np.sqrt(2/3) * a

    fcc_cell = Cell(
      lattice_vectors = [np.asarray([2 * a, 0, 0]),                        
                        np.asarray([0, np.sqrt(3) * a, 0]),                
                        np.asarray([0, 0, 3*h_step])],
      particles=[
                  Spherocylinder(np.asarray([0, 0, 0]), ori, diam, 'a'),
                  Spherocylinder(np.asarray([a, 0, 0]), ori, diam, 'a'),
                  Spherocylinder(np.asarray([0.5*a, np.sqrt(3)/2*a, 0]), ori, diam, 'a'),
                  Spherocylinder(np.asarray([1.5*a, np.sqrt(3)/2*a, 0]),ori,  diam, 'a'),
                  Spherocylinder(np.asarray([0.5*a, np.sqrt(3)/6*a, h_step]),ori, diam,'a'),
                  Spherocylinder(np.asarray([0*a, 2*np.sqrt(3)/3*a, h_step]),ori, diam,'a'),
                  Spherocylinder(np.asarray([1.5*a, np.sqrt(3)/6*a, h_step]),ori, diam,'a'),
                  Spherocylinder(np.asarray([1*a, 2*np.sqrt(3)/3*a, h_step]),ori, diam,'a'),
                  Spherocylinder(np.asarray([0,         (np.sqrt(3)/3)*a,               2*h_step]), ori, diam, 'a'),
                  Spherocylinder(np.asarray([1*a,       (np.sqrt(3)/3)*a,               2*h_step]), ori, diam, 'a'),
                  Spherocylinder(np.asarray([0.5*a,     (np.sqrt(3)/2 + np.sqrt(3)/3)*a,2*h_step]), ori, diam, 'a'),
                  Spherocylinder(np.asarray([1.5*a,     (np.sqrt(3)/2 + np.sqrt(3)/3)*a,2*h_step]), ori, diam, 'a')]
      )
    return fcc_cell
  
  
  def hex_cell(a, l, diam=1): #This is clearly not a minimal cell, but it's what we need to tile with orthogonal vectors and with the rods aligned in the (0 0 1) direction
    ori = [0,0,l]
    h_step = l + np.sqrt(2/3) * a

    hex_cell = Cell(
      lattice_vectors = [np.asarray([2 * a, 0, 0]),                        
                        np.asarray([0, np.sqrt(3) * a, 0]),                
                        np.asarray([0, 0, 2*h_step])],
      particles=[
                  Spherocylinder(np.asarray([0, 0, 0]), ori, diam, 'a'),
                  Spherocylinder(np.asarray([a, 0, 0]), ori, diam, 'a'),
                  Spherocylinder(np.asarray([0.5*a, np.sqrt(3)/2*a, 0]), ori, diam, 'a'),
                  Spherocylinder(np.asarray([1.5*a, np.sqrt(3)/2*a, 0]),ori,  diam, 'a'),
                  Spherocylinder(np.asarray([0.5*a, np.sqrt(3)/6*a, h_step]),ori, diam,'a'),
                  Spherocylinder(np.asarray([0, 2*np.sqrt(3)/3*a, h_step]),ori, diam,'a'),
                  Spherocylinder(np.asarray([1.5*a, np.sqrt(3)/6*a, h_step]),ori, diam,'a'),
                  Spherocylinder(np.asarray([1*a, 2*np.sqrt(3)/3*a, h_step]),ori, diam,'a')]
      )
    return hex_cell
    
  def S1_AB_cell(a, l, diam1 = 1, diam2 = 0.4):
    ori = [0,0,l]
    h_step = l + np.sqrt(2)/2 * a
    cubic_cell = Cell(
    lattice_vectors = [np.asarray( [a, 0, 0]),                        
                       np.asarray( [0, a, 0]),                
                        np.asarray([0,0, 2*h_step])],
    particles=[ Spherocylinder(np.asarray([0, 0, 0]), ori, diam1, 'a'),
                Spherocylinder(np.asarray([a/2., a/2., 0]),ori, diam2, 'b'),
                Spherocylinder(np.asarray([0, 0, h_step]), ori, diam2, 'b'),
                Spherocylinder(np.asarray([a/2., a/2., h_step]), ori, diam1, 'a')]
    )
    return cubic_cell