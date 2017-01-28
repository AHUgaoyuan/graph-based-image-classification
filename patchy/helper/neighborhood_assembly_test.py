import tensorflow as tf

from .neighborhood_assembly import neighborhoods_weights_to_root,\
                                   neighborhoods_nearest_scanline


class NeighborhoodAssemblyTest(tf.test.TestCase):

    def test_neighborhoods_by_weight(self):
        sequence = tf.constant([0, 2, 5, -1])

        adjacency = tf.constant([
            [0, 1, 4, 0, 0, 0, 0],
            [1, 0, 2, 0, 5, 0, 0],
            [4, 2, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 9, 2],
            [0, 5, 0, 0, 0, 3, 0],
            [0, 0, 0, 9, 3, 0, 0],
            [0, 0, 0, 2, 0, 0, 0],
        ])

        size = 3

        expected = [
            [0, 1, 2],
            [2, 3, 1],
            [5, 4, 1],
            [-1, -1, -1],
        ]

        with self.test_session() as sess:
            neighborhoods = neighborhoods_weights_to_root(
                adjacency, sequence, size)
            self.assertAllEqual(neighborhoods.eval(), expected)

        sequence = tf.constant([0, 1, 2, 3])

        adjacency = tf.constant([
            [0, 1, 3, 0],
            [1, 0, 0, 11],
            [3, 0, 0, 5],
            [0, 11, 5, 0],
        ])

        size = 5

        expected = [
            [0, 1, 2, 3, -1],
            [1, 0, 2, 3, -1],
            [2, 0, 1, 3, -1],
            [3, 2, 0, 1, -1],
        ]

        with self.test_session() as sess:
            neighborhoods = neighborhoods_weights_to_root(
                adjacency, sequence, size)
            self.assertAllEqual(neighborhoods.eval(), expected)

    def test_nearest_scanline(self):
        sequence = tf.constant([0, 2, 5, -1])

        adjacency = tf.constant([
            [0, 1, 4, 0, 0, 0, 0],
            [1, 0, 2, 0, 5, 0, 0],
            [4, 2, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 9, 2],
            [0, 5, 0, 0, 0, 3, 0],
            [0, 0, 0, 9, 3, 0, 0],
            [0, 0, 0, 2, 0, 0, 0],
        ])

        size = 3

        expected = [
            [0, 1, 2],
            [1, 2, 3],
            [1, 4, 5],
            [-1, -1, -1],
        ]

        with self.test_session() as sess:
            neighborhoods = neighborhoods_nearest_scanline(
                adjacency, sequence, size)
            self.assertAllEqual(neighborhoods.eval(), expected)
