from space import Space
from arff import Arff
import sys
import random 
import math

NUM_TRIALS = 25

def read_args():
  if len(sys.argv) != 3:
    raise Exception("Wrong number of arguments!")
  arff_file1 = sys.argv[1]
  arff_file2 = sys.argv[2]
  return arff_file1, arff_file2

def _stats(data):
  N = len(data)
  mean = sum(data)/float(N)
  sum_of_squares = 0
  for x in data:
    sum_of_squares += (x-mean)**2
  sigma = math.sqrt((1/float(N-1))*sum_of_squares)
  return (mean, sigma)

def normalize(x, m, s):
  return (x-m)/float(s)

def mean_point(points):
  return tuple(map(lambda x: sum(x)/float(len(x)), zip(*zip(*points)[1])))

def k_means(k, space):
  max_iter = 50
  count = 0
  num_trials = 10
  used_randoms = []

  means_sses = []
  for i in range(num_trials):
    means = []
    for _ in range(k):
      index = random.randrange(1, len(space.points))
      means.append(space.points[index][1])
    while count < 50:
      new_means = map(lambda (index, part): mean_point(part) if part else means[index],
                                                   enumerate(space.partition(means)))
      if set(new_means) == set(means):
        break
      means = new_means
    means_sses.append((space.sum_squared_errors(means), means))
  return min(means_sses)[1] # default key is fst

def get_outliers(space, ratio):
  k = 2
  outliers = set()
  total_points = float(len(space.points))

  while len(outliers) < 5:
    means = k_means(k, space)
    parts = space.partition(means)
    for part in parts:
      if len(part)/total_points < ratio:
        for line_no, point in part:
          outliers.add(line_no)
    k += 1

  return outliers


def populate_space_from_arff(arff, space): 
  """
  the list of points in space is ordered
  """
  for line_no, train_point in arff.points:
    point = []
    for attr_type in arff.attributes:
      point.append(float(train_point[attr_type[0]]))
    space.put_point(line_no, *point)
   
def main():
  arff_file1, arff_file2 = read_args()
  arff1 = Arff.fromfile(arff_file1)
  arff2 = Arff.fromfile(arff_file2)
  norm_arff1 = arff1.normalize()
  norm_arff2 = arff2.normalize()

  space1= Space(len(norm_arff1.attributes))
  populate_space_from_arff(norm_arff1, space1)

  print "Outliers from "+arff_file1+":"
  for x in get_outliers(space1, 0.05):
    print x

  space2 = Space(len(norm_arff2.attributes))
  populate_space_from_arff(norm_arff2, space2)

  print "Outliers from "+arff_file2+":"
  for x in get_outliers(space2, 0.05):
    print x


if __name__ == "__main__":
  main()
