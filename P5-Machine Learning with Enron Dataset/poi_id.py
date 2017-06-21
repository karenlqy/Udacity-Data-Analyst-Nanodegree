#!/usr/bin/python

import sys
import pickle
import numpy
import pandas
import matplotlib
from copy import copy


from ggplot import *

sys.path.append("../tools/")
import sklearn
from sklearn.feature_selection import SelectKBest,chi2
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from feature_format import featureFormat, targetFeatureSplit
from sklearn import preprocessing
from sklearn.grid_search import GridSearchCV

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
#features_list = ['poi','salary','bonus', 'exercised_stock_options' 'expenses','restricted_stock' 'total_stock_value','poi_email_ratio'] # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
target_label = 'poi'
email_features_list = [
    # 'email_address', # remit email address; informational label
    'from_messages',
    'from_poi_to_this_person',
    'from_this_person_to_poi',
    'shared_receipt_with_poi',
    'to_messages',
    ]
financial_features_list = [
    'bonus',
    'deferral_payments',
    'deferred_income',
    'director_fees',
    'exercised_stock_options',
    'expenses',
    'loan_advances',
    'long_term_incentive',
    'other',
    'restricted_stock',
    'restricted_stock_deferred',
    'salary',
    'total_payments',
    'total_stock_value',
]
features_list = [target_label] + financial_features_list + email_features_list


### Task 2: Remove outliers
data_dict.pop('TOTAL',0)
data_dict.pop('LOCKHART EUGENE E', 0)
df=pandas.DataFrame.from_records(list(data_dict.values()))
df.replace(to_replace='NaN', value=numpy.nan, inplace=True)

#Remove variables with 80% of total datapoints missing. There are 146 people in the dataset.
#80% of the 146 is 116. So we remove variables that have more than 116 NaNs.
for column, series in df.iteritems():
    if series.isnull().sum() > 116:
        df.drop(column, axis=1, inplace=True)
# Drop email address column
if 'email_address' in list(df.columns.values):
    df.drop('email_address', axis=1, inplace=True)

features_list.remove('loan_advances')
features_list.remove('director_fees')
features_list.remove('restricted_stock_deferred')


#Since the range of some variables can be very big, causing the mean to be skewed toward high value, 
#median would be better for imputation.
impute = sklearn.preprocessing.Imputer(missing_values=numpy.nan, strategy='median', axis=0)
impute.fit(df)
df_imputed = pandas.DataFrame(impute.transform(df.copy(deep=True)))
df_imputed.columns = list(df.columns.values)
#Plot salary vs. bonus and found an outlier that has salary more than $2,500,000
ggplot(aes(x='salary',y='bonus',color='poi'),data=df_imputed)+geom_point()

#add new features
df_imputed['fraction_from_poi']=df_imputed['from_poi_to_this_person']/df_imputed['from_messages']
df_imputed['fraction_to_poi']=df_imputed['from_this_person_to_poi']/df_imputed['to_messages']

features_list.append('fraction_from_poi')
features_list.append('fraction_to_poi')
#features_list.append('fraction_shared')

features_list.remove('from_poi_to_this_person')
features_list.remove('from_this_person_to_poi')
features_list.remove('from_messages')
features_list.remove('to_messages')
#features_list.remove('shared_receipt_with_poi')
df_imputed=df_imputed.drop('from_poi_to_this_person',1)
df_imputed=df_imputed.drop('from_this_person_to_poi',1)
df_imputed=df_imputed.drop('to_messages',1)
df_imputed=df_imputed.drop('from_messages',1)
#df_imputed=df_imputed.drop('shared_receipt_with_poi',1)

#Rescale data
labels = df_imputed['poi'].astype(int).as_matrix()
features = df_imputed.drop('poi',1).as_matrix()

min_max_scaler = preprocessing.MinMaxScaler()
features_scaled=min_max_scaler.fit_transform(features)


#### feature selection using SelectKBest;
kbest = SelectKBest(chi2, k=10)
features_kbest=kbest.fit_transform(features_scaled,labels)
features_selected=[features_list[i+1] for i in kbest.get_support(indices=True)]

feature_scores = ['%.2f' % elem for elem in kbest.scores_ ]
features_scores_selected=[feature_scores[i]for i in kbest.get_support(indices=True)]
print 'Selected Features', features_selected
print 'Feature Scores', features_scores_selected

#data for grading
#remove features that already been deleted in the dataset

my_dataset=df_imputed.to_dict(orient='index')
my_features_list=[target_label]+features_selected
print my_features_list
data = featureFormat(my_dataset, my_features_list)
labels, features = targetFeatureSplit(data)


from sklearn.model_selection import train_test_split
features_train, features_test, labels_train, labels_test = train_test_split(features_scaled,labels,test_size=0.3,random_state=42)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html
# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
g_clf = GaussianNB()
g_clf.fit(features_train,labels_train)
pred=g_clf.predict(features_test)
accuracy = accuracy_score(pred,labels_test)
recall=recall_score(labels_test,pred)
precision=precision_score(labels_test,pred)
print "The accuracy score of this classifier is: %s" % accuracy
print "The recall score of this classifier is: %s" % recall
print "The precision score of this classifier is: %s" % precision


from sklearn.ensemble import RandomForestClassifier
r_clf=RandomForestClassifier()
r_clf.fit(features_train,labels_train)
pred=r_clf.predict(features_test)
accuracy = accuracy_score(pred,labels_test)
recall=recall_score(labels_test,pred)
precision=precision_score(labels_test,pred)
print "The accuracy score of this classifier is: %s" % accuracy
print "The recall score of this classifier is: %s" % recall
print "The precision score of this classifier is: %s" % precision

from sklearn.ensemble import AdaBoostClassifier
a_clf=AdaBoostClassifier()
a_clf.fit(features_train,labels_train)
pred=a_clf.predict(features_test)
accuracy = accuracy_score(pred,labels_test)
recall=recall_score(labels_test,pred)
precision=precision_score(labels_test,pred)
print "The accuracy score of this classifier is: %s" % accuracy
print "The recall score of this classifier is: %s" % recall
print "The precision score of this classifier is: %s" % precision

from sklearn.linear_model import LogisticRegression
l_clf=LogisticRegression()
l_clf.fit(features_train,labels_train)
pred=l_clf.predict(features_test)
accuracy = accuracy_score(pred,labels_test)
recall=recall_score(labels_test,pred)
precision=precision_score(labels_test,pred)
print "The accuracy score of this classifier is: %s" % accuracy
print "The recall score of this classifier is: %s" % recall
print "The precision score of this classifier is: %s" % precision
### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!


a_clf=AdaBoostClassifier()
parameters={'n_estimators':[5,10,20,50,60,70,80,90,100],'learning_rate':[0.5,1,1.2,1.3,1.4,1.5,2 ],'algorithm':('SAMME','SAMME.R')}
gs=GridSearchCV(a_clf,parameters)
gs.fit(features_train,labels_train)
a_y_pred=gs.predict(features_test)


#accuracy = accuracy_score(r_y_pred,labels_test)
#recall=recall_score(labels_test,r_y_pred)
#precision=precision_score(labels_test,r_y_pred)
#print "The accuracy score of this classifier is: %s" % accuracy
#print "The recall score of this classifier is: %s" % recall
#print "The precision score of this classifier is: %s" % precision



clf=gs.best_estimator_

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

    
pickle.dump(clf, open("my_classifier.pkl", "w") )
pickle.dump(my_dataset, open("my_dataset.pkl", "w") )
pickle.dump(my_features_list, open("my_feature_list.pkl", "w") )