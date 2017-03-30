## OpenStreetMap Data Case Study with SQL
Author: Qingyu Li

Date: Mar 30 2017
### Map Area
Chicago, IL United States
- The OpenStreetMap Project: https://www.openstreetmap.org/relation/122604#map=10/41.8343/-87.7334
- Data Extract: https://mapzen.com/data/metro-extracts/metro/chicago_illinois/

I have lived in Chicago city for two years now and I would like to learn more about this windy city. 

After downloading the osm data, which is about 2G, we created a sample set of 

### Problems Encountered in Map and Data Cleaning

We can see that there are a lot of inconsistencies in the way street is recorded:
   - Street names with suite numbers. Example: Renaissance Drive #103
   - There are zip codes in the street name tag. Example: 60008
   - Street name abbrevations. 
       - "Deleware Ave" instead of "Deleware Avenue"
       - "Augusta Dr" instead of "Augusta Drive"
      
#### 

####

#### Create SQL database from cleaned XML data



### Overview of Database


### Learn More about Chicago
##
```sql
sqlite> SELECT * FROM nodesTags WHERE id="3443667462";
```
