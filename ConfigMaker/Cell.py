import numpy as np
class Cell:
  def __init__(self, lattice_vectors, particles):
    self.lattice_vectors = np.array(lattice_vectors)
    self.particles = particles
    self.npart = len(particles)
    
    