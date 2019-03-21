# Jillian James, jiljames at reed dot edu

# Python program for running ML algorithms that predicts
# the contents of a systems paper using a bag-of-words model
# consisting of words and bigrams from a dataset of computer systems
# research papers. 

import csv
import pandas as pd
import numpy as np
import timeit

from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import tree


def get_metrics(true_labels, predicted_labels):
	#proportion of correct predictions in model
	print("Accuracy: ", (metrics.accuracy_score(true_labels, predicted_labels)))
	#number of predictions actually correct out of all positive predictions
	print("Precision: ", (metrics.precision_score(true_labels, predicted_labels, average="weighted")))
	#number of instances of positive class correctly predicted.
	print("Recall: ", (metrics.recall_score(true_labels, predicted_labels, average="weighted")))
	#the harmonic mean of the precision and recall 
	print("F1 score:", (metrics.f1_score(true_labels, predicted_labels, average="weighted")))


def split(filename):
	# Prepare the data for training.
	with open(filename, 'r') as tagcsv:
		tf = pd.read_csv(tagcsv)
		tagcsv.close()
	column_length = (len(tf.columns))
	
	train, test= train_test_split(tf, test_size = 0.2)
	print("train: ", train)
	print("test: ", test)
	train_features, train_labels = train.iloc[:,1:(column_length -1)], train.iloc[:,(column_length -1):column_length]
	test_features, test_labels = test.iloc[:,1:(column_length -1)], test.iloc[:,(column_length -1):column_length]
	feature_names = list(tf.columns)[1:column_length-1]

	print("Train features:", train_features)
	print("test features:", test_features)
	print("Train labels:", train_labels)
	print("test labels:", test_labels)

	return train_features, test_features, train_labels, test_labels, feature_names


def train_predict_evaluate(classifier, tagfile):
	train_features, test_features, train_labels, test_labels, feature_names = split(tagfile)
	train_labels = np.ravel(train_labels)
	print("Done splitting.")
	classifier.fit(train_features,train_labels)
	print("Done training.")
	predictions = classifier.predict(test_features)
	print("Done predicting.")
	get_metrics(np.ravel(test_labels), predictions)
	print("Predictions: ")
	return predictions, feature_names


def main():
#	print(str(timeit.timeit(split("open"), number=1))+" seconds")
	dtf = tree.DecisionTreeClassifier("entropy")

	# print(train_predict_evaluate(MultinomialNB(), "open_matrix.csv"))
	predictions, feature_names = train_predict_evaluate(dtf, "analysis_matrix.csv")
	print(predictions)
	tree.export_graphviz(dtf, out_file='tree.dot', feature_names = feature_names, filled = True, class_names = ['0', '1'])

	# print(train_predict_evaluate(MultinomialNB(), "system"))
	# print(train_predict_evaluate(MultinomialNB(), "data"))
	# print(train_predict_evaluate(MultinomialNB(), "analysis"))


