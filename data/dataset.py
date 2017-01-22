import abc
import six

import tensorflow as tf

from .helper.record import Record


SHOW_PROGRESS = True


@six.add_metaclass(abc.ABCMeta)
class DataSet():
    """Abstract class for defining a dataset interface."""

    def __init__(self, data_dir, show_progress=SHOW_PROGRESS):
        """Creates a dataset.

        Args:
            data_dir: The path to the directory where the dataset is stored.
            show_progress: Show a pretty progress bar for dataset computations
              (optional).
        """

        self._data_dir = data_dir
        self._show_progress = show_progress

    @classmethod
    def create(cls, json):
        """Creates a dataset via a json file.

        Args:
            json: The json object.

        Returns:
            The dataset.
        """

        return cls(
            json['data_dir'] if 'data_dir' in json else None,
            json['show_progress'] if 'show_progress' in json
            else SHOW_PROGRESS)

    @property
    def data_dir(self):
        """The path to the directory where the dataset is stored.

        Returns:
            A string with the path to the dataset.
        """

        return self._data_dir

    @property
    @abc.abstractmethod
    def train_filenames(self):
        """The filenames of the training batches from the dataset.

        Returns:
             A list of absolute filenames.
        """

        pass

    @property
    @abc.abstractmethod
    def eval_filenames(self):
        """The filenames of the evaluating batches from the dataset.

        Returns:
             A list of absolute filenames.
        """

        pass

    @property
    @abc.abstractmethod
    def labels(self):
        """The ordered labels of the dataset.

        Returns:
            A list of labels.
        """

        pass

    @property
    def num_labels(self):
        """The number of labels of the dataset.

        Return:
            A number.
        """

        return len(self.labels)

    def label_index(self, label_name):
        """The index of the given label name.

        Args:
            label: The label name.

        Returns:
            A number.

        Raises:
            ValueError: If the label cannot be found in the labels.
        """

        index = self.labels.index(label_name)

        if index == -1:
            raise ValueError('{} is no valid label name.'.format(label_name))

        return index

    def label_name(self, index):
        """The label name of the given label index.

        Args:
            index: The label index:

        Returns:
            A string describing the label.

        Raises:
            ValueError: If the label of the index cannot be found in the
              labels.
        """

        if 0 <= index < self.num_labels:
            return self.labels[index]

        raise ValueError('{} is no valid label index.'.format(index))

    @property
    @abc.abstractmethod
    def num_examples_per_epoch_for_train(self):
        """The number of examples per epoch for training the dataset.

        Returns:
            A number.
        """

        pass

    @property
    @abc.abstractmethod
    def num_examples_per_epoch_for_eval(self):
        """The number of examples per epoch for evaluating the dataset.

        Returns:
            A number.
        """

        pass

    @abc.abstractmethod
    def read(self, filename_queue):
        """Reads and parses examples from data files.

        Args:
            filename_queue: A queue of strings with the filenames to read from.

        Returns:
            A record object.
        """

        pass

    def distort_for_train(self, record):
        """Applies random distortions for training to a record.

        Args:
            record: The record before applying distortions.

        Returns:
            A new record object of the passed record after applying
            distortions.
        """

        return record

    def distort_for_eval(self, record):
        """Applies distortions for evaluation to a record.

        Args:
            record: The record before applying distortions.

        Returns:
            A new record object of the passed record after applying
            distortions.
        """

        return record
