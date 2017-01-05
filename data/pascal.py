import os

import tensorflow as tf
import skimage.io as io
from xml.dom.minidom import parse

from .download import maybe_download_and_extract

DATA_URL = 'http://host.robots.ox.ac.uk/pascal/VOC/voc2012/'\
           'VOCtrainval_11-May-2012.tar'


class PascalVOC():
    def __init__(self, data_dir):
        maybe_download_and_extract(DATA_URL, data_dir)

        extracted_dir = os.path.join(data_dir, 'VOCdevkit', 'VOC2012')

        train_files = tf.train.match_filenames_once(
            os.path.join(extracted_dir, 'ImageSets', 'Main', 'train.txt'))
        eval_files = tf.train.match_filenames_once(
            os.path.join(extracted_dir, 'ImageSets', 'Main', 'val.txt'))

        self._read_example_name(train_files, base_dir=extracted_dir)
        self._read_example_name(eval_files, base_dir=extracted_dir)
        # data_batch, label_batch = tf.train.batch(
        #     [data, label],
        #     batch_size=batch_size,
        #     num_threads=num_threads,
        #     capacity=capacity)

    def _read_example_name(files, base_dir):
        filename_queue = tf.train.string_input_producer(
            train_file, num_epochs=1)

        reader = tf.TextLineReader()
        _, value = reader.read(filename_queue)

        return os.path.join(base_dir, 'Annotations', '{}.xml'.format(value)),
        os.path.join(base_dir, 'JPEGImages', '{}.jpg'.format(value))

    def _read_annotation(name, ba):
        name = '{}.xml'.format(name)

        filename_queue = tf.train.string_input_producer(
            os.path.join(base_dir, 'Annotations', name), num_epochs=1)


                

        # annotation_filenames = tf.train.match_filenames_once(
        #     os.path.join(extracted_dir, 'Annotatoions', '*.xml'))

        # filename_queue = tf.train.string_input_producer(
        #     annotation_filenames, num_epochs=1)

        # reader = tf.WholeFileReader()
        # _, value = reader.read(filename_queue)

        # annotation_paths = [os.path.join(extracted_dir, 'Annotations', '2007_000033.xml'),
        #                     os.path.join(extracted_dir, 'Annotations', '2007_000027.xml'),
        #                     os.path.join(extracted_dir, 'Annotations', '2007_001175.xml')]

        # for annotation_path in annotation_paths:
        #     annotation_name = annotation_path.split('/')[-1]
        #     image_name = '{}.jpg'.format(annotation_name.split('.')[0])
        #     image_path = os.path.join(extracted_dir, 'JPEGImages', image_name)

        #     image = io.imread(image_path)

        #     print(annotation_path)
        #     xmldoc = parse(annotation_path)
        #     objects = xmldoc.getElementsByTagName('object')

        #     # Find the biggest bounding box to specify one label.
        #     area = 0
        #     label = ''
        #     for obj in objects:
        #         xmin = int(obj.getElementsByTagName('xmin')[0].firstChild.nodeValue)
        #         xmax = int(obj.getElementsByTagName('xmax')[0].firstChild.nodeValue)
        #         ymin = int(obj.getElementsByTagName('ymin')[0].firstChild.nodeValue)
        #         ymax = int(obj.getElementsByTagName('ymax')[0].firstChild.nodeValue)

        #         a = (ymax - ymin) * (xmax - xmin)

        #         if a >= area:
        #             area = a
        #             label = obj.getElementsByTagName('name')[0].firstChild.nodeValue

        #     print(label)
        #     # TODO save to tfrecord

    def name(self):
        """The name of the dataset for pretty printing.

        Returns:
            A String with the name of the dataset.
        """
        return 'PascalVOC'

    @property
    def data_dir(self):
        return ''

    @property
    def train_filenames(self):
        return ''

    @property
    def eval_filenames(self):
        return ''

    @property
    def classes(self):
        return ['person', 'bird', 'cat', 'cow', 'dog', 'horse', 'sheep',
                'aeroplane', 'bicycle', 'boat', 'bus', 'car', 'motorbike',
                'train', 'bottle', 'chair', 'diningtable', 'pottedplant',
                'sofa', 'tvmonitor']

    def _train_filename_classes(self):
        def _train(filename):
            return '{}_train.txt'.format(filename)

        def _trainval(filename):
            return '{}_trainval.txt'.format(filename)

        return [f(label) for label in self.classes
                for f in (_train, _trainval)]

    def _eval_filename_classes(self):
        def _val(filename):
            return '{}_val.txt'.format(filename)

        return [_val(label) for label in self.classes]

    @property
    def num_examples_per_epoch_for_train(self):
        pass

    @property
    def num_examples_per_epoch_for_eval(self):
        pass

    def read(self, filename_queue):
        pass

    def distort_for_train(self, record):
        return record

    def distort_for_eval(self, record):
        return record
