from __future__ import division

import tensorflow as tf
import numpy as np

from .adjacency import adjacency_unweighted, adjacency_euclidean_distance


class AdjacencyTest(tf.test.TestCase):

    def test_adjacency_unweighted(self):
        segmentation = tf.constant([
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [2, 0, 0, 3],
            [2, 2, 3, 3],
        ], dtype=tf.int32)

        expected = [
            [0, 1, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 0],
        ]

        with self.test_session() as sess:
            adjacency_matrix = adjacency_unweighted(segmentation)
            self.assertAllEqual(adjacency_matrix.eval(), expected)

    def test_adjacency_euclidean_distance(self):
        segmentation = tf.constant([
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [2, 0, 0, 3],
            [2, 2, 3, 3],
        ], dtype=tf.int32)

        c = np.array([
            [(0+1+0+1+2+1+2)/7, (0+1+0+1+2+1+2)/7],
            [(0+0+1)/3, (2+3+3)/3],
            [(2+3+3)/3, (0+0+1)/3],
            [(3+2+3)/3, (3+2+3)/3],
        ], dtype=np.float32)

        def _distance(centroid, index1, index2):
            return np.linalg.norm(centroid[index1] - centroid[index2])

        expected = [
            [0, _distance(c, 0, 1), _distance(c, 0, 2), _distance(c, 0, 3)],
            [_distance(c, 1, 0), 0, 0, _distance(c, 1, 3)],
            [_distance(c, 2, 0), 0, 0, _distance(c, 2, 3)],
            [_distance(c, 3, 0), _distance(c, 3, 1), _distance(c, 3, 2), 0],
        ]

        with self.test_session() as sess:
            adjacency_matrix = adjacency_euclidean_distance(segmentation)
            self.assertAllEqual(adjacency_matrix.eval(), expected)
