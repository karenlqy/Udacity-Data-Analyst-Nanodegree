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
from sklearn.feature_selection import SelectKBest
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from feature_format import featureFormat, targetFeatureSplit
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA

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

#features_list.remove('from_poi_to_this_person')
#features_list.remove('from_this_person_to_poi')
#features_list.remove('from_messages')
#features_list.remove('to_messages')
#features_list.remove('shared_receipt_with_poi')
#df_imputed=df_imputed.drop('from_poi_to_this_person',1)
#df_imputed=df_imputed.drop('from_this_person_to_poi',1)
#df_imputed=df_imputed.drop('to_messages',1)
#df_imputed=df_imputed.drop('from_messages',1)
#df_imputed=df_imputed.drop('shared_receipt_with_poi',1)

#Rescale data
labels = df_imputed['poi'].astype(int).as_matrix()
features = df_imputed.drop('poi',1).as_matrix()


#### feature selection using SelectKBest;
pipe=Pipeline([("scaler",MinMaxScaler()),
               ("skb",SelectKBest()),
               ("clf",RandomForestClassifier(random_state=42))])

sss = StratifiedShuffleSplit(random_state = 0)
parameters={'skb__k':range(1,len(features_list)),
            "clf__n_estimators":[5,10,15,20,50,100],
            "clf__min_samples_split":[2,3,5],
            "clf__min_samples_leaf":[2,3,5]}
gs=GridSearchCV(pipe,parameters,cv=sss,scoring="f1")
gs.fit(features,labels)

K_best = gs.best_estimator_.named_steps['skb']

# Get SelectKBest scores, rounded to 2 decimal places, name them "feature_scores"
feature_scores = ['%.2f' % elem for elem in K_best.scores_ ]
# Get SelectKBest pvalues, rounded to 3 decimal places, name them "feature_scores_pvalues"
feature_scores_pvalues = ['%.3f' % elem for elem in  K_best.pvalues_ ]
# Get SelectKBest feature names, whose indices are stored in 'K_best.get_support',
# create a tuple of feature names, scores and pvalues, name it "features_selected_tuple"
features_selected_tuple=[(features_list[i+1], feature_scores[i], feature_scores_pvalues[i]) for i in K_best.get_support(indices=True)]
features_selected=[features_list[i+1] for i in K_best.get_support(indices=True)]

# Sort the tuple by score, in reverse order
features_selected_tuple = sorted(features_selected_tuple, key=lambda feature: float(feature[1]) , reverse=True)
print features_selected_tuple

#data for grading
#remove features that already been deleted in the dataset

my_dataset=df_imputed.to_dict(orient='index')
my_features_list=[target_label]+features_selected
print my_features_list
data = featureFormat(my_dataset, my_features_list)
labels, features = targetFeatureSplit(data)

features_kbest=K_best.fit_transform(features,labels)

sss = StratifiedShuffleSplit(n_splits=3,test_size=0.3,random_state=42)
for train_index,test_index in sss.split(features_kbest,labels):
    features_train = []
    features_test  = []
    labels_train   = []
    labels_test    = []
    for ii in train_index:
        features_train.append( features_kbest[ii] )
        labels_train.append( labels[ii] )
    for jj in test_index:
        features_test.append( features_kbest[jj] )
        labels_test.append( labels[jj] )
        
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
#parameters={"penalty":('l1','l2'),
#            "C":(0.2,0.5,0.8,1,1.2,1.5,1.7,1.9,2),
#            'max_iter':[100,200,500,1000]}

#l_clf=LogisticRegression()
#gs=GridSearchCV(l_clf,parameters)
#gs.fit(features_train,labels_train)
#l_y_pred=gs.predict(features_test)

#parameters={
#            "n_estimators":[5,10,15,20,50,100],
#            "criterion":("gini","entropy"),
#            "min_samples_split":[2,3,5],
#            "min_samples_leaf":[2,3,5]}
#r_clf=RandomForestClassifier()
#gs=GridSearchCV(r_clf,parameters)
#gs.fit(features_train,labels_train)
#r_y_pred=gs.predict(features_test)

#parameters={
#            "n_neighbors":range(1,10),
#            "algorithm":("ball_tree","kd_tree","brute"),
#            'weights': ['uniform', 'distance'],
#            'p': [1, 2], 'leaf_size': [1, 5, 9, 10, 20, 30, 40, 50, 60]}

#k_clf=KNeighborsClassifier()
#gs=GridSearchCV(k_clf,parameters)
#gs.fit(features_train,labels_train)
#k_y_pred=gs.predict(features_test)


clf=g_clf

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

    
pickle.dump(clf, open("my_classifier.pkl", "w") )
pickle.dump(my_dataset, open("my_dataset.pkl", "w") )
pickle.dump(my_features_list, open("my_feature_list.pkl", "w") )