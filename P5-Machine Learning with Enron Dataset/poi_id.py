#!/usr/bin/python

import sys
import pickle
import numpy
import pandas
import matplotlib

from ggplot import *

sys.path.append("../tools/")
import sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from feature_format import featureFormat, targetFeatureSplit
from sklearn import preprocessing

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
#features_list = ['poi','salary','bonus', 'exercised_stock_options' 'expenses','restricted_stock' 'total_stock_value','poi_email_ratio'] # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
df=pandas.DataFrame.from_records(list(data_dict.values()))
df.replace(to_replace='NaN', value=numpy.nan, inplace=True)

for column, series in df.iteritems():
    if series.isnull().sum() > 73:
        df.drop(column, axis=1, inplace=True)
# Drop email address column
if 'email_address' in list(df.columns.values):
    df.drop('email_address', axis=1, inplace=True)

impute = sklearn.preprocessing.Imputer(missing_values=numpy.nan, strategy='median', axis=0)
impute.fit(df)
df_imputed = pandas.DataFrame(impute.transform(df.copy(deep=True)))
df_imputed.columns = list(df.columns.values)
df_cleaned=df_imputed.loc[df_imputed.salary<2500000]

### Task 3: Create new feature(s)
df_cleaned['poi_email_ratio']=(df_cleaned['from_poi_to_this_person']+df_cleaned['from_this_person_to_poi'])/(df_cleaned['from_messages']+df_cleaned['to_messages']+1)

labels = df_cleaned['poi'].astype(int).as_matrix()
features = df_cleaned.drop('poi',1).as_matrix()

min_max_scaler = preprocessing.MinMaxScaler()
features_scaled=min_max_scaler.fit_transform(features)

#### feature selection using random forest;
from sklearn.ensemble import RandomForestClassifier
clf=RandomForestClassifier(n_estimators=1000,random_state=456)
clf.fit(features,labels)


important_features = []
for x,i in enumerate(clf.feature_importances_):
    if i>numpy.average(clf.feature_importances_):
        important_features.append((x))
        
from sklearn.model_selection import train_test_split
features_selected=features[:,important_features]
features_train, features_test, labels_train, labels_test = train_test_split(features_selected,labels,test_size=0.3,random_state=123)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html
# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.fit(features_train,labels_train)
pred=clf.predict(features_test)
accuracy = accuracy_score(pred,labels_test)
print "The accuracy score of Naive Bayes classifier is: %s" % accuracy


from sklearn.ensemble import RandomForestClassifier
clf=RandomForestClassifier()
clf.fit(features_train,labels_train)
pred=clf.predict(features_test)
accuracy = accuracy_score(pred,labels_test)
print "The accuracy score of Random Forest classifier is: %s" % accuracy

from sklearn.ensemble import AdaBoostClassifier
clf=AdaBoostClassifier()
clf.fit(features_train,labels_train)
pred=clf.predict(features_test)
accuracy = accuracy_score(pred,labels_test)
print "The accuracy score of AdaBoost classifier is: %s" % accuracy

from sklearn.linear_model import LogisticRegression
clf=LogisticRegression()
clf.fit(features_train,labels_train)
pred=clf.predict(features_test)
accuracy = accuracy_score(pred,labels_test)
print "The accuracy score of Logistic Regression classifier is: %s" % accuracy
### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
clf= GaussianNB()
clf.fit(features_train,labels_train)
pred=clf.predict(features_test)

accuracy = accuracy_score(pred,labels_test)
recall=recall_score(labels_test,pred)
precision=precision_score(labels_test,pred)
print "The accuracy score of this classifier is: %s" % accuracy
print "The recall score of this classifier is: %s" % recall
print "The precision score of this classifier is: %s" % precision

clf=RandomForestClassifier(n_estimators=30,min_samples_split=10,max_features=8)
clf.fit(features_train,labels_train)
pred=clf.predict(features_test)

accuracy = accuracy_score(pred,labels_test)
recall=recall_score(labels_test,pred)
precision=precision_score(labels_test,pred)
print "The accuracy score of this classifier is: %s" % accuracy
print "The recall score of this classifier is: %s" % recall
print "The precision score of this classifier is: %s" % precision

clf=AdaBoostClassifier(n_estimators=10,learning_rate=1.5,algorithm='SAMME')
clf.fit(features_train,labels_train)
pred=clf.predict(features_test)
accuracy = accuracy_score(pred,labels_test)
recall=recall_score(labels_test,pred)
precision=precision_score(labels_test,pred)
print "The accuracy score of this classifier is: %s" % accuracy
print "The recall score of this classifier is: %s" % recall
print "The precision score of this classifier is: %s" % precision

clf=LogisticRegression(penalty='l1' )
clf.fit(features_train,labels_train)
pred=clf.predict(features_test)

accuracy = accuracy_score(pred,labels_test)
recall=recall_score(labels_test,pred)
precision=precision_score(labels_test,pred)
print "The accuracy score of this classifier is: %s" % accuracy
print "The recall score of this classifier is: %s" % recall
print "The precision score of this classifier is: %s" % precision


### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.
clf=RandomForestClassifier(n_estimators=30,min_samples_split=10,max_features=8)
clf.fit(features_train,labels_train)
pickle.dump(clf, open("my_classifier.pkl", "w") )
pickle.dump(df_cleaned, open("my_dataset.pkl", "w") )
pickle.dump(features_selected, open("my_feature_list.pkl", "w") )