#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
""" Script which checks if file with semantic network is consistent """

import sholva
import sys

def test_consistency(filename):
  net = sholva.Sholva(filename, ["_substance", "_pointable/person", "_event",
    "_pointable/person/individual", "_pointable/person/animal", "_pointable/person/profession", "_pointable/person/institution",
    "_pointable/person/nationality",
    "_pointable",
    "_valid_lemma/k1"])
  return net.check_consistency()

if __name__ == "__main__":
  if not len(sys.argv) == 2:
    print "Usage: check_consistency.py [file-with-network]"
    print "\tScript is intented to find most common syntax error in a file with semantic network"
    sys.exit(1)
  if test_consistency(sys.argv[1]):
    sys.exit(0)
  else:
    sys.exit(1)
