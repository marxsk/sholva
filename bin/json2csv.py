#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
""" Script that transform JSON file from annotation tool to a format used in sholva.txt """

import json
import sys
import codecs
import logging

def parse_json(filename):
  json_data = open(filename)
  data = json.load(json_data)

  for np in data["frames"]:
    if np["head"] != None or np["head"] != "null":
      try:
        print "#".join([np["semantic"].strip(), np["head"].strip(), np["status"].strip()])
      except Exception:
        logging.warning("JSON block for '%s' is invalid, ignoring", np["head"])

if __name__ == "__main__":
  sys.stdout = codecs.getwriter('utf8')(sys.stdout)
  parse_json(sys.argv[1])
