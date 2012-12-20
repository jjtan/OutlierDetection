import copy
import math

class Arff(object):
  DATA = '@data'

  def __init__(self, relation, attributes, points):
    self.relation = relation # string
    self.attributes = attributes # set
    self.points = points # list of (line_no, dicts)

  @staticmethod
  def _split_data(data_delim, lines):
    """ assumption: data runs till last element"""
    data_index = zip(*lines)[1].index(data_delim)
    data_index += 1 # and it better not be empty
    data = lines[data_index:]
    header = lines[:data_index]
    return [(line_no, point.split(',')) for line_no, point in data], [line.split() for _, line in header]

  @classmethod
  def fromfile(cls, filename):
    #parse here
    f = open(filename, 'r')
    lines = [(i+1, line.strip()) for i, line in enumerate(f.readlines())]
    lines = filter(lambda x: x[1], lines)  # identity function used when None
    data, header = cls._split_data(cls.DATA, lines)
    relation = ''
    attributes = []
    points = []
    for line in header:
      key = line[0].upper()
      if key == '@RELATION':
        relation = line[1]
      if key == '@ATTRIBUTE':
        attributes.append((line[1], line[2]))
    for line_no, point in data:
      zipped = zip(zip(*attributes)[0], point)
      entree = {}
      for pair in zipped:
        entree[pair[0].lower()] = pair[1] # point dict keys are all lowercase
      points.append((line_no, entree))
    return cls(relation, attributes, points)

  def output_file(self, filename):
    f = open(filename, 'w')
    f.write("@RELATION %s\n\n" % self.relation)
    for x in self.attributes:
      f.write("@ATTRIBUTE %s %s\n" % (x[0], x[1]))
    f.write("\n"+self.DATA+"\n")
    for _, x in self.points:
      output_list = []
      for y, _ in self.attributes:
        output_list.append(x[y])
      out = ','.join(map(str,output_list))
      f.write("%s\n" % out)

  # testing required
  def non_class_attrs(self, class_name):
    return filter(lambda x: x != class_name, zip(*arff.attributes)[0])

  def _print_arff(self):
    print "Relation:"
    print self.relation
    print "Attributes:"
    print self.attributes
    print "Points:"
    print self.points

  def copy_arff(self):
    #untested
    return Arff(self.relation, copy.deepcopy(self.attributes), copy.deepcopy(self.points))

  @staticmethod
  def _stats(data):
    data = [float(x) for x in data]
    N = len(data)
    mean = sum(data)/float(N)
    sum_of_squares = 0
    for x in data:
      sum_of_squares += (x-mean)**2
    sigma = math.sqrt((1/float(N-1))*sum_of_squares)
    return (mean, sigma)

  def normalize(self):
    """
      removes features with sigma 0
    """
    norm_arff = self.copy_arff()
    for attr_type in norm_arff.attributes:
      attr = attr_type[0]
      if attr_type[1].lower() == 'real':
        attr_points = map(lambda x: x[attr], zip(*norm_arff.points)[1])
        mean, sigma = Arff._stats(attr_points)
        if sigma > 0:
          #print "mean("+str(attr)+"): "+str(mean)
          #print "sigma("+str(attr)+"):"+str(sigma)
          for _, point in norm_arff.points:
            point[attr] = (float(point[attr])-mean)/sigma
        else:
          norm_arff.attributes = filter(lambda x: x[0] != attr, norm_arff.attributes)
          for point in norm_arff.points:
            del point[attr]
      else:
        norm_arff.attributes = filter(lambda x: x[0] != attr, norm_arff.attributes)
        for _, point in norm_arff.points:
          del point[attr]
    return norm_arff


def main():
  a = Arff.fromfile('veh-prime.arff')
  a.output_file('output.arff')

if __name__ == "__main__":
  main()

