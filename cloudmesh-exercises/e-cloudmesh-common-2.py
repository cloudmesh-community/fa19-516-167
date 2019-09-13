# fa19-516-167 
# E.Cloudmesh.Common.2
# Objective: Develop a program that demonstartes the use of dotdict.

# Imports
from cloudmesh.common.dotdict import dotdict

# Sample JSON data
data = [
  {
  "org": "Amazon",
  "address": {
    "street1": "123 aws avenue",
    "city": "Seattle",
    "zip": "12345",
    "country": "United States",
    "countryCode": "US"
  }},
  {
  "org": "Microsoft",
  "address": {
    "street1": "456 azure street",
    "city": "Redmond",
    "zip": "54321",
    "country": "United States",
    "countryCode": "US"
  }}
]

# Convert to dotdict and Print JSON data
dotdict_data = dotdict(data[0])
print(type(dotdict_data))
print(dotdict_data)