# AB Test Whether to Launch Free Trial Screener for Udacity Enrollment Page

## Experiment Overview
At the time of this experiment, Udacity courses currently have two options on the home page: "start free trial", and "access course materials". If the student clicks "start free trial", they will be asked to enter their credit card information, and then they will be enrolled in a free trial for the paid version of the course. After 14 days, they will automatically be charged unless they cancel first. If the student clicks "access course materials", they will be able to view the videos and take the quizzes for free, but they will not receive coaching support or a verified certificate, and they will not submit their final project for feedback.

In the experiment, Udacity tested a change where if the student clicked "start free trial", they were asked how much time they had available to devote to the course. If the student indicated 5 or more hours per week, they would be taken through the checkout process as usual. If they indicated fewer than 5 hours per week, a message would appear indicating that Udacity courses usually require a greater time commitment for successful completion, and suggesting that the student might like to access the course materials for free. At this point, the student would have the option to continue enrolling in the free trial, or access the course materials for free instead. 

The hypothesis was that this might set clearer expectations for students upfront, thus reducing the number of frustrated students who left the free trial because they didn't have enough time—without significantly reducing the number of students to continue past the free trial and eventually complete the course. If this hypothesis held true, Udacity could improve the overall student experience and improve coaches' capacity to support students who are likely to complete the course.

The unit of diversion is a cookie, although if the student enrolls in the free trial, they are tracked by user-id from that point forward. The same user-id cannot enroll in the free trial twice. For users that do not enroll, their user-id is not tracked in the experiment, even if they were signed in when they visited the course overview page.

## Experiment Design
### Metric Choice
First we need to determine the metrics to measure and their expected results.

#### Invariant metrics
Invariant metrics are variables that are tend to have big difference between the test and control group.
- Number of cookies: The number of unique cookies to view the course overview page.
- Number of clicks: The number of users who enroll in the free trial.
- Click through probabiliy: The number of unique cookies to click the "Start free trial" button divided by number of unique cookies to view the course overview page. 

Since visitors of the website did not view the screen asking if they can spend at least 5 hours per week at this point, these variables should not be affected by adding the screener. Thus these metrics should be the same for case and control group.

#### Evaluation metrics
- Gross Conversion: The number of user-ids to complete checkout and enroll in the free trial divided by number of unique cookies to click the "Start free trial" button.
- Retention: The number of user-ids to remain enrolled past the 14-day boundary (and thus make at least one payment) divided by number of user-ids to complete checkout.
- Net Conversion: The number of user-ids to remain enrolled past the 14-day boundary (and thus make at least one payment) divided by the number of unique cookies to click the "Start free trial" button. 

We expect gross conversion rate to be lower for testing group. With number of clicks be the same across groups, we expect the number of user-ids to decrease when the screening page eliminate visitors who cannot study enough time every week and potentially cancel the service. 

We expect retention rate to increase for testing group. With similar visitors enrolled in free trial in the test and control group, the screening page will likely to filter out students who are more likely to cancel in the future and thus increase the retention rate.

We expect net conversion to increase for the testing group with less students to cancel past the free trial period and more stay enrolled.


### Measuring Standard Deviation

Since we need a sample of unique cookies of 5,000 and the unique cookies to view Udacity page per day is 40,000. We are using 12.5% of the daily unique cookies as our sample. So the number of unique cookies that start the free trial per day for our sample is 3200 \*12.5% = 400 and the number of enrollment per day is 660 \*12.5%=82.5. 

The standard deviation of the three evaluation metrics are as follows:

Evaluation Metrics | Probability | Standard Deviation
-------------------|-------------|-------------------
 Gross Conversion | 0.20625 |0.02023
 Retention | 0.53 | 0.05495
 Net Conversion | 0.10931 | 0.0156
 
 We expect gross conversion and net conversion to be comparable to empirical results since the unit of analysis is cookie based while retention is based on the enrollment event. 


### Sizing
#### Number of Samples vs. Power
I decided not to use Bonferroni correction at this moment.

To calculate the sample sized for each evaluation metrics, we use this online calculator(http://www.evanmiller.org/ab-testing/sample-size.html) and alpha=0.05, beta=0.2.

Parameters| Gross Conversion | Retention | Net Conversion
----------| -----------------|-----------|---------------
Baseline Conversion| 0.20625 | 0.53 |0.10931
Minimum Detectable Effect| 0.01| 0.01 | 0.0075
alpha| 0.05 |0.05|0.05
beta| 0.2 |0.2 |0.2
sample size (each group) | 25,835| 39,115 |27,413
Total sample size | 51,670 | 78,230 | 54,826

Page view for gross conversion = 51,670/0.08= 645,875

Page view for retention = 78,230/(660/40,000) = 4,741,213

Page view for net conversion =54,826 /0.08=685,325

So total pageview needed for these metrics is 4,741,213. 

#### Duration vs. Exposure
Since Udacity have 40,000 unique cookies to view page per day, we would need about 119 days to collect enough sample if we use 100% of  the traffice to collect data. This strategy would be very risky. If we direct 50% of the traffice for study, then it would take 238 days to collect enough sample and this is too long.

If we could eliminate retention and use gross conversion and net conversion as measurements, our sample pageview needed is down to 685,325. If we direct 100% traffic, then it would take about 17 days and if 50% of the traffic is directed then it would take about 35 days for data collection. Using 50% of traffic would be more appropriate in this case and test and control group would each have 25%.

## Experiment Analysis
### Sanity Checks

#### Invariant Metrics:

Dataset|Total Pageviews | Total Clicks | Enrollments |Payments
-------|----------------|--------------|-------------|--------
Test | 344,660 | 28,325 |3,423 | 1,945
Control | 345,543| 28,378 | 3,785| 2,033

- Number of Cookies:

Observed = 345543/(344660+345543) = 0.5006

SE = sqrt(0.5006\*(1-0.5006)/(345543+344660)) = 0.0006018

CI Lower Bound= 0.5006-1.96\*SE = 0.4988

CI Upper Bound = 0.5006+1.96\*SE= 0.5012

- Number of Clicks:

Observed = 28378/(28325+28378) = 0.5004

SE = sqrt(0.5004\*(1-0.5004)/(28325+28378)) = 0.0020998

CI Lower Bound = 0.5004 - 1.96\*SE = 0.4959

CI Upper Bound = 0.5004 + 1.96\*SE = 0.5041

- Click-through probability: 

Observed = 28378/345543=0.08212

SE = sqrt(0.08212\*(1-0.08212)/(345543+344660)) =0.00033

CI Lower Bound = 0.08212-1.96\*SE = 0.0812

CI Upper Bound = 0.08212+1.96\*SE = 0.0830

Summarize the calculated numbers in the following table:

Metric | Expected Value | Empirical Result |CI| Check Result
-------| ---------------| -----------------|--|----------------
Number of Cookies | 0.5 | 0.5006 | (0.4994,0.5018) | Pass
Number of Clicks | 0.5 | 0.5004 | (0.4963,0.5045)|Pass
Click-through Probability | 0.08 | 0.0821 |(0.0815,0.0828)| Pass


## Result Analysis

### Effect Size Tests

For the experiment data, since there are only 23 observations with complete data, we will summarize the data as follows:

Dataset|Total Pageviews | Total Clicks | Enrollments |Payments
-------|----------------|--------------|-------------|--------
Test | 211,362|	17,260|	3,423|	1,945
Control | 212,163|	17,293|	3,785|	2,033

- Gross Conversion: The number of user-ids to complete checkout and enroll in the free trial divided by number of unique cookies to click the "Start free trial" button.

p_pooled = (3423+3785)/(17260+17293) = 0.2086071

SE = sqrt(0.2086\*(1-0.2086)\*(1/17260+1/17293)) = 0.0043716

d = 3423/17260-3785/17293 = -0.02055

CI Lower Bound = -0.02055 - 1.96\*SE = -0.0291

CI Upper Bound = -0.02055 + 1.96\*SE = -0.0120

The confidence interval for gross conversion is (-0.0291,-0.0120), which does not cover 0 and does not cover the minimum detectable effect d_min=(-)0.01. So it is both statistically and practically significant.


- Net Conversion: The number of user-ids to remain enrolled past the 14-day boundary (and thus make at least one payment) divided by the number of unique cookies to click the "Start free trial" button. 

p_pooled = (1945+2033)/(17260+17293) = 0.1151

SE = sqrt(0.1151\*(1-0.1151)\*(1/17260+1/17293)) = 0.003433

d = 1945/17260-2033/17293 = -0.00487

CI Lower Bound = -0.00487 - 1.96\*SE = -0.0116

CI Upper Bound = -0.00487 + 1.96\*SE = 0.0018

The confidence inverval for net conversion is (-0.0116, 0.0018). Since it covers 0, it is not statistically significant. The minimum detectable effect is d_min=0.0075, which falls within the confidence interval. Thus the confidence interval is not practically significant.


### Sign Tests

we read the data into R and calculated the following results:

Metric | P-value | Statistically significant
-------| --------|--------------------------
Gross Conversion|0.0026 | Statistically Significant
Net Conversion|0.6776 | Not Statistically Significant


## Summary

In this report, we explored the experiment conducted at udacity to decide whether to launch a screening page during course enrollment process. We first determined that number of cookies, number of clicks, and the click-through probability are invariant metrics of our study and gross conversion, retention, and net conversion are evaluatoin metrics for this study. We calculated the sample sizes for each evaluation metrics and the study length needed to colloect sample to have enough statistical power. But the sample size required by retention is too big that the experiment length would be too long to have enough sample so we decided to remove it from the evaluation metrics.

After the metrics are chosen, we conducted sanity checks to ensure the invariant metrics are similar across two groups and all three metrics pass the sanity checks. Next, we conducted paired t-tests and sign tests to check the statistical significance of the two evaluation metrics. The null hypothesis is that there is no difference between experiment and control groups for each evaluation metrics. We reject the null is p-value is smaller than 0.05. We found that, with 95% of confidence, gross conversion there are both statistically and practically significant difference between the experiment and control group. However, for net conversion, it is neither a statistically significant nor a practically significant metric at 95% confidence level.

During the exploration, we did not use the Bonferroni Correction. Boferroni correction is employed when conducting multiple testing to control family wise error rate or false positive rate. But since there are positive correlation within the sample variables, using Bonferroni Correction would make the tests being too conservative. 

## Recommendation

From the results above, we can see statistically and practically significant in gross conversion but not so for net conversion. This translates to decreases in enrollment but the proportion of students paying to stay for the service did not increase. I would recommend not to launch this screener at this moment. 


## Follow-Up Experiment
Give a high-level description of the follow up experiment you would run, what your hypothesis would be, what metrics you would want to measure, what your unit of diversion would be, and your reasoning for these choices.


