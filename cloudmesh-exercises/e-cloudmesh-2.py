# fa19-516-167 E.Cloudmesh.Common.2
# Objective: Develop a program that demonstartes the use of dotdict.

# Imports
from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.FlatDict import FlatDict #there is a typo in the book 'Flatdict'
from cloudmesh.common.Printer import Printer

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

# Convert to FlatDict and Print JSON data
flatdict_data = FlatDict(data[0])
print(type(flatdict_data))
print(flatdict_data)

# Printing Dicts
table = Printer.flatwrite(data, sort_keys=["org"]
  ,order=["org", "address.street1", "address.city"]
  ,header=["Name", "Street", "City"]
  ,output='table')

print(table)
