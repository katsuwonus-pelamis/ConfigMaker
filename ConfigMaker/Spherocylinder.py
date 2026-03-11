import numpy as np

class Spherocylinder:
  def __init__(self, pos, ori, diameter, specie):
    self.pos = pos
    self.ori = ori
    self.diameter = diameter
    self.specie = specie

  def read(line):
    parts = line.strip().split()
    specie = parts[0]
    pos = [float(parts[1]), float(parts[2]), float(parts[3])]
    diameter = float(parts[4])
    ori = [float(parts[5]), float(parts[6]), float(parts[7])]
    return Spherocylinder(pos, ori, diameter, specie)
  
  def write(self, filename):
    with open(filename, 'a') as f:
      pos_str = " ".join(str(x) for x in self.pos)
      ori_str = " ".join(str(x) for x in self.ori)
      f.write(f"{self.specie} {pos_str} {self.diameter} {ori_str}\n")
      
  def csv_to_rod(row):
    pos = [row['POSITION_X'], row['POSITION_Y'], row['POSITION_Z']] 
    ori = [np.cos(float(row["ELLIPSE_THETA"]))*float(row["ELLIPSE_MAJOR"]), np.sin(float(row["ELLIPSE_THETA"]))*float(row["ELLIPSE_MAJOR"]), 0]
    return Spherocylinder(pos, ori, row['RADIUS']*2, 'a')
  
  def get_volume(self):
    return np.pi * self.diameter**2 * (np.linalg.norm(self.ori)+ 2./3. * self.diameter)/ 4