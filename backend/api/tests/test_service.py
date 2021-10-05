import operator
from collections import namedtuple

from django.test import TestCase
from rest_framework import serializers

from api.service import calc_cpc, calc_cpm, sort_response, sort_dict, get_key_func


class ServiceTest(TestCase):

    def test_calc_cpc(self):
        with self.assertRaises(serializers.ValidationError):
            calc_cpc({'user': 'admin'})
        self.assertTrue(calc_cpc({'cost': 1000, 'clicks': 0}) == 0)
        self.assertTrue(calc_cpc({'cost': 1000, 'clicks': 100}) == 10)

    def test_calc_cpm(self):
        with self.assertRaises(serializers.ValidationError):
            calc_cpm({'user': 'admin'})
        self.assertTrue(calc_cpm({'cost': 1000, 'views': 0}) == 0)
        self.assertTrue(calc_cpm({'cost': 10, 'views': 1}) == 10000)

    def test_sort_response(self):
        request = namedtuple('request', ['query_params'])
        request.query_params = {'ordering': 'views'}
        response = namedtuple('response', ['data'])
        response.data = [
            {'date': '2021-10-10', 'views': 1000, 'cpc': 10},
            {'date': '2021-15-10', 'views': 1500, 'cpc': 1084},
            {'date': '2020-10-10', 'views': 180, 'cpc': 180},
            {'date': '2021-10-13', 'views': 1, 'cpc': 1, 'clicks': 10},
        ]
        self.assertEqual(sort_response(response=response, request=request).data,
                         [
                             {'date': '2021-10-13', 'views': 1, 'cpc': 1, 'clicks': 10},
                             {'date': '2020-10-10', 'views': 180, 'cpc': 180},
                             {'date': '2021-10-10', 'views': 1000, 'cpc': 10},
                             {'date': '2021-15-10', 'views': 1500, 'cpc': 1084}
                         ])

    def test_sort_dict(self):
        data = [{'date': '2021-10-10', 'views': 1000, 'cpc': 10},
                {'date': '2021-15-10', 'views': 1500, 'cpc': 1084},
                {'date': '2020-10-10', 'views': 180, 'cpc': 180},
                {'date': '2021-10-13', 'views': 1, 'cpc': 1, 'clicks': 10}]
        self.assertEqual(sort_dict(data, "views"),
                         [
                             {'date': '2021-10-13', 'views': 1, 'cpc': 1, 'clicks': 10},
                             {'date': '2020-10-10', 'views': 180, 'cpc': 180},
                             {'date': '2021-10-10', 'views': 1000, 'cpc': 10},
                             {'date': '2021-15-10', 'views': 1500, 'cpc': 1084}
                         ])
        self.assertEqual(sort_dict(data, "-cpc"),
                         [
                             {'date': '2021-15-10', 'views': 1500, 'cpc': 1084},
                             {'date': '2020-10-10', 'views': 180, 'cpc': 180},
                             {'date': '2021-10-10', 'views': 1000, 'cpc': 10},
                             {'date': '2021-10-13', 'views': 1, 'cpc': 1, 'clicks': 10}
                         ])
        with self.assertRaises(KeyError):
            sort_dict(data, 'post')

    def test_get_key_func(self):
        self.assertTrue(get_key_func('views'),
                        operator.itemgetter('views')
                        )
        self.assertFalse(get_key_func('cost') is operator.itemgetter('cost'))
