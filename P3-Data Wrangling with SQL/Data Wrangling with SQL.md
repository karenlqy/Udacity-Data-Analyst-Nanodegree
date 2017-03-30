## OpenStreetMap Data Case Study with SQL
Author: Qingyu Li

Date: Mar 30 2017
### Map Area
Chicago, IL United States
- The OpenStreetMap Project: https://www.openstreetmap.org/relation/122604#map=10/41.8343/-87.7334
- Data Extract: https://mapzen.com/data/metro-extracts/metro/chicago_illinois/

I have lived in Chicago city for two years now and I would like to learn more about this windy city. 

After downloading the osm data, which is about 2G, we created a sample set of 

defaultdict(set,
            {'59': {'S IL State Route 59'},
             'Ave': {'Arkansas Ave', 'Deleware Ave', 'Meridian Ave'},
             'B': {'South Avenue B'},
             'Broadway': {'North Broadway'},
             'C': {'South Avenue C'},
             'Center': {'Yorktown Shopping Center'},
             'Ct': {'Leadville Ct', 'Telluride Ct'},
             'D': {'South Avenue D'},
             'Dr': {'Alpine Dr',
              'Augusta Dr',
              'Gregory M Sears Dr',
              'Marketview Dr',
              'Meadows Dr'},
             'E': {'South Avenue E'},
             'F': {'South Avenue F'},
             'G': {'South Avenue G'},
             'H': {'South Avenue H'},
             'Highway': {'North Northwest Highway'},
             'J': {'South Avenue J'},
             'K': {'South Avenue K'},
             'L': {'South Avenue L'},
             'Ln': {'Leadville Ln'},
             'M': {'South Avenue M'},
             'N': {'South Avenue N'},
             'O': {'South Avenue O'},
             'Park': {'West Midway Park'},
             'Rd': {'Powers Rd'},
             'St': {'Pierce St', 'Tipperary St'},
             'St.': {'Valley View St.'},
             'Terrace': {'Harvard Terrace',
              'North Geneva Terrace',
              'West Jonquil Terrace',
              'West Junior Terrace',
              'West Westgate Terrace'},
             'Way': {'Woodridge Way'},
             'West': {'North Lincoln Park West'},
             'roosevelt': {'roosevelt'}})

We can see that there are a lot of inconsistencies in the way street is recorded:
   - Street names with suite numbers. Example: Renaissance Drive #103
   - There are zip codes in the street name tag. Example: 60008
   - Street name abbrevations. 
       - "E North Ave" instead of "East North Avenue"
       - "Aspen Cir" instead of "Aspen Circle"
