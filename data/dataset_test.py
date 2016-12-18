from nose.tools import *
from numpy import testing as np_test

import numpy as np

from .dataset import Dataset


def test_create_dataset():
    batch = {
        'data': np.array([
            [1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2],
            [3, 3, 3, 3, 3],
            [4, 4, 4, 4, 4],
            [5, 5, 5, 5, 5],
        ]),
        'labels': np.array([
            1, 2, 3, 4, 5
        ]),
    }

    dataset = Dataset([batch, batch])

    assert_equals(dataset.num_examples, 10)
    assert_equals(dataset.data.shape, (10, 5))
    assert_equals(dataset.labels.shape, (10,))

    np_test.assert_array_equal(dataset.data[0], [1, 1, 1, 1, 1])
    np_test.assert_array_equal(dataset.data[1], [2, 2, 2, 2, 2])
    np_test.assert_array_equal(dataset.data[2], [3, 3, 3, 3, 3])
    np_test.assert_array_equal(dataset.data[3], [4, 4, 4, 4, 4])
    np_test.assert_array_equal(dataset.data[4], [5, 5, 5, 5, 5])
    np_test.assert_array_equal(dataset.data[5], [1, 1, 1, 1, 1])
    np_test.assert_array_equal(dataset.data[6], [2, 2, 2, 2, 2])
    np_test.assert_array_equal(dataset.data[7], [3, 3, 3, 3, 3])
    np_test.assert_array_equal(dataset.data[8], [4, 4, 4, 4, 4])
    np_test.assert_array_equal(dataset.data[9], [5, 5, 5, 5, 5])

    np_test.assert_array_equal(dataset.labels, [1, 2, 3, 4, 5, 1, 2, 3, 4, 5])


def test_next_batch():
    batch = {
        'data': np.array([
            [1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2],
            [3, 3, 3, 3, 3],
            [4, 4, 4, 4, 4],
            [5, 5, 5, 5, 5],
        ]),
        'labels': np.array([
            1, 2, 3, 4, 5
        ]),
    }

    dataset = Dataset([batch])

    data, labels = dataset.next_batch(2)

    assert_equals(len(data), 2)
    assert_equals(len(labels), 2)

    np_test.assert_array_equal(data[0], [1, 1, 1, 1, 1])
    np_test.assert_array_equal(data[1], [2, 2, 2, 2, 2])
    np_test.assert_array_equal(labels, [1, 2])

    data, labels = dataset.next_batch(3)

    assert_equals(len(data), 3)
    assert_equals(len(labels), 3)

    np_test.assert_array_equal(data[0], [3, 3, 3, 3, 3])
    np_test.assert_array_equal(data[1], [4, 4, 4, 4, 4])
    np_test.assert_array_equal(data[2], [5, 5, 5, 5, 5])
    np_test.assert_array_equal(labels, [3, 4, 5])

    data, labels = dataset.next_batch(3)

    assert_equals(len(data), 3)
    assert_equals(len(labels), 3)

    # The resulting data and labels are random, we cannot test them.
