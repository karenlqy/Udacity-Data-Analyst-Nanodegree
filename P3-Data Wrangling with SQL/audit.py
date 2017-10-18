n"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "philadelphia_pennsylvania.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
           "Sstreet":"Street",
            "Ave": "Avenue",
           "Ave.": "Avenue",
             "avenue": "Avenue",
            "ave": "Avenue",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
           "blvd": "Boulevard",
            "Bouevard": "Boulevard",
            "Boulavard": "Boulevard",
            "Boulvard": "Boulevard",
            "Rd.": "Road",
            "Rd": "Road",
           "RD": "Road",
           "rd": "Road",
           "road": "Road",
            "st": "Street",
           "Street.": "Street", 
           "street": "Street",
           "Sts":"Street",
           "Pkwy": "Parkway", 
           "Ct": "Court", 
           "Cir": "Circle",
           "Dr": "Drive", 
           "Dr.": "Drive", 
           "Hwy": "Highway",
           "Hwy.": "Highway",
           "Ln": "Lane",
           "Line":"Lane",
           "L":"Lane",
            "Ln.": "Lane",
           "PIke":"Pike",
            "Pl": "Place",
           "PLACE": "Place",
           "place":"Place",
            "Plz": "Plaza",
            "Rd": "Road",
            "Rd.": "Road",
            "St": "Street",
            "St.": "Street",
            "st": "Street",
           "ST": "Street",
            "street": "Street",
            "square": "Square",
            "parkway": "Parkway",
            "N.": "North",
            "N": "North",
            "E.": "East",
            "E": "East",
            "S.": "South",
            "S": "South",
            "W.": "West",
            "W": "West",
           "way":"Way"
            }



def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(OSM_PATH):
    osm_file = open(OSM_PATH, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

def update_name(name, mapping):
    """takes an old name to mapping dictionary, and update to a new one"""
    
    m = street_type_re.search(name)
    if m:
        for a in mapping:
            if a == m.group():
                name = re.sub(street_type_re, mapping[a], name)
    name = re.split(",|#|-",name)[0]
    return name


def is_postcode(elem):
    """check if elem is a postcode"""
    return (elem.attrib['k'] == "addr:postcode" or elem.attrib['k'] == "postal_code")

def audit_postcode(postcodes, postcode):
    """ Get a full list of entries about postcode """
    postcodes[postcode].add(postcode)
    return postcodes


def update_postcode(postcode):
    """Clean postcode to a uniform format of 5 digit; Return updated postcode"""
    if re.findall(r'^\d{5}$', postcode): # 5 digits
        valid_postcode = postcode
        return valid_postcode
    elif re.findall(r'(^\d{5})-\d{4}$', postcode): # 9 digits
        valid_postcode = re.findall(r'(^\d{5})-\d{4}$', postcode)[0]
        return valid_postcode
    elif re.findall(r'PA\s*\d{5}', postcode): # with state code PA
        valid_postcode =re.findall(r'\d{5}', postcode)[0]  
        return valid_postcode  
    else:
        return None
