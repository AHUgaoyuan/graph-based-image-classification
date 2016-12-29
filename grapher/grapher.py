import abc
import six


@six.add_metaclass(abc.ABCMeta)
class Grapher(object):

    @abc.abstractmethod
    def create_graph(self, data):
        """Returns nodes and adjacent tensors."""
        pass
