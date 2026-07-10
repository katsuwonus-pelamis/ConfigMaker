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
  
  def from_sphere(sphere, length, ori_axis = 2):
    ori =  np.zeros(3)
    ori[ori_axis] = length
    return Spherocylinder(sphere.pos,ori,sphere.radius*2, sphere.specie)
  
  def csv_to_rod(row):
    pos = [row['POSITION_X'], row['POSITION_Y'], row['POSITION_Z']] 
    ori = [np.cos(float(row["ELLIPSE_THETA"]))*float(row["ELLIPSE_MAJOR"]), np.sin(float(row["ELLIPSE_THETA"]))*float(row["ELLIPSE_MAJOR"]), 0]
    return Spherocylinder(pos, ori, row['RADIUS']*2, 'a')
  
  def get_volume(self):
    return np.pi * self.diameter**2 * (np.linalg.norm(self.ori)+ 2./3. * self.diameter)/ 4
  

  def spherocylinder_distance(r1, r2, threshold=1e-10):
    # Assuming r1.pos, r2.pos, r1.ori, r2.ori are all 1D NumPy arrays
    r12 = r2.pos - r1.pos
    
    xl1 = np.linalg.norm(r1.ori)/2.
    xl2 = np.linalg.norm(r2.ori)/2.
    ori1 = r1.ori/np.linalg.norm(r1.ori)
    ori2 = r2.ori/np.linalg.norm(r2.ori)
    
    # NumPy dot product syntax
    u12 = np.dot(ori1, ori2)
    ru1 = np.dot(r12, ori1)
    ru2 = np.dot(r12, ori2)
    
    cc = 1.0 - u12 * u12  # 0-or-so if parallel
    lam = 0.0
    mu = 0.0
    
    if abs(cc) < threshold:
        if ru1 != 0:
            lam = np.copysign(xl1, ru1)
            mu = lam * u12 - ru2
            if abs(mu) > xl2:
                mu = np.copysign(xl2, mu)
        else:
            lam = 0.0
            mu = 0.0
    else:
        lam = (ru1 - u12 * ru2) / cc  # first actual guess
        mu = (-ru2 + u12 * ru1) / cc
        
        if abs(lam) > xl1 or abs(mu) > xl2:
            aux1 = abs(lam) - xl1
            aux2 = abs(mu) - xl2
            if aux1 > aux2:
                lam = np.copysign(xl1, lam)
                mu = lam * u12 - ru2
                if abs(mu) > xl2:
                    mu = np.copysign(xl2, mu)
            else:
                mu = np.copysign(xl2, mu)
                lam = mu * u12 + ru1
                if abs(lam) >= xl1:
                    lam = np.copysign(xl1, lam)
                    

    r12_norm2 = np.dot(r12, r12)
    
    return (r12_norm2 + lam**2 + mu**2 - 2.0 * lam * mu * u12 
            + 2.0 * mu * ru2 - 2.0 * lam * ru1)
    
    
    
  
  
class Sphere:

  def __init__(self, pos, radius, specie):
    self.pos = pos
    self.radius = radius
    self.specie = specie

  def read(line):
    parts = line.strip().split()
    specie = parts[0]
    pos = [float(parts[1]), float(parts[2]), float(parts[3])]
    radius = float(parts[4])
    return Sphere(pos, radius, specie)
  
  def write(self, filename):
    with open(filename, 'a') as f:
      pos_str = " ".join(str(x) for x in self.pos)
      f.write(f"{self.specie} {pos_str} {self.radius}\n")
      
  
  def get_volume(self):
    return 4./3. * np.pi * self.radius**3