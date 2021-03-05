# taxee-api-python-wrapper
A python wrapper for the Taxee Api

check out the API at "https://taxee.io/"

How to use...

```
from taxee import Taxee, SINGLE, MARRIED

api_key = 'your api key'
taxee = Taxee(api_key)

pay_rate = 100000

fed = taxee.get_federal_tax_brackets(year=2020)
state = taxee.get_state_tax_brackets(year=2020, 'NJ')
income_tax = taxee.get_income_tax(year=2020, pay_rate, SINGLE, 'NJ')
```

if an api key is not specified it will then check to see if there is an environment variable called TAXEE_API_KEY

