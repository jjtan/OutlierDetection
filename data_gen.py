import random
from arff import Arff

def generate_norm(num_points, dim, means, sigmas):
  points = []
  for _ in range(num_points):
    point = []
    for i in range(dim):
      point.append(random.gauss(means[i], sigmas[i]))
    points.append(point)
  return points

def main():
  num_points = 100
  dim = 2
  means = [2.4, 5.5, 6.2]
  sigmas = [1, 1.5, 0.5]
  raw_points = generate_norm(num_points, dim, means, sigmas)

  attrs = []
  for d in range(dim):
    attrs.append(('f'+str(d), 'real'))

  points = []
  for i in range(num_points):
    point = {}
    for j, (attr, _) in enumerate(attrs):
      point[attr] = raw_points[i][j]
    points.append((i+1, point))

  relation = 'DATASET'

  arff = Arff(relation, attrs, points)
  arff._print_arff()
  arff.output_file("synthetic.arff")

if __name__ == "__main__":
  main()

