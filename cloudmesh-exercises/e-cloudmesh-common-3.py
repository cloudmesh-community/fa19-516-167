# fa19-516-167
# E.Cloudmesh.Common.3
# Objective: Develop a program that demonstartes the use of FlatDict.

# Imports
from cloudmesh.common.FlatDict import FlatDict #there is a typo in the book 'Flatdict'

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

# Convert to FlatDict and Print JSON data
flatdict_data = FlatDict(data[0])
print(type(flatdict_data))
print(flatdict_data)