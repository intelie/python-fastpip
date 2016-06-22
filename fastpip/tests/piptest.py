# -*- coding: utf-8 -*-
from unittest import TestCase, expectedFailure
from functools import partial

from fastpip import pip
from .test_data import test_data

__all__ = ['TestFastPip', 'TestSimplePip']


class BaseTestPip(TestCase):

    def setUp(self):
        self.data = [(item.get('x'), item.get('y')) for item in test_data]
        self.data_length = len(self.data)

    def test_empty_input(self):
        data = []
        self.assertEqual(self.pip(data, 50), data)

    def test_nothing_is_changed_when_data_has_less_points_than_expected(self):
        data = list(zip(range(0, 10), 'qwertasdfg'))
        self.assertEqual(self.pip(data, 50), data)

    @expectedFailure
    def test_values_for_X_must_always_be_increasing(self):
        data = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0)]
        expected = [(0, 0), (4, 4), (0, 0)]
        self.assertEqual(self.pip(data, 3), expected)

    def test_smallest_set_of_significant_points(self):
        data = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 3), (6, 2), (7, 1), (8, 0)]
        expected = [(0, 0), (4, 4), (8, 0)]
        self.assertEqual(self.pip(data, 3), expected)

    def test_four_significant_points(self):
        data = [(0, 0), (1, 1), (2, 0), (3, -1), (4, -2), (5, -3), (6, -2), (7, -1), (8, 0)]
        expected = [(0, 0), (1, 1), (5, -3), (8, 0)]
        self.assertEqual(self.pip(data, 4), expected)

    def test_five_significant_points(self):
        data = [(0, 0), (1, 3), (2, 2), (3, 1), (4, 0), (5, 1), (6, 2), (7, 3), (8, 0)]
        expected = [(0, 0), (1, 3), (4, 0), (7, 3), (8, 0)]
        self.assertEqual(self.pip(data, 5), expected)

    def test_result_should_always_be_the_same_for_a_given_input(self):
        first_result = pip(self.data, self.data_length/10)
        for i in range(3):
            self.assertEqual(
                self.pip(self.data, self.data_length/10), first_result, "Result has changed on iteration {}".format(i+1)
            )


class TestFastPip(BaseTestPip):

    def setUp(self):
        super(TestFastPip, self).setUp()
        self.pip = partial(pip, fast=True)

    @expectedFailure
    def test_values_for_X_must_always_be_increasing_in_all_modes(self):
        data = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0)]
        expected = [(0, 0), (4, 4), (0, 0)]
        self.assertEqual(self.pip(data, 3, stream_mode=False), expected)

    def test_smallest_set_of_significant_points_in_batch_mode(self):
        data = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 3), (6, 2), (7, 1), (8, 0)]
        expected = [(0, 0), (4, 4), (8, 0)]
        self.assertEqual(self.pip(data, 3, stream_mode=False), expected)

    def test_four_significant_points_in_batch_mode(self):
        data = [(0, 0), (1, 1), (2, 0), (3, -1), (4, -2), (5, -3), (6, -2), (7, -1), (8, 0)]
        expected = [(0, 0), (1, 1), (5, -3), (8, 0)]
        self.assertEqual(self.pip(data, 4, stream_mode=False), expected)

    def test_five_significant_points_in_batch_mode(self):
        data = [(0, 0), (1, 3), (2, 2), (3, 1), (4, 0), (5, 1), (6, 2), (7, 3), (8, 0)]
        expected = [(0, 0), (1, 3), (4, 0), (7, 3), (8, 0)]
        self.assertEqual(self.pip(data, 5, stream_mode=False), expected)


class TestSimplePip(BaseTestPip):

    def setUp(self):
        super(TestSimplePip, self).setUp()
        self.pip = partial(pip, fast=False)
