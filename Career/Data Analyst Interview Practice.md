### 1. Describe a data project you worked on recently.

I worked on a project from udacity class to study the financial and email data from Enron which is a dataset of 146 records of the senior management's financial and email data. In this project, I need to build a predictive model that can identify an individual as a "Person of Interest" (POI) that requires further analysis. I used the scikit-learn package & various machine learning techniques for this exercise.

First, I used the SelectKBest function from scikitlearn to select the top 10 influential features and used those featuers for upcoming algorithm. After feature selection, I then scaled all features using min-max scalers to make sure all data are on the same scale. Next, I split the dataset into training and testing dataset using a 80:20 ratio. I used the 10-fold validation method to build and compare several machine learning algorithms, such as random forest, adaboost, and logistic regression. I also used parameter tuning in order to improve the fit on the training set. I selected the random forest algothm as my final model based on the accuracy, recall and precision rates.

Finally, I test the model on testing dataset and reported the accuracy, recall and precision rates.
By working on this project, I have the experienced the complete data analytics process from data cleansing, exploratory analysis, to model building and evaluation. I believe this is a great exercise for me to explore this field and have a taste of my future workflow. After completion of the data analyst nanodegree, I'm planning to dive deeper into the data science field to continue learning and working on more projects and kaggle competitions.

### 2. You are given a ten piece box of chocolate truffles. You know based on the label that six of the pieces have an orange cream filling and four of the pieces have a coconut filling. If you were to eat four pieces in a row, what is the probability that the first two pieces you eat have an orange cream filling and the last two have a coconut filling?

P(1st is orange cream)=6/10
P(2nd is orange cream)=5/9
P(3rd is coconut)=4/8
P(4th is coconut)=3/7
So,
P(1st orange and 2nd orange and 3rd cocut and 4th coconut) =6/10*5/9*4/8*3/7=0.0714

If you were given an identical box of chocolates and again eat four pieces in a row, what is the probability that exactly two contain coconut filling?

From the four pieces, we would like to find the probability of two having coconut filling.

P(two pieces have coconut filling)=$\frac{{4 \choose 2}}{{4 \choose 0}+{4 \choose 1}+{4 \choose 2} + {4 \choose 3} + {4 \choose 4}}$
### 3. Construct a query to find the top 5 states with the highest number of active users. Include the number for each state in the query result.
```sqlite
select sum(active) as num_active_user, state
from users
group by state
order by num_active_user desc
limit 5
```


### 4. Define a function first_unique that takes a string as input and returns the first non-repeated (unique) character in the input string. If there are no unique characters return None. Note: Your code should be in Python.

```python
from collections import defaultdict
def first_unique(string):
  counts = defaultdict(int)
    ''' create an empty list'''
    l = []
    '''loop through each character in the string'''
    for c in word:
        counts[c] += 1
        '''if there's first unique character, append them to list'''
        if counts[c] == 1:
            l.append(c)
    ''' if list only contains 1 character, return the result'''        
    for c in l:
        if counts[c] == 1:
            return c
    ''' otherwise, return "None"" '''
    return "None"
```

### 5. What are underfitting and overfitting in the context of Machine Learning? How might you balance them?
Overfitting is when the model fits the data perfectly. The issue with overfitting is that when we test the model on another testing dataset, the prediction error might be very large. On the other hand, underfitting is when the model does not capture the data trends shown in the data. We can identify underfitting issue when the model shows low variance but high bias. To balance overfitting and underfitting, we can use resampling method of the training data to estimate the model accuracy, such as the k-fold validation method. We also need to hold a separate testing dataset to check if the model fits well on the testing data.

### 6. If you were to start your data analyst position today, what would be your goals a year from now?
I would like to apply to this position: https://www.kaggle.com/jobs/18070/capital-one-data-scientist-post-graduate-programme-nottingham

6 months into the position, I would like to have a better understanding of the big picture of capital one business, the marketspace and be familiar with current statistical and machine learning used in the business. I will be very familiar with all the databases and metrics used in daily work. In addition, I should be able to contribute my insights to some projects and facilitate business decisions. 

A year from now, I would like to greatly improve my coding skills in python to meet daily  project needs. I will be developeing new process or improving existing models to study member behaviour and predict their future credit card activities. Within one year, I would like to learn and be able to build machine learning models such as Xgboost and be comfortable with packages such as Tensorflow. 

Beyong one year, I would like to continue my learning within the data analytics field and keep up with the popular methods at that time. I would also like to take leadership on several projects and contribute to productionize of existing processes.
