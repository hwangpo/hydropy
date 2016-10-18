# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 23:30:01 2016

@author: Marty
"""
from __future__ import absolute_import, print_function

try:
    from unittest import mock
except ImportError:
    import mock
import unittest

import hydropy as hp


class TestStation(unittest.TestCase):

    def test_Station_inits_site(self):
        actual = hp.Station('any')
        expected = 'any'
        self.assertEqual(expected, actual.site)

    def test_Station_str_returns_str(self):
        actual = hp.Station('any')
        # This might be a dumb test, because I think an error gets thrown if
        # a __str__ function doesn't return a string.  Hmmm.
        self.assertIsInstance(actual.__repr__(), str)

    def test_Station_repr_returns_str(self):
        actual = hp.Station('any')
        self.assertIsInstance(actual.__repr__(), str)

    def test_Station_htmlrepr_returns_html(self):
        actual = hp.Station('any')
        # IPython will take advantage of this function if it exists; The
        # purpose is to display a table of data as html instead of as a string.
        self.assertIsInstance(actual._repr_html_(), str)
        # perhaps it also makes sense to do a regex to check for proper html?

    @mock.patch('hydropy.get_usgs')
    def test_Station_fetch_accepts_source_usgs_iv(self, mock_get):
        expected = 'mock data'
        mock_get.return_value = expected

        actual = hp.Station('any')
        actual.fetch(source='usgs-iv', start='A', end='B')

        mock_get.assert_called_once_with('any', 'iv', 'A', 'B')
        self.assertEqual(expected, actual.data)

    @mock.patch('hydropy.get_usgs')
    def test_Station_fetch_accepts_source_usgs_dv(self, mock_get):
        expected = 'mock data'
        mock_get.return_value = expected

        actual = hp.Station('any')
        actual.fetch(source='usgs-dv', start='A', end='B')

        mock_get.assert_called_once_with('any', 'dv', 'A', 'B')
        self.assertEqual(expected, actual.data)

    def test_Station_raises_HydroSourceError_for_bad_source(self):
        with self.assertRaises(hp.HydroSourceError):
            actual = hp.Station("any")
            actual.fetch(source='nonsense')


class TestAnalysis(unittest.TestCase):

    def test_Analysis_accepts_usgsdv_list(self):
        actual = hp.Analysis(['01585200', '01581500'], source='usgs-dv')
        expected = 'usgs-dv'
        self.assertEqual(expected, actual.source)

    def test_Analysis_accepts_usgsiv_list(self):
        actual = hp.Analysis(['01585200', '01581500'], source='usgs-iv')
        expected = 'usgs-iv'
        self.assertEqual(expected, actual.source)

    def test_Analysis_accepts_dict(self):
        actual = hp.Analysis({'blah': 'blah'})
        expected = 'dict'
        self.assertEqual(expected, actual.source)

    def test_Analysis_raises_HydroSourceError_for_bad_source(self):
        with self.assertRaises(hp.HydroSourceError):
            actual = hp.Analysis([1, 2, 3], source='nonsense')