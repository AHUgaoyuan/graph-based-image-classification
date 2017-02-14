import tensorflow as tf

from data import inputs

from .inference import inference
from .model import train_step, cal_loss, cal_accuracy
from .hooks import hooks


BATCH_SIZE = 128
LAST_STEP = 20000

LEARNING_RATE = 0.1
EPSILON = 1.0
BETA_1 = 0.9
BETA_2 = 0.999
DROPOUT = 0.5

SCALE_INPUTS = 1
DISTORT_INPUTS = True
ZERO_MEAN_INPUTS = True

DISPLAY_STEP = 10
SAVE_CHECKPOINT_SECS = 60*60
SAVE_SUMMARIES_STEPS = 100


def train(dataset, network, checkpoint_dir, batch_size=BATCH_SIZE,
          last_step=LAST_STEP, learning_rate=LEARNING_RATE, epsilon=EPSILON,
          beta1=BETA_1, beta2=BETA_2, dropout=DROPOUT,
          scale_inputs=SCALE_INPUTS, distort_inputs=DISTORT_INPUTS,
          zero_mean_inputs=ZERO_MEAN_INPUTS, display_step=DISPLAY_STEP,
          save_checkpoint_secs=SAVE_CHECKPOINT_SECS,
          save_summaries_steps=SAVE_SUMMARIES_STEPS):

    if not tf.gfile.Exists(checkpoint_dir):
        tf.gfile.MakeDirs(checkpoint_dir)

    with tf.Graph().as_default():

        ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
        global_step_init = -1
        if ckpt and ckpt.model_checkpoint_path:
            global_step_init = int(
                ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1])
            global_step = tf.Variable(global_step_init, name='global_step',
                                      dtype=tf.int64, trainable=False)
        else:
            global_step = tf.contrib.framework.get_or_create_global_step()

        data, labels = inputs(dataset, False, batch_size, scale_inputs,
                              distort_inputs, zero_mean_inputs, shuffle=True)

        keep_prob = tf.placeholder(tf.float32)
        logits = inference(data, network, keep_prob)
        loss = cal_loss(logits, labels)
        acc = cal_accuracy(logits, labels)

        train_op = train_step(
            loss, global_step, learning_rate, beta1, beta2, epsilon)

        try:
            with tf.train.MonitoredTrainingSession(
                    checkpoint_dir=checkpoint_dir,
                    save_checkpoint_secs=save_checkpoint_secs,
                    save_summaries_steps=save_summaries_steps,
                    hooks=hooks(display_step, last_step, batch_size, loss, acc)
                    ) as monitored_session:
                while not monitored_session.should_stop():
                    monitored_session.run(train_op,
                                          feed_dict={keep_prob: dropout})

        except KeyboardInterrupt:
            pass


def train_from_config(dataset, config, display_step=DISPLAY_STEP,
                      save_checkpoint_secs=SAVE_CHECKPOINT_SECS,
                      save_summaries_steps=SAVE_SUMMARIES_STEPS):

    train(dataset,
          config['network'],
          config['checkpoint_dir'],
          config.get('batch_size', BATCH_SIZE),
          config.get('last_step', LAST_STEP),
          config.get('learning_rate', LEARNING_RATE),
          config.get('epsilon', EPSILON),
          config.get('beta1', BETA_1),
          config.get('beta2', BETA_2),
          config.get('dropout', DROPOUT),
          config.get('scale_inputs', SCALE_INPUTS),
          config.get('distort_inputs', DISTORT_INPUTS),
          config.get('zero_mean_inputs', ZERO_MEAN_INPUTS),
          display_step, save_checkpoint_secs, save_summaries_steps)
