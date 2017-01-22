import tensorflow as tf

from .inputs import inputs


def iterator(dataset, eval_data, batch_size=1, scale_inputs=1.0,
             distort_inputs=False, zero_mean_inputs=False, num_epochs=1,
             shuffle=False):

    """Returns a function which iterates over a dataset in batches.

    Args:
        dataset: The dataset.
        eval_data: Boolean indicating if one should use the train or eval data
          set.
        batch_size: Number of data per batch (optional).
        scale_inputs: Float defining the scaling to use for resizing the
          records data (optional).
        distort_inputs: Boolean whether to distort the inputs (optional).
        zero_mean_inputs: Boolean indicating if one should linearly scales the
          records data to have zero mean and unit norm (optional).
        num_epochs: Number indicating the maximal number of epoch iterations
          (optional).
        shuffle: Boolean indiciating if one wants to shuffle the inputs
          (optional).

    Returns:
        A function that iterates over the dataset.
    """

    def _iterate(each, before=None, done=None):
        """Iterates over a dataset defined by the iterator.

        Args:
            each: Function that is called for every passed batch.
                output_batch: The output_batch computed by the session.
                index: The currently passed number of records.
                last_index: The maximal number of records to iterate. Can be
                  None.
            before: Function that is called before running the iterator. Its
              return value is passed as the operation to run (optional). If
              None, the data_batch and label_batch gets passed to the session.
                data_batch: The data batch tensor.
                label_batch: The label batch tensor.
            done: Function that is called after running the iterator
              (optional).
                index: The passed number of records.
                last_index: The maximal number of records to iterate. Can be
                  None.
        """

        index = 0

        if not eval_data:
            num_examples_per_epoch = dataset.num_examples_per_epoch_for_train
        else:
            num_examples_per_epoch = dataset.num_examples_per_epoch_for_eval

        if num_epochs is not None:
            last_index = num_epochs * num_examples_per_epoch
        else:
            last_index = None

        # Build up a new graph.
        with tf.Graph().as_default():
            data_batch, label_batch = inputs(dataset, eval_data=eval_data,
                                             batch_size=batch_size,
                                             scale_inputs=scale_inputs,
                                             distort_inputs=distort_inputs,
                                             zero_mean_inputs=zero_mean_inputs,
                                             num_epochs=num_epochs,
                                             shuffle=shuffle)

            if batch_size == 1:
                # Remove the first dimension, because we only consider batch
                # sizes of one.
                data_batch = tf.squeeze(data_batch, squeeze_dims=[0])
                label_batch = tf.squeeze(label_batch, squeeze_dims=[0])

            # Customize input batch with the optional before callback.
            if before is None:
                input_batch = [data_batch, label_batch]
            else:
                input_batch = before(data_batch, label_batch)

            try:
                # Run a controlled tensorflow session.
                with tf.train.MonitoredTrainingSession(
                        save_checkpoint_secs=None,
                        save_summaries_steps=None,
                        ) as monitored_session:
                    while not monitored_session.should_stop():
                        index += batch_size

                        # Index can't be greater than the last index.
                        if last_index is not None:
                            index = min(index, last_index)

                        output_batch = monitored_session.run(input_batch)

                        # Call the callback for each computed output batch.
                        each(output_batch, index, last_index)

            except KeyboardInterrupt:
                pass

            finally:
                # Call the optional done callback.
                if done is not None:
                    done(index, last_index)

    return _iterate
