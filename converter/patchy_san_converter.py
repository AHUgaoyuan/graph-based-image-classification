import tensorflow as tf

from converter import Converter
from .patchy_san.labeling import labelings
from .patchy_san.node_sequence import node_sequence
from .patchy_san.neighborhood_assembly import neighborhoods_assembly
from .patchy_san.receptive_field import receptive_fields


class PatchySan(Converter):

    def __init__(self, grapher, num_nodes, node_labeling, node_stride,
                 neighborhood_size, neighborhood_labeling):

        if node_labeling not in labelings:
            raise ValueError(
                'Could not find labeling "{}".'.format(node_labeling))

        if neighborhood_labeling not in labelings:
            raise ValueError(
                'Could not find labeling "{}".'.format(neighborhood_labeling))

        self._grapher = grapher
        self._num_nodes = num_nodes
        self._node_labeling = node_labeling
        self._node_stride = node_stride
        self._neighborhood_size = neighborhood_size
        self._neighborhood_labeling = neighborhood_labeling

    @property
    def shape(self):
        return [
            self._num_nodes,
            self._neighborhood_size,
            self._grapher.num_node_channels,
        ]

    def convert(self, data):
        nodes, adjacent = self._grapher.create_graph(data)

        # Test speed.
        result = tf.strided_slice(nodes, [0], [self._num_nodes], [1])
        result = tf.map_fn(lambda x: tf.random_normal([self._neighborhood_size, 8]), result)
        return result

        # TODO
        sequence = labelings[self._node_labeling](adjacent)
        sequence = tf.cast(sequence, tf.float32)
        result = tf.strided_slice(sequence, [0], [self._num_nodes], [1])
        result = tf.map_fn(lambda x: tf.random_normal([self._neighborhood_size, 8]), result)
        return result
        # sequence = node_sequence(sequence, self._num_nodes, self._node_stride)

        # neighborhoods = neighborhoods_assembly(
        #     sequence, adjacent, self._neighborhood_size,
        #     labelings[self._neighborhood_labeling])

        # return receptive_fields(neighborhoods, nodes,
        #                         self._grapher.node_channels_length)