# taxee-api-python-wrapper
A python wrapper for the Taxee Api

check out the API at "https://taxee.io/"

How to use...

from taxee import Taxee

api_key = 'your api key'
taxee = Taxee(api_key)

if an api key is not specified it will then check to see if there is an environment variable called TAXEE_API_KEY

