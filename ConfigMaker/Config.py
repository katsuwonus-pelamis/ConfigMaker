from .Snapshot import *
import numpy as np
import pandas as pd
import os

class Config:
  def __init__(self, nframes, frames):
    self.nframes = nframes
    self.frames = frames
    
  def read(filename):
    frames = []
    print(os.path.splitext(filename))
    ext = os.path.splitext(filename)[1]
    particle_type = 'spherocylinder' if ext == '.rod' else 'sphere' if ext == '.sph' else None
    
    with open(filename, 'r') as f:
        while True:
            snap = Snapshot.read(f, particle_type)
            if snap is None:
                break
            frames.append(snap)
    nframes = len(frames)
    return Config(nframes, frames)
    
  def write(self, filename):
    open(filename, 'w').close() #this overwrites the eventually existing configuration while allowing to use append in the smaller write calls
    for frame in self.frames:
      frame.write(filename)
  
  def csv_to_rod(filename):
    csv = pd.read_csv(filename, header=0, skiprows=[1, 2, 3])
    csv.fillna(0, inplace=True)
    csv = csv.sort_values('FRAME')
    nframes = np.max(csv["FRAME"])
    frames = []
    for frame_id, group in csv.groupby('FRAME'):
      snapshot = Snapshot.csv_to_rod(group)
      frames.append(snapshot)
    return Config(nframes, frames)
    