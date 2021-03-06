# -*- coding: utf-8 -*-

import unittest

from pyramid import testing

from chsdi.lib.helpers import make_agnostic, make_api_url, check_url, transformCoordinate, sanitize_url, check_even, round, format_search_text, remove_accents, escape_sphinx_syntax, quoting, float_raise_nan, resource_exists, parseHydroXML

from urlparse import urljoin


class Test_Helpers(unittest.TestCase):

    def test_make_agnostic(self):
        url = 'http://foo.com'
        agnostic_link = make_agnostic(url)
        self.assertTrue(not agnostic_link.startswith('http://'))
        self.assertTrue(agnostic_link.startswith('//'))

        url_2 = 'https://foo.com'
        agnostic_link_2 = make_agnostic(url_2)
        self.assertTrue(not agnostic_link_2.startswith('https://'))
        self.assertTrue(agnostic_link_2.startswith('//'))

        url_3 = '//foo.com'
        agnostic_link_3 = make_agnostic(url_3)
        self.assertEqual(url_3, agnostic_link_3)

    def test_resource_exists(self):
        test_path = 'https://api3.geo.admin.ch'
        test_result = resource_exists(test_path)
        self.assertTrue(test_result)

        test_path2 = 'http://dummy.com'
        test_result2 = resource_exists(test_path2)
        self.assertTrue(test_result2)

    def test_make_api_url(self):
        request = testing.DummyRequest()
        request.host = 'api3.geo.admin.ch'
        request.scheme = 'http'
        request.registry.settings = {}
        request.registry.settings['apache_base_path'] = 'main'
        api_url = make_api_url(request, agnostic=True)
        self.assertTrue(not api_url.startswith('http://'))
        self.assertTrue(api_url.startswith('//'))
        self.assertEqual(api_url, '//api3.geo.admin.ch')

        request.scheme = 'https'
        api_url = make_api_url(request)
        self.assertEqual(api_url, 'https://api3.geo.admin.ch')

        request.host = 'localhost:9000'
        request.scheme = 'http'
        api_url = make_api_url(request)
        self.assertEqual(api_url, api_url)

    def test_check_url(self):
        from pyramid.httpexceptions import HTTPBadRequest
        url = None
        config = {'shortener.allowed_hosts': 'admin.ch,swisstopo.ch,bgdi.ch'}
        try:
            check_url(url, config)
        except Exception as e:
            self.assertTrue(isinstance(e, HTTPBadRequest))

        url = 'dummy'
        try:
            check_url(url, config)
        except Exception as e:
            self.assertTrue(isinstance(e, HTTPBadRequest))

        url = 'http://dummy.com'

        try:
            check_url(url, config)
        except Exception as e:
            self.assertTrue(isinstance(e, HTTPBadRequest))

        url = 'http://admin.ch'
        self.assertEqual(url, check_url(url, config))

    def test_sanitize_url(self):
        base_url_string = 'http://somehost.com/some/path/here'
        relative_url_string = 'http://somehost.com/some/other/path'
        result1 = sanitize_url(base_url_string)
        self.assertEqual(result1, base_url_string)

        result2 = sanitize_url(relative_url_string)
        self.assertEqual(result2, relative_url_string)

        self.assertNotEqual(result1, urljoin(base_url_string, relative_url_string))

        self.assertEqual(result2, urljoin(base_url_string, relative_url_string))

    def test_sanitize_url_throws_ValueError(self):
        # ValueError
        url2 = None
        result2 = sanitize_url(url2)
        self.assertRaises(ValueError, result2)

    def test_parseHydroXML(self):
        import xml.etree.ElementTree as ET

        tree = ET.parse('filename.xml')
        root = tree.getroot()
        test_result = parseHydroXML('idname', root)
        self.assertEqual({'date_time': '01 September 8Uhr', 'wasserstand': '-', 'wassertemperatur': '-', 'abfluss': '141100'}, test_result)

        tree2 = ET.parse('filename2.xml')
        root2 = tree2.getroot()
        test_result2 = parseHydroXML('idname', root2)
        self.assertEqual({'date_time': '04 Oktober 11 Uhr', 'wasserstand': '59900', 'wassertemperatur': '-', 'abfluss': '-'}, test_result2)

        tree3 = ET.parse('filename3.xml')
        root3 = tree3.getroot()
        test_result3 = parseHydroXML('idname', root3)
        self.assertEqual({'date_time': '16 Mai 18 Uhr', 'wasserstand': '-', 'wassertemperatur': '59900', 'abfluss': '-'}, test_result3)

    def test_transformCoordinate(self):
        from osgeo.ogr import Geometry
        wkt = 'POINT (7.37840 45.91616)'
        srid_from = 4326
        srid_to = 21781
        wkt_21781 = transformCoordinate(wkt, srid_from, srid_to)
        self.assertTrue(isinstance(wkt_21781, Geometry))
        self.assertEqual(int(wkt_21781.GetX()), 595324)
        self.assertEqual(int(wkt_21781.GetY()), 84952)

    def test_check_even(self):
        testnumber = 10
        result = check_even(testnumber)
        self.assertTrue(result)

        testnumber = 5
        result = check_even(testnumber)
        self.assertFalse(result)

    def test_round(self):
        testnumber = 4.4
        result = round(testnumber)
        self.assertEqual(result, 4)

    def test_format_search_text(self):
        testinput_str = 'Hallo!'
        result = format_search_text(testinput_str)
        self.assertEqual(result, 'Hallo\\!')

        testinput_str2 = u'über'
        result2 = format_search_text(testinput_str2)
        self.assertEqual(result2, 'ueber')

    def test_remove_accents(self):
        testinput_str = None
        result = remove_accents(testinput_str)
        self.assertEqual(result, None)

    def test_escape_sphinx_syntax(self):
        testinput_str = None
        result = escape_sphinx_syntax(testinput_str)
        self.assertEqual(result, None)

    def test_quoting(self):
        testtext = 'Hallo'
        result = quoting(testtext)
        self.assertEqual(result, 'Hallo')

    def test_float_raise_nan(self):
        testval = 5
        result = float_raise_nan(testval)
        self.assertEqual(result, 5.0)
        self.assertRaises('ValueError')
