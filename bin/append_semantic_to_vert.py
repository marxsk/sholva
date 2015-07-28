#!/usr/bin/python -tt

""" Script that is used to append semantic information to vertical """

import sholva
import sys
import codecs

def append_to_vertical(network, output_classes):
  """ Append semantic information to vertical from stdin """
  net = sholva.Sholva(network)
  semclasses = output_classes.split(",")

  for line in sys.stdin:
    items = line.rstrip().split("\t")
    if len(items) < 3:
      print line.rstrip("\n")
    else:
      lemma = items[1]
      tag = items[2]

      # Corpus specific part - we want to tag only nouns (k1 in our system)
      #   when it will make sense, it will be more generic
      if not "k1" in tag:
        print line.rstrip("\n")
      else:
        append_text = ""
        for s in semclasses:
          value = net.in_class(lemma, s)
          if value == sholva.Sholva.POSITIVE:
            append_text += "\t+"
          elif value == sholva.Sholva.NEGATIVE:
            append_text += "\t-"
          else:
            append_text += "\t?"
        print "%s%s" % (line.rstrip(), append_text)

if __name__ == "__main__":
  sys.stdin = codecs.getreader("utf-8")(sys.stdin)
  sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

  if not len(sys.argv) == 3:
    print "Usage: append_semantic_to_vert.py [file-with-network] [semantic classes separated by ,]"
    print "\tAdd semantic classes to vertical obtained from STDIN"
    sys.exit(1)
  if append_to_vertical(network=sys.argv[1], output_classes=sys.argv[2]):
    sys.exit(0)
  else:
    sys.exit(1)
