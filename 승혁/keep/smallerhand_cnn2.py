#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 23:27:00 2018
    
@author: kimseunghyuck
"""
import tensorflow as tf
tf.reset_default_graph()     #그래프 초기화
tf.set_random_seed(777) 
import pandas as pd
import numpy as np
train = pd.read_csv('desktop/python/train.csv')

#훈련세트, validation세트 나누기
from sklearn.model_selection import train_test_split
train_set, validate_set = train_test_split(train, test_size = 0.3)
trainData = train_set.values[:,1:]
validateData = validate_set.values[:,1:]
trainLabel=train_set.values[:,0]
validateLabel=validate_set.values[:,0]

# hyper parameters
learning_rate = 0.001
training_epochs = 20
batch_size = 100
steps_for_validate = 5
keep_prob = tf.placeholder(tf.float32)

# input place holders
X = tf.placeholder(tf.float32, [None, 784])
X_img = tf.reshape(X, [-1, 28, 28, 1])          # img 28x28x1 (black/white)
Y = tf.placeholder(tf.int32, [None, 1])
Y_onehot=tf.reshape(tf.one_hot(Y, 10), [-1, 10])

# L1 ImgIn shape=(?, 28, 28, 1)
W1 = tf.Variable(tf.random_normal([2, 2, 1, 32], stddev=0.01))
L1 = tf.nn.conv2d(X_img, W1, strides=[1, 1, 1, 1], padding='SAME')
L1 = tf.nn.relu(L1)
L1 = tf.nn.max_pool(L1, ksize=[1, 2, 2, 1],
                    strides=[1, 2, 2, 1], padding='SAME')
L1 = tf.nn.dropout(L1, keep_prob=keep_prob)
L1_flat = tf.reshape(L1, [-1, 14 * 14 * 32])

# L1_2 추가
W1_2 = tf.Variable(tf.random_normal([3, 3, 1, 32], stddev=0.01))
L1_2 = tf.nn.conv2d(X_img, W1_2, strides=[1, 1, 1, 1], padding='SAME')
L1_2 = tf.nn.relu(L1_2)
L1_2 = tf.nn.max_pool(L1_2, ksize=[1, 2, 2, 1],
                    strides=[1, 2, 2, 1], padding='SAME')
L1_2 = tf.nn.dropout(L1_2, keep_prob=keep_prob)
L1_flat_2 = tf.reshape(L1_2, [-1, 14 * 14 * 32])

# L1_3 추가
W1_3 = tf.Variable(tf.random_normal([4, 4, 1, 32], stddev=0.01))
L1_3 = tf.nn.conv2d(X_img, W1_3, strides=[1, 1, 1, 1], padding='SAME')
L1_3 = tf.nn.relu(L1_3)
L1_3 = tf.nn.max_pool(L1_3, ksize=[1, 2, 2, 1],
                    strides=[1, 2, 2, 1], padding='SAME')
L1_3 = tf.nn.dropout(L1_3, keep_prob=keep_prob)
L1_flat_3 = tf.reshape(L1_3, [-1, 14 * 14 * 32])

# L2 ImgIn shape=(?, 14, 14, 10)
W2 = tf.Variable(tf.random_normal([2, 2, 32, 64], stddev=0.01))
L2 = tf.nn.conv2d(L1, W2, strides=[1, 1, 1, 1], padding='SAME')
L2 = tf.nn.relu(L2)
L2 = tf.nn.max_pool(L2, ksize=[1, 2, 2, 1],
                    strides=[1, 2, 2, 1], padding='SAME')
L2 = tf.nn.dropout(L2, keep_prob=keep_prob)
L2_flat = tf.reshape(L2, [-1, 7 * 7 * 64])

# L2_2 추가
W2_2 = tf.Variable(tf.random_normal([3, 3, 32, 64], stddev=0.01))
L2_2 = tf.nn.conv2d(L1_2, W2_2, strides=[1, 1, 1, 1], padding='SAME')
L2_2 = tf.nn.relu(L2_2)
L2_2 = tf.nn.max_pool(L2_2, ksize=[1, 2, 2, 1],
                    strides=[1, 2, 2, 1], padding='SAME')
L2_2 = tf.nn.dropout(L2_2, keep_prob=keep_prob)
L2_flat_2 = tf.reshape(L2_2, [-1, 7 * 7 * 64])

# L2_3 추가
W2_3 = tf.Variable(tf.random_normal([3, 3, 32, 64], stddev=0.01))
L2_3 = tf.nn.conv2d(L1_3, W2_3, strides=[1, 1, 1, 1], padding='SAME')
L2_3 = tf.nn.relu(L2_3)
L2_3 = tf.nn.max_pool(L2_3, ksize=[1, 2, 2, 1],
                    strides=[1, 2, 2, 1], padding='SAME')
L2_3 = tf.nn.dropout(L2_3, keep_prob=keep_prob)
L2_flat_3 = tf.reshape(L2_3, [-1, 7 * 7 * 64])

# Final FC 7x7x64 inputs -> 10 outputs
W3 = tf.get_variable("W3", shape=[7 * 7 * 64, 10],
                     initializer=tf.contrib.layers.xavier_initializer())
W3_2 = tf.get_variable("W3_2", shape=[7 * 7 * 64, 10],
                     initializer=tf.contrib.layers.xavier_initializer())
W3_3 = tf.get_variable("W3_3", shape=[7 * 7 * 64, 10],
                     initializer=tf.contrib.layers.xavier_initializer()) 
W32 = tf.get_variable("W32", shape=[14 * 14 * 32, 10],
                     initializer=tf.contrib.layers.xavier_initializer())
W3_22 = tf.get_variable("W3_22", shape=[14 * 14 * 32, 10],
                     initializer=tf.contrib.layers.xavier_initializer())
W3_32 = tf.get_variable("W3_32", shape=[14 * 14 * 32, 10],
                     initializer=tf.contrib.layers.xavier_initializer()) 
logits = tf.matmul(L2_flat, W3) + tf.matmul(L2_flat_2, W3_2) + tf.matmul(L2_flat_3, W3_3) + tf.matmul(L1_flat, W32) + tf.matmul(L1_flat_2, W3_32) + tf.matmul(L1_flat_3, W3_32) 


# define cost/loss & optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
    logits=logits, labels=Y_onehot))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# initialize
sess = tf.Session()
sess.run(tf.global_variables_initializer())

# train my model
print('Learning started. It takes sometime.')
for epoch in range(training_epochs):
    avg_cost = 0
    total_batch = int(len(trainData) / batch_size)
    for i in range(total_batch):
        batch_xs = trainData[i*batch_size:(i+1)*batch_size]
        batch_ys = trainLabel[i*batch_size:(i+1)*batch_size].reshape(-1, 1)
        feed_dict = {X: batch_xs, Y: batch_ys, keep_prob: .7}
        c, _ = sess.run([cost, optimizer], feed_dict=feed_dict)
        avg_cost += c / total_batch
    print('Epoch:', '%04d' % (epoch + 1), 'cost =', '{:.9f}'.format(avg_cost))
    if epoch % steps_for_validate == steps_for_validate-1:
        correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(Y_onehot, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        print('Accuracy:', sess.run(accuracy, feed_dict={
                X: validateData, Y: validateLabel.reshape(-1, 1), keep_prob: 1}))       
print('Finished!')


"""
learning_rate = 0.001
training_epochs = 15
batch_size = 100

5. 병렬로 구성하고 window 크기도 원래만큼 늘림.
w1, w2= 5*5, 32개/ 3*3, 64개
w1_2, w2_2 = 3*3, 36개/ 3*3, 40개
정확도 98.48%
생각보다 높지 않았다.

6. 5에서 dropout추가
정확도 98.78% / 98.73% (epoch 5)

7. 6에서 각 층에 3개 window. w1= 2*2, 32개/ 3*3, 32개/ 4*4, 32개
w2=2*2, 64개/ 3*3, 64개/ 4*4, 64개 

8. 7에서 1층에서 2층으로도, 3층으로도 전달.
최종 layer에서 w1과 w2의 출력값을 모두 받음.
97.93% (epoch 20)
"""
