import math

radp=180/math.pi
CSq5P2=((2,1),(2,0),(2,-1), \
        (1,2),(1,1),(1,0),(1,-1),(1,-2), \
        (0,2),(0,1),(0,0),(0,-1),(0,-2), \
        (-1,2),(-1,1),(-1,0),(-1,-1),(-1,-2), \
        (-2,1),(-2,0),(-2,-1))
CSq5=((3,1),(3,0),(3,-1), \
      (2,2),(2,1),(2,0),(2,-1),(2,-2), \
      (1,3),(1,2),(1,1),(1,0),(1,-1),(1,-2),(1,-3), \
      (0,3),(0,2),(0,1),(0,0),(0,-1),(0,-2),(0,-3), \
      (-1,3),(-1,2),(-1,1),(-1,0),(-1,-1),(-1,-2),(-1,-3), \
      (-2,2),(-2,1),(-2,0),(-2,-1),(-2,-2), \
      (-3,1),(-3,0),(-3,-1))
def fl(x):
    return int(math.floor(x+1e-7))