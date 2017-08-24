# Udacity DAND P6 Data Visualization with Tableau Write Up
### Qingyu Li  Aug. 23 2017  Final Project link is [here](https://public.tableau.com/profile/qingyu.li#!/vizhome/AirTravelDelayStudy-DANDTableauClassProject/Story1?publish=yes)

First working version is [here](https://public.tableau.com/profile/qingyu.li#!/vizhome/AirTravelDelayStudy_v1/Story1)
## Background
I'm traveling out of Chicago O'Hare frequently and I am interested in studying the flight delay data for US in 2016. The data is downloaded from Bureau of Transportation Statistics website [RITA](https://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp) database. 

## Design
In this project, I'm interested to see which airport has highest average delay arrival in minutes and I would like to know the reason for such delay. I will find out the top 5 airports with arrival delays and study the delay time by security reason, weather and carrier.

- Card 1: A map of continental US of 48 states that plots the average arrival delay in minutes. The size of the dot indicates the length of the average delay. A dot in larger size indicates longer average arrival delay at a given airport.

- Card 2: A bar plot that shows the average arrival delay in minutes by airport. From this plot, we found out the top 5 airports that have longest average arrival delay. This card was not originally included in the story. But one of the feedback mentioned that there are gap between card 1 and card 2 so I added a card between these two and show a bar plot of the average arrival delay in minutes so that reader understands how I chose the five airports in card 3.

- Card 3: In this plot, there are five big columns for each airport. And then in each airport, I added the delay categories: weather, security, and carrier. I think in this design, we can not only compare across airports, but also compare the delay categories within each airport. Percentage of each delay category out of the arrival delay. Here we see that for each airport, carrier delay is count as the majority of the arrival delays. Chicago has the lowest percentage of delays due to carrier but delays due to weather is higher compare to other airports.

- Card 4: A map of continental US of 48 states with arrival delay by airlines. This plot is the average arrival delay by different airline and airport. The legend shows color for each airline. In the map, we can also see the circles are separated into rings of different colors. This can give us a clue of which airline has the most delays for a certain airport.


## Feedback

- 1. The airport was originally sorted alphabetically instead of descending according to arrival delay time. This causes confusion and hard to locate the top 5 airports with highest average delay time. So with this feedback, I change the sorting from alphabetically to descending order by arrival delay.
- 2. Card 3: Color for each delay category were the same. In response to this feedback, I used one color for each delay category for easier between group comparison.
- 3. Card 3: Originally, I plotted the average arrival delay for weather, security and carrier. However, the minutes for security was really small and the number for carrier delay was very large. So the bar for security delay was very small and hard to see. For this feedback, I calculated the percentage of delay for each category out of the total arrival delay minutes and plot the percentage. This helps adjust the scale of the variables.

## Resources
[Tableau tutorials](https://www.tableau.com/learn/training)
