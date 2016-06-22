# -*- coding: utf-8 -*-
from unittest import TestCase, expectedFailure

from fastpip import pip
from .test_data import test_data

__all__ = ['TestPip']


class TestPip(TestCase):

    def setUp(self):
        self.data = [(item.get('x'), item.get('y')) for item in test_data]
        self.data_length = len(self.data)

    def test_empty_input(self):
        data = []
        self.assertEqual(pip(data, 50), data)

    def test_nothing_is_changed_when_data_has_less_points_than_expected(self):
        data = list(zip(range(0, 10), 'qwertasdfg'))
        self.assertEqual(pip(data, 50), data)

    @expectedFailure
    def test_values_for_X_must_always_be_increasing(self):
        data = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0)]
        expected = [(0, 0), (4, 4), (0, 0)]
        self.assertEqual(pip(data, 3), expected)

    @expectedFailure
    def test_values_for_X_must_always_be_increasing_in_all_modes(self):
        data = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0)]
        expected = [(0, 0), (4, 4), (0, 0)]
        self.assertEqual(pip(data, 3, stream_mode=False), expected)

    def test_smallest_set_of_significant_points_in_stream_mode(self):
        data = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 3), (6, 2), (7, 1), (8, 0)]
        expected = [(0, 0), (4, 4), (8, 0)]
        self.assertEqual(pip(data, 3), expected)

    def test_smallest_set_of_significant_points_in_batch_mode(self):
        data = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 3), (6, 2), (7, 1), (8, 0)]
        expected = [(0, 0), (4, 4), (8, 0)]
        self.assertEqual(pip(data, 3, stream_mode=False), expected)

    def test_five_significant_points_in_stream_mode(self):
        data = [(0, 0), (1, 1), (2, 2), (3, 1), (4, 0), (5, 1), (6, 2), (7, 1), (8, 0)]
        expected = [(0, 0), (2, 2), (4, 0), (6, 2), (8, 0)]
        self.assertEqual(pip(data, 5), expected)

    def test_five_significant_points_in_batch_mode(self):
        data = [(0, 0), (1, 1), (2, 2), (3, 1), (4, 0), (5, 1), (6, 2), (7, 1), (8, 0)]
        expected = [(0, 0), (2, 2), (4, 0), (6, 2), (8, 0)]
        self.assertEqual(pip(data, 5, stream_mode=False), expected)

    def test_result_should_always_be_the_same_for_a_given_input(self):
        first_result = pip(self.data, self.data_length/10)
        for i in range(5):
            self.assertEqual(
                pip(self.data, self.data_length/10), first_result, "Result has changed on iteration {}".format(i+1)
            )
