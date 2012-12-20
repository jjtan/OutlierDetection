from space import Space
from arff import Arff
import sys
import random 
import math


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

def mean_point(points):
  return tuple(map(lambda x: sum(x)/float(len(x)), zip(*zip(*points)[1])))

def find_connected(edges):
  reps = {} # line_no, min in set
  sets = {}
  
  line_nos = set()
  for a, b in edges:
    line_nos.add(a)
    line_nos.add(b)

  for x in line_nos:
    reps[x] = x
    sets[x] = set([x])

  for a, b in edges:
    new_set = sets[reps[a]].union(sets[reps[b]])
    del sets[max(reps[a], reps[b])]
    rep = min(reps[a], reps[b])
    for x in new_set:
      reps[x] = rep
    sets[rep] = new_set

  return sets.values()

def get_outliers(min_size, k, space):
  """
  return dict of line_no: [line_no]
  """

  # get the k closest points for each point (including self)
  d = {}
  for line_no, point in space.points:
    d[line_no] = zip(*space.find_k_closest_in_order(k, point))[1] # we don't care about distance, just line_no

  # if a is in the k closest points of b and vice versa add edge (a, b), where a < b
  edges = []
  for k, v in d.iteritems():
    for nos in v:
      if k in d[nos]:
        edges.append(tuple(sorted([k, nos])))

  clusters = find_connected(edges)

  outliers = []

  for cluster in clusters:
    if len(cluster) < min_size:
      for point in cluster:
        outliers.append(point)

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
  outliers1 = get_outliers(3, 5, space1)
  if outliers1:
    for x in outliers1:
      print x
  else:
    print "None"

  space2 = Space(len(norm_arff2.attributes))
  populate_space_from_arff(norm_arff2, space2)

  print "Outliers from "+arff_file2+":"
  outliers2 = get_outliers(3, 12, space2)
  if outliers2:
    for x in outliers2:
      print x
  else:
    print "None"

if __name__ == "__main__":
  main()

