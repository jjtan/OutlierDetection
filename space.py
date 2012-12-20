from math import sqrt

class Space:
  def __init__(self, dimensions):
    self.dimensions = dimensions
    self.points = [] # ele - ( *pos)

  def put_point(self, val, *position):
    if len(position) < self.dimensions:
      raise Exception("Space: too few dimensions specified during putPoint")
    self.points.append((val, position[0:self.dimensions]))
    
  def print_points(self):
    for point in self.points:
      print point

  def sum_squared_errors(self, means):
    error = 0

    for _, point in self.points:
      distances = []
      for mean in means:
        distance = 0
        for i in range(self.dimensions):
          distance += (mean[i] - point[i])**2
        distances.append(distance)
      error += min(distances)

    return error

  def find_k_closest_in_order(self, k, point):
    if len(point) < self.dimensions:
      raise Exception("Too few dimensions in point")
    distances = []
    for line_no, p in self.points:
      distance = 0
      for i in range(self.dimensions):
        distance += (point[i] - p[i])**2
      distance = sqrt(distance)
      distances.append((distance, line_no))
    distances.sort() # default fst
    return distances[0:k]

  def partition(self, mean_set):
    """
    partition points given a number of centroids
    mean_dict - { index: [2,5.2,3.3]}
    returns - { index: mean_points }
    """
    means = {}
    for k, mean in enumerate(mean_set):
      means[k] = mean

    partitions = {}
    for k in means.keys():
      partitions[k] = []

    for line_no, point in self.points:
      distances = []
      for k, v in means.iteritems():
        distance = 0
        for i in range(self.dimensions):
          distance += (v[i] - point[i])**2
        distances.append((sqrt(distance), k))
      distances.sort(key=lambda x: x[0])
      partitions[distances[0][1]].append((line_no, point))

    return partitions.values()
    
if __name__ == "__main__":
  space = Space(3)
  space.put_point(1, 2.2, 3)
  space.put_point(1.2, 5.2, 1.3)
  space.put_point(3, 2.3, 3)
  space.put_point(5.1, 9, 8.1)
  space.put_point(6.3, 8.2, 7.0)
  space.print_points()
  print space.k_means({1:(0,0,0),2:(10,12,9)})
  
