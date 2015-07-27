#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
""" Library for easy manipulation with semantic network Sholva """
import codecs
import logging

class Sholva(object):
  """ Object that encapsulated operation over semantic network """
  _ITEMS_IN_RECORD = 3
  _ITEM_TOKEN = 0
  _ITEM_SEMANTIC_CLASS = 1
  _ITEM_VALUE = 2

  POSITIVE = 1
  NEGATIVE = -1
  UNKNOWN = 0

  def __init__(self, network_file, semclasses=None):
    """ Constructor that automatically load semantic network

    semclasses = list of expected semclasses or None (anything is acceptable)
    """
    self._network = {}
    self._load_network(network_file)
    self._semclasses = semclasses

  def contains(self, token):
    """ Check if there is any information about token in the loaded network """
    return token in self._network

  def _load_network(self, network_file):
    """ Load semantic network from local file """
    for line in codecs.open(network_file, "r", "utf-8").readlines():
      items = line.strip().split(u"#")
      if line.startswith(u"#") or line.strip() == "":
        pass
      elif len(items) == self._ITEMS_IN_RECORD:
        if self._network.get(items[self._ITEM_TOKEN], None) is None:
          self._network[items[self._ITEM_TOKEN]] = \
              {items[self._ITEM_SEMANTIC_CLASS] : items[self._ITEM_VALUE]}
        else:
          self._network[items[self._ITEM_TOKEN]][items[self._ITEM_SEMANTIC_CLASS]] = items[self._ITEM_VALUE]
      else:
        raise SyntaxError("Line '%s' is not in the required format" % (line))

  def in_class(self, token, semantic_class):
    """ Return information that we have for given token and semantic class (it can be inherited)"""
    token_lc = token.lower()

    token_semclasses = self._network.get(token_lc, None)
    value = token_semclasses.get(semantic_class, None) if token_semclasses else None
    if value == u"+":
      return self.POSITIVE
    elif value == u"-":
      # capitalized tokens can be NE, so they are unknown, not negative
      if token_lc[0] == token[0]:
        return self.NEGATIVE
      else:
        return self.UNKNOWN
    elif value is None:
      # inheritance of negative value of semantic class
      if token_semclasses:
        for semclass in self._network[token_lc].keys():
          if semantic_class.startswith(semclass + u"/") and self._network[token_lc][semclass] == u"-":
            return self.NEGATIVE
      return self.UNKNOWN
    else:
      raise SyntaxError("Value '%s' for token '%s' is not valid value" % (value, token))

    return True

  def check_consistency(self):
    """ Check if semantic network is consistent when all constraints are evaluated """
    if not self._check_consistency_inheritance():
      return False
    elif not self._check_consistency_names():
      return False
    else:
      return True

  def _check_consistency_inheritance(self):
    """ Check if inheritance in semantic network is working as expected by in_class() """
    for token in self._network:
      for semclass in self._network[token]:
        for semclass2 in self._network[token]:
          if semclass == semclass2:
            continue
          else:
            if semclass.startswith(semclass2 + "/") and self._network[token][semclass] == u"+" and \
                self._network[token][semclass2] == u"-":
              logging.error("Token '%s' has inconsistent semantic values between '%s' and '%s'", \
                token, semclass, semclass2)
              return False
            elif semclass2.startswith(semclass + "/") and self._network[token][semclass2] == u"+" and \
                self._network[token][semclass] == u"-":
              logging.error("Token '%s' has inconsistent semantic values between '%s' and '%s'", \
                token, semclass2, semclass)
              return False

    return True

  def _check_consistency_names(self):
    """ Check if names of semantic classses are between those expected """
    if self._semclasses is None:
      return True

    for token in self._network:
      for semclass in self._network[token]:
        if not semclass in self._semclasses:
          logging.error("Token '%s' has undefined semantic class '%s' ", token, semclass)
          return False

    return True
