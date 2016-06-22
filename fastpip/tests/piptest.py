# -*- coding: utf-8 -*-
from unittest import TestCase, expectedFailure
import os
import json
from functools import partial

from fastpip import pip

__all__ = ['TestFastPip', 'TestSimplePip']


class BaseTestPip(TestCase):

    __samples_cache__ = {}

    def setUp(self):
        super(BaseTestPip, self).setUp()
        self.sample_1 = lambda: self.load_sample('sample_1')
        self.sample_2 = lambda: self.load_sample('sample_2')
        self.sample_3 = lambda: self.load_sample('sample_3')

    def load_sample(self, name):
        if name not in self.__samples_cache__:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(current_dir, name)
            with open(filename) as handle:
                self.__samples_cache__[name] = json.load(handle)

        return self.__samples_cache__[name]

    def assertAlmostEqualCurves(self, curve_a, curve_b, msg=None):
        with_seven_places = lambda value: round(value, 7)
        curve_with_seven_places = lambda curve: [
            (with_seven_places(item[0]), with_seven_places(item[1]))
            for item in curve
        ]

        return self.assertEqual(
            curve_with_seven_places(curve_a), curve_with_seven_places(curve_b), msg=msg
        )

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
        data = [(item.get('x'), item.get('y')) for item in self.sample_1()]
        data_length = len(data)

        first_result = pip(data, data_length/10)
        for i in range(3):
            self.assertAlmostEqualCurves(
                self.pip(data, data_length/10), first_result, "Result has changed on iteration {}".format(i+1)
            )

    def test_behaviour_changes_according_to_the_distance_function_used_1(self):
        data = [(item.get('x'), item.get('y')) for item in self.sample_1()]

        vertical_result = pip(data, 300, distance='vertical')
        euclidean_result = pip(data, 300, distance='euclidean')
        self.assertNotEqual(vertical_result, euclidean_result)

    def test_behaviour_changes_according_to_the_distance_function_used_2(self):
        data = self.sample_2()

        vertical_result = pip(data, 300, distance='vertical')
        euclidean_result = pip(data, 300, distance='euclidean')
        self.assertNotEqual(vertical_result, euclidean_result)

    def test_behaviour_changes_according_to_the_distance_function_used_3(self):
        data = self.sample_3()

        vertical_result = pip(data, 300, distance='vertical')
        euclidean_result = pip(data, 300, distance='euclidean')
        self.assertNotEqual(vertical_result, euclidean_result)

    def test_behaviour_may_change_with_batch_or_stream_processing_using_vertical_distance_1(self):
        data = [(item.get('x'), item.get('y')) for item in self.sample_1()]

        stream_result = pip(data, 300, distance='vertical', stream_mode=True)
        batch_result = pip(data, 300, distance='vertical', stream_mode=False)
        self.assertNotEqual(stream_result, batch_result)

    def test_behaviour_may_change_with_batch_or_stream_processing_using_vertical_distance_2(self):
        data = self.sample_2()

        stream_result = pip(data, 300, distance='vertical', stream_mode=True)
        batch_result = pip(data, 300, distance='vertical', stream_mode=False)
        self.assertNotEqual(stream_result, batch_result)

    def test_behaviour_may_change_with_batch_or_stream_processing_using_vertical_distance_3(self):
        data = self.sample_3()

        stream_result = pip(data, 300, distance='vertical', stream_mode=True)
        batch_result = pip(data, 300, distance='vertical', stream_mode=False)
        self.assertNotEqual(stream_result, batch_result)

    def test_behaviour_may_change_with_batch_or_stream_processing_using_euclidean_distance_1(self):
        data = [(item.get('x'), item.get('y')) for item in self.sample_1()]

        stream_result = pip(data, 300, distance='euclidean', stream_mode=True)
        batch_result = pip(data, 300, distance='euclidean', stream_mode=False)
        self.assertNotEqual(stream_result, batch_result)

    def test_behaviour_may_change_with_batch_or_stream_processing_using_euclidean_distance_2(self):
        data = self.sample_2()

        stream_result = pip(data, 300, distance='euclidean', stream_mode=True)
        batch_result = pip(data, 300, distance='euclidean', stream_mode=False)
        self.assertNotEqual(stream_result, batch_result)

    def test_behaviour_may_change_with_batch_or_stream_processing_using_euclidean_distance_3(self):
        data = self.sample_3()

        stream_result = pip(data, 300, distance='euclidean', stream_mode=True)
        batch_result = pip(data, 300, distance='euclidean', stream_mode=False)
        self.assertNotEqual(stream_result, batch_result)


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
