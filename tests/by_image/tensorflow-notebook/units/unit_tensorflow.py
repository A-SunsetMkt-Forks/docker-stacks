# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import sys

if "NVIDIA_VISIBLE_DEVICES" in os.environ:
    print("Not running this test in GPU mode")
    sys.exit(0)

import tensorflow as tf

print(tf.constant("Hello, TensorFlow"))
print(tf.reduce_sum(tf.random.normal([1000, 1000])))
