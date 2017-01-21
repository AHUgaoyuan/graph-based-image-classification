import tensorflow as tf
import numpy as np

from data import DataSet
from data import iterator
from data import read_tfrecord

from .feature_extraction import feature_extraction


class SlicGrid(DataSet):

    def __init__(self, dataset, slic_algorithm, max_num_epochs=1,
                 show_progress=True):

        super().__init__(dataset.data_dir, show_progress)

        self._dataset = dataset

        iterate_train = iterator(
            dataset, eval_data=False, batch_size=1, distort_inputs=True,
            scale_inputs=False, num_epochs=max_num_epochs, shuffle=True)

        iterate_eval = iterator(
            dataset, eval_data=True, batch_size=1, distort_inputs=True,
            scale_inputs=False, num_epochs=1, shuffle=False)

        def _before(image_batch, label_batch):
            # Remove the first dimension, because we only consider batch sizes
            # of one.
            image = tf.squeeze(image_batch, squeeze_dims=[0])
            label = tf.squeeze(label_batch, squeeze_dims=[0])

            segmentation = slic_algorithm(image)
            return segmentation
            # Cast image to uint8, so
            return [image, label]
            # return [tf.cast(image, tf.uint8), label]

        def _each(output, index, last_index):
            # Get the image and the label name from the output of the session.
            image = output
            print(np.unique(image).size)

            # a = image.flatten()
            # indexes = np.unique(a, return_index=True)[1]
            # a = [a[index] for index in sorted(indexes)]
            # print(a)

            # label_name = dataset.label_name(output[1])

            # # Save the image in the label named subdirectory and name it
            # # incrementally.
            # image_names[label_name] += 1
            # image_name = '{}.png'.format(image_names[label_name])
            # image_path = os.path.join(images_dir, label_name, image_name)

            # imsave(image_path, image)

            # sys.stdout.write(
            #     '\r>> Saving images to {} {:.1f}%'
            #     .format(images_dir, 100.0 * index / last_index))
            # sys.stdout.flush()

        def _done(index, last_index):
            pass

        # Run through each single batch.
        iterate_train(_each, _before, _done)

    @property
    def train_filenames(self):
        pass

    @property
    def eval_filenames(self):
        pass

    @property
    def labels(self):
        return self._dataset.labels

    @property
    def num_examples_per_epoch_for_train(self):
        return self._dataset.num_examples_per_epoch_for_train

    @property
    def num_examples_per_epoch_for_eval(self):
        return self._dataset.num_examples_per_epoch_for_eval

    def read(self, filename_queue):
        return read_tfrecord(filename_queue, [HEIGHT, WIDTH, 3])