from collections import OrderedDict
from decimal import Decimal

from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase


class APITest(APITestCase):
    fixtures = ['data.json']

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/'
        self.url_range = 'http://127.0.0.1:8000/?from=2018-01-01&to=2020-05-10'
        self.url_range_order = 'http://127.0.0.1:8000/?from=2018-01-01&to=2020-05-10&ordering=-date'
        self.url_order = 'http://127.0.0.1:8000/?ordering=-date'
        self.client.login(username='admin', password='admin')

    def test_list(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert len(response.data) == 7

    def test_list_with_range(self):
        response = self.client.get(self.url_range)
        assert response.status_code == 200
        assert response.data == [OrderedDict([('date', '2020-03-01'),
                                              ('views', 102572),
                                              ('clicks', 4454),
                                              ('cost', '375.67'),
                                              ('cost_currency', 'RUB'),
                                              ('cpc', Decimal('545.4550000')),
                                              ('cpm', Decimal('3435.0000'))]),
                                 OrderedDict([('date', '2020-01-30'),
                                              ('views', 1028425),
                                              ('clicks', 445544),
                                              ('cost', '52.70'),
                                              ('cost_currency', 'RUB'),
                                              ('cpc', Decimal('2453.0000000')),
                                              ('cpm', Decimal('7222.0000'))]),
                                 OrderedDict([('date', '2018-04-04'),
                                              ('views', 12),
                                              ('clicks', 454),
                                              ('cost', '4.01'),
                                              ('cost_currency', 'RUB'),
                                              ('cpc', Decimal('2.4000000')),
                                              ('cpm', Decimal('3.0000'))])]

    def test_list_with_range_order(self):
        response = self.client.get(self.url_range_order)
        assert response.status_code == 200
        assert response.data == [OrderedDict([('date', '2020-03-01'),
                                              ('views', 102572),
                                              ('clicks', 4454),
                                              ('cost', '375.67'),
                                              ('cost_currency', 'RUB'),
                                              ('cpc', Decimal('545.4550000')),
                                              ('cpm', Decimal('3435.0000'))]),
                                 OrderedDict([('date', '2020-01-30'),
                                              ('views', 1028425),
                                              ('clicks', 445544),
                                              ('cost', '52.70'),
                                              ('cost_currency', 'RUB'),
                                              ('cpc', Decimal('2453.0000000')),
                                              ('cpm', Decimal('7222.0000'))]),
                                 OrderedDict([('date', '2018-04-04'),
                                              ('views', 12),
                                              ('clicks', 454),
                                              ('cost', '4.01'),
                                              ('cost_currency', 'RUB'),
                                              ('cpc', Decimal('2.4000000')),
                                              ('cpm', Decimal('3.0000'))])]

    def test_list_order(self):
        response = self.client.get(self.url_order)
        assert response.status_code == 200
        assert response.data == [OrderedDict([('date', '2021-04-10'),
                                              ('views', 102),
                                              ('clicks', 4564),
                                              ('cost', '32.67'),
                                              ('cost_currency', 'RUB'),
                                              ('cpc', Decimal('23.4500000')),
                                              ('cpm', Decimal('32.0000'))]),
                                 OrderedDict([('date', '2021-04-08'),
                                              ('views', 10),
                                              ('clicks', 458),
                                              ('cost', '3.67'),
                                              ('cost_currency', 'RUB'),
                                              ('cpc', Decimal('2.4500000')),
                                              ('cpm', Decimal('332.0000'))]),
                                 OrderedDict([('date', '2021-03-20'),
                                              ('views', 10205),
                                              ('clicks', 45654054),
                                              ('cost', '342.67'),
                                              ('cost_currency', 'RUB'),
                                              ('cpc', Decimal('238.4500000')),
                                              ('cpm', Decimal('3235.0000'))]),
                                 OrderedDict([('date', '2021-02-08'),
                                              ('views', 10255),
                                              ('clicks', 455564),
                                              ('cost', '321.67'),
                                              ('cost_currency', 'RUB'),
                                              ('cpc', Decimal('253.4500000')),
                                              ('cpm', Decimal('3232.0000'))]),
                                 OrderedDict([('date', '2020-03-01'),
                                              ('views', 102572),
                                              ('clicks', 4454),
                                              ('cost', '375.67'),
                                              ('cost_currency', 'RUB'),
                                              ('cpc', Decimal('545.4550000')),
                                              ('cpm', Decimal('3435.0000'))]),
                                 OrderedDict([('date', '2020-01-30'),
                                              ('views', 1028425),
                                              ('clicks', 445544),
                                              ('cost', '52.70'),
                                              ('cost_currency', 'RUB'),
                                              ('cpc', Decimal('2453.0000000')),
                                              ('cpm', Decimal('7222.0000'))]),
                                 OrderedDict([('date', '2018-04-04'),
                                              ('views', 12),
                                              ('clicks', 454),
                                              ('cost', '4.01'),
                                              ('cost_currency', 'RUB'),
                                              ('cpc', Decimal('2.4000000')),
                                              ('cpm', Decimal('3.0000'))])]

    def test_delete(self):
        response = self.client.delete(self.url)
        assert response.status_code == 204
        assert response.data == None

    def test_create(self):
        response = self.client.post(self.url, data=OrderedDict([('date', '2021-05-05'),
                                                                ('views', 10842),
                                                                ('clicks', 454564),
                                                                ('cost', '8.2')]))
        assert response.status_code == 201
        assert response.data == {'date': '2021-05-05',
                                 'views': 10842,
                                 'clicks': 454564,
                                 'cost': '8.20',
                                 'cost_currency': 'RUB',
                                 'cpc': 1.803926399802888e-05,
                                 'cpm': 0.7563180225050727}

    def test_bad_create(self):
        response = self.client.post(self.url, data=OrderedDict([('date', '2021-05-05'),
                                                                ('view', 10842),
                                                                ('clicks', 454564),
                                                                ('cost', '8.2')]))
        assert response.status_code == 400
        assert response.data == [ErrorDetail(string='Unable to calculate cpm', code='invalid')]
