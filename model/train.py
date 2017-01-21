import json

import tensorflow as tf

from data import inputs
from .inference import inference
from .model import train_step, cal_loss, cal_acc
from .hooks import hooks


TRAIN_DIR = '/tmp/train'
BATCH_SIZE = 128
LAST_STEP = 20000
LEARNING_RATE = 0.1
EPSILON = 1.0
BETA_1 = 0.9
BETA_2 = 0.999
DISTORT_INPUTS = True
STANDARDIZATION = True
DISPLAY_STEP = 10
SAVE_CHECKPOINT_SECS = 30
SAVE_SUMMARIES_STEPS = 100


def train(dataset, structure, train_dir=TRAIN_DIR, batch_size=BATCH_SIZE,
          last_step=LAST_STEP,  learning_rate=LEARNING_RATE, epsilon=EPSILON,
          beta1=BETA_1, beta2=BETA_2, distort_inputs=DISTORT_INPUTS,
          standardization=STANDARDIZATION, display_step=DISPLAY_STEP,
          save_checkpoint_secs=SAVE_CHECKPOINT_SECS,
          save_summaries_steps=SAVE_SUMMARIES_STEPS):

    if tf.gfile.Exists(train_dir):
        tf.gfile.DeleteRecursively(train_dir)
    tf.gfile.MakeDirs(train_dir)

    with tf.Graph().as_default():
        global_step = tf.contrib.framework.get_or_create_global_step()

        data, labels = inputs(dataset, batch_size, distort_inputs,
                              standardization, shuffle=True)

        logits = inference(data, structure)
        loss = cal_loss(logits, labels)
        acc = cal_acc(logits, labels)

        train_op = train_step(
            loss, global_step, learning_rate, beta1, beta2, epsilon)

        with tf.train.MonitoredTrainingSession(
                checkpoint_dir=train_dir,
                save_checkpoint_secs=save_checkpoint_secs,
                save_summaries_steps=save_summaries_steps,
                hooks=hooks(display_step, last_step, batch_size, loss, acc)
                ) as monitored_session:
            while not monitored_session.should_stop():
                monitored_session.run(train_op)


def json_train(dataset, json):
    train(
        dataset,
        json['structure'],
        json['train_dir'] if 'train_dir' in json else TRAIN_DIR,
        json['batch_size'] if 'batch_size' in json else BATCH_SIZE,
        json['last_step'] if 'last_step' in json else LAST_STEP,
        json['learning_rate'] if 'learning_rate' in json else LEARNING_RATE,
        json['epsilon'] if 'epsilon' in json else EPSILON,
        json['beta1'] if 'beta1' in json else BETA_1,
        json['beta2'] if 'beta2' in json else BETA_2,
        json['distort_inputs'] if 'distort_inputs' in json else DISTORT_INPUTS,
        json['standardization'] if 'standardization' in json
        else STANDARDIZATION,
        json['display_step'] if 'display_step' in json else DISPLAY_STEP,
        json['save_checkpoint_secs'] if 'save_checkpoint_secs' in json
        else SAVE_CHECKPOINT_SECS,
        json['save_summaries_steps'] if 'save_summaries_steps' in json
        else SAVE_SUMMARIES_STEPS)
