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
 
 


### Sizing
#### Number of Samples vs. Power
Indicate whether you will use the Bonferroni correction during your analysis phase, and give the number of pageviews you will need to power you experiment appropriately. (These should be the answers from the "Calculating Number of Pageviews" quiz.)

#### Duration vs. Exposure
Indicate what fraction of traffic you would divert to this experiment and, given this, how many days you would need to run the experiment. (These should be the answers from the "Choosing Duration and Exposure" quiz.)

Give your reasoning for the fraction you chose to divert. How risky do you think this experiment would be for Udacity?

## Experiment Analysis
Sanity Checks
For each of your invariant metrics, give the 95% confidence interval for the value you expect to observe, the actual observed value, and whether the metric passes your sanity check. (These should be the answers from the "Sanity Checks" quiz.)

For any sanity check that did not pass, explain your best guess as to what went wrong based on the day-by-day data. Do not proceed to the rest of the analysis unless all sanity checks pass.

## Result Analysis
### Effect Size Tests
For each of your evaluation metrics, give a 95% confidence interval around the difference between the experiment and control groups. Indicate whether each metric is statistically and practically significant. (These should be the answers from the "Effect Size Tests" quiz.)

### Sign Tests
For each of your evaluation metrics, do a sign test using the day-by-day data, and report the p-value of the sign test and whether the result is statistically significant. (These should be the answers from the "Sign Tests" quiz.)

## Summary
State whether you used the Bonferroni correction, and explain why or why not. If there are any discrepancies between the effect size hypothesis tests and the sign tests, describe the discrepancy and why you think it arose.

## Recommendation
Make a recommendation and briefly describe your reasoning.

## Follow-Up Experiment
Give a high-level description of the follow up experiment you would run, what your hypothesis would be, what metrics you would want to measure, what your unit of diversion would be, and your reasoning for these choices.


