#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
""" Test suite for library sholva - Test Driven Development approach """

import unittest
import sys
sys.path.append("../bin")
import sholva

DATASET_VODA = "data/dataset-voda.txt"
DATASET_COMMENT = "data/dataset-comment.txt"
DATASET_PES = "data/dataset-pes.txt"
DATASET_PES_PROFESSION = "data/dataset-pes-profession.txt"
DATASET_INCONSISTENT = "data/dataset-inconsistent.txt"
DATASET_TYPO = "data/dataset-typo.txt"
DATASET_TWICE = "data/dataset-twice.txt"
DATASET_TWICE_CONFLICT = "data/dataset-twice-conflict.txt"
DATASET_INHERITANCE = "data/dataset-inheritance.txt"

class TestSholva(unittest.TestCase):
  def test_class_existence(self):
    """ Check if we class can be instatizied """
    sholva.Sholva(DATASET_VODA)

  def test_load_network_positive(self):
    """ Load file with network and check word that IS network """
    con = sholva.Sholva(DATASET_VODA)
    self.assertEquals(con.contains(u"voda"), True)

  def test_load_network_negative(self):
    """ Load file with network and check word that IS NOT network """
    con = sholva.Sholva(DATASET_VODA)
    self.assertEquals(con.contains(u"pes"), False)

  def test_load_network_with_comment(self):
    """ Load file with network that contains comments """
    sholva.Sholva(DATASET_COMMENT)

  def test_positive_person(self):
    """ Test if token that is positive _person """
    con = sholva.Sholva(DATASET_PES)
    self.assertEquals(con.in_class(u"pes", u"_person"), sholva.Sholva.POSITIVE)

  def test_negative_person(self):
    """ Test if token that is negative _person """
    con = sholva.Sholva(DATASET_PES)
    self.assertEquals(con.in_class(u"voda", u"_person"), sholva.Sholva.NEGATIVE)

  def test_unknown_person(self):
    """ Test if token that is negative _person """
    con = sholva.Sholva(DATASET_PES)
    self.assertEquals(con.in_class(u"qwerty", u"_person"), sholva.Sholva.UNKNOWN)

  def test_unknown_animal(self):
    """ Test if token that is positive _person """
    con = sholva.Sholva(DATASET_PES)
    self.assertEquals(con.in_class(u"pes", u"_animal"), sholva.Sholva.UNKNOWN)

  def test_negative_inheritance(self):
    """ Test if negative inheritance is working. So, if X is negative Y then it is also negative Y/Z """
    con = sholva.Sholva(DATASET_VODA)
    self.assertEquals(con.in_class(u"voda", u"_person/individual"), sholva.Sholva.NEGATIVE)

  def test_unknown_inheritance(self):
    """ Test if negative inheritance is working. So, if X is negative Y then it is also negative Y/Z """
    con = sholva.Sholva(DATASET_PES_PROFESSION)
    self.assertEquals(con.in_class(u"pes", u"_person/profession/manual"), sholva.Sholva.NEGATIVE)

  def test_check_consistency_positive(self):
    """ Check that semantic network is consistent in inheritenance """
    con = sholva.Sholva(DATASET_PES_PROFESSION)
    self.assertEquals(con.check_consistency(), True)

  def test_check_consistency_negative(self):
    """ Check that semantic network is NOT consistent in inheritenance """
    con = sholva.Sholva(DATASET_INCONSISTENT)
    self.assertEquals(con.check_consistency(), False)

  def test_check_name_consistency_positive(self):
    """ Check if names of semantic classes are only those expected """
    con = sholva.Sholva(DATASET_PES_PROFESSION)
    self.assertEquals(con.check_consistency(), True)
    con2 = sholva.Sholva(DATASET_PES_PROFESSION, semclasses=["_person", "_person/profession"])
    self.assertEquals(con2.check_consistency(), True)

  def test_check_name_consistency_negative(self):
    """ Check if names of semantic classes are NOT those expected """
    con = sholva.Sholva(DATASET_PES_PROFESSION, semclasses=[])
    self.assertEquals(con.check_consistency(), False)
    con2 = sholva.Sholva(DATASET_PES_PROFESSION, semclasses=[u"xyz"])
    self.assertEquals(con2.check_consistency(), False)

  def test_person_uppercase_already_positive(self):
    """ Token starting with uppercase should be positive, if it was positive in lowercase """
    con = sholva.Sholva(DATASET_PES)
    self.assertEquals(con.POSITIVE, con.in_class(u"Pes", "_person"))

  def test_person_uppercase_negative(self):
    """ Token starting with uppercase should not be -anything because it can be NE """
    con = sholva.Sholva(DATASET_PES)
    self.assertEquals(con.UNKNOWN, con.in_class(u"Voda", "_person"))

  @unittest.skip("Not implemented yet")
  def test_person_pointable(self):
    """ Inheritance should also work between person and pointable """
    # @todo: improve debug -> logging
    self.assertEquals(True, False)

  def test_typo_consistency(self):
    """ If word is typo then it can't be + in any other class """
    con = sholva.Sholva(DATASET_TYPO)
    self.assertEquals(False, con.check_consistency())

  def test_duplicity_consistency(self):
    """ If same records are listed twice, consistency should find this problem """
    try:
      self.assertRaises(SyntaxError, sholva.Sholva(DATASET_TWICE_CONFLICT))
    except SyntaxError:
      pass

  def test_conflict_consistency(self):
    """ If same records are listed twice with different polarity, consistency should find this problem """
    try:
      self.assertRaises(SyntaxError, sholva.Sholva(DATASET_TWICE_CONFLICT))
    except SyntaxError:
      pass

  def test_inheritance(self):
    """ If 'hroch' is (_person/animal +) than it has to be (_person +) too """
    con = sholva.Sholva(DATASET_INHERITANCE)
    self.assertEquals(con.POSITIVE, con.in_class(u"hroch", "_person"))

if __name__ == "__main__":
  unittest.main()
