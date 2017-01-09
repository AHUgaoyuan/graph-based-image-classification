import os
import sys

import tensorflow as tf
import skimage.io as io
from xml.dom.minidom import parse

from .download import maybe_download_and_extract
from .io import get_example

DATA_URL = 'http://host.robots.ox.ac.uk/pascal/VOC/voc2012/'\
           'VOCtrainval_11-May-2012.tar'


def _get_first_tag_text(dom, tag):
    return dom.getElementsByTagName(tag)[0].firstChild.nodeValue


class PascalVOC():
    def __init__(self, data_dir='/tmp/pascal_voc_data', max_height=224,
                 max_width=224, min_object_height=50, min_object_width=50):

        self._data_dir = data_dir
        self._max_height = max_height
        self._max_width = max_width
        self._min_object_height = min_object_height
        self._min_object_width = min_object_width

        maybe_download_and_extract(DATA_URL, data_dir)

        extracted_dir = os.path.join(data_dir, 'VOCdevkit', 'VOC2012')
        image_sets_dir = os.path.join(extracted_dir, 'ImageSets', 'Main')

        self._num_examples_per_epoch_for_train = self._write_set(
            os.path.join(image_sets_dir, 'train.txt'),
            os.path.join(data_dir, 'train.tfrecords'))
        self._num_examples_per_epoch_for_eval = self._write_set(
            os.path.join(image_sets_dir, 'val.txt'),
            os.path.join(data_dir, 'eval.tfrecords'))

    def _write_set(self, input_path, filename, show_progress=True):
        writer = tf.python_io.TFRecordWriter(filename)

        with open(input_path) as f:
            lines = f.readlines()

            length = len(lines)
            count = 0
            bypassed = 0
            cutted = 0
            smaller = 0

            for i, line in enumerate(lines):
                example_name = line.strip('\n')
                stats = self._write_example(writer, example_name)
                count += stats['count']
                bypassed += stats['bypassed']
                cutted += stats['cutted']
                smaller += stats['smaller']

                if show_progress:
                    sys.stdout.write(
                        '\r>> Extracting objects to {} {:.1f}%'
                        .format(filename, 100.0 * i / length))
                    sys.stdout.flush()

            if show_progress:
                print()

            print(' '.join([
                'Extracted {} objects'.format(count),
                'from {} images'.format(length),
                '({} bypassed,'.format(bypassed),
                '{} with a dissected bounding box,'.format(cutted),
                '{} with a smaller image shape)'.format(smaller),
            ]))

        writer.close()
        return count

    def _write_example(self, writer, example_name):
        extracted_dir = os.path.join(self._data_dir, 'VOCdevkit', 'VOC2012')

        annotation_path = os.path.join(
            extracted_dir, 'Annotations', '{}.xml'.format(example_name))
        image_path = os.path.join(
            extracted_dir, 'JPEGImages', '{}.jpg'.format(example_name))

        annotation = parse(annotation_path)
        image = io.imread(image_path)

        count = 0
        bypassed = 0
        cutted = 0
        smaller = 0

        # Iterate over all bounding boxes.
        for obj in annotation.getElementsByTagName('object'):
            cropped_image, bb_height, bb_width = self._crop_image(image, obj)

            if cropped_image is None:
                bypassed += 1
                continue

            count += 1

            # Check whether the bounding box is cutted.
            if cropped_image.shape[0] < bb_height or\
               cropped_image.shape[1] < bb_width:
                cutted += 1

            # Check whether the resulting image shape is smaller than the
            # specified max height/width.
            if cropped_image.shape[0] < self._max_height or\
               cropped_image.shape[1] < self._max_width:
                smaller += 1

            label_name = _get_first_tag_text(obj, 'name')

            example = get_example(cropped_image, self._get_label(label_name))
            writer.write(example.SerializeToString())

        return {
            'count': count,
            'bypassed': bypassed,
            'cutted': cutted,
            'smaller': smaller,
        }

    def _get_label(self, name):
        label = self.classes.index(name)

        if label == -1:
            raise ValueError('Couldn\'t find label name in defined classes.')

        return label

    def _crop_image(self, image, obj):
        top = int(_get_first_tag_text(obj, 'ymin'))
        height = int(_get_first_tag_text(obj, 'ymax')) - top
        left = int(_get_first_tag_text(obj, 'xmin'))
        width = int(_get_first_tag_text(obj, 'xmax')) - left

        # Check whether the bounding box is too small. If so, we discard the
        # object.
        if height < self._min_object_height or width < self._min_object_width:
            return None, height, width

        # Crop the image from the center of the bounding box.
        crop_top = max(top + height // 2 - self._max_height // 2, 0)
        crop_left = max(left + width // 2 - self._max_width // 2, 0)

        # We need to adjust the variables if the object is at the right or the
        # bottom of the image, so that we can get a full max height/width
        # cropping.
        crop_top = min(crop_top, max(image.shape[0] - self._max_height, 0))
        crop_left = min(crop_left, max(image.shape[1] - self._max_width, 0))

        crop_bottom = min(crop_top + self._max_height, image.shape[0])
        crop_right = min(crop_left + self._max_width, image.shape[1])

        return image[crop_top:crop_bottom, crop_left:crop_right], height, width

    def name(self):
        """The name of the dataset for pretty printing.

        Returns:
            A String with the name of the dataset.
        """
        return 'PascalVOC'

    @property
    def data_dir(self):
        return self._data_dir

    @property
    def train_filenames(self):
        return [os.path.join(self.data_dir, 'train.tfrecords')]

    @property
    def eval_filenames(self):
        return [os.path.join(self.data_dir, 'eval.tfrecords')]

    @property
    def classes(self):
        return ['person', 'bird', 'cat', 'cow', 'dog', 'horse', 'sheep',
                'aeroplane', 'bicycle', 'boat', 'bus', 'car', 'motorbike',
                'train', 'bottle', 'chair', 'diningtable', 'pottedplant',
                'sofa', 'tvmonitor']

    @property
    def num_examples_per_epoch_for_train(self):
        return self._num_examples_per_epoch_for_train

    @property
    def num_examples_per_epoch_for_eval(self):
        return self._num_examples_per_epoch_for_eval

    def read(self, filename_queue):
        pass

    def distort_for_train(self, record):
        return record

    def distort_for_eval(self, record):
        return record
