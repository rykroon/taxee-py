import os

import requests
from requests.auth import AuthBase


SINGLE = 'single'
MARRIED = 'married'
MARRIED_SEPARATELY = 'married_separately'
HEAD_OF_HOUSEHOLD = 'head_of_household'

FILING_STATUSES = (
    SINGLE, 
    MARRIED, 
    MARRIED_SEPARATELY, 
    HEAD_OF_HOUSEHOLD
)


STATES = (
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
)


class Taxee:

    def __init__(self,api_key=None):
        self.api_key = api_key or os.getenv('TAXEE_API_KEY')
        self.auth = TaxeeAuth(self.api_key)
        self.base_url = 'https://taxee.io/api/v2'

    def get_federal_tax_brackets(self, year):
        #returns the response from the taxee api's Federal Tax Brackets
        url = '{}/federal/{}'.format(self.base_url, year)
        resp = requests.get(url, auth=self.auth)
        if not resp.ok:
            raise TaxeeError(resp.content)
        return resp.json()

    def get_state_tax_brackets(self, year, state_abbreviation):
        #returns the response from the taxee api's State Tax Brackets
        url = '{}/state/{}/{}'.format(self.base_url, year, state_abbreviation)
        resp = requests.get(url, auth=self.auth)
        if not resp.ok:
            raise TaxeeError(resp.content)
        return resp.json()

    def get_income_tax(self, year, **kwargs):
        #returns a request from the income tax part of the API
        url = '{}/calculate/{}'.format(self.base_url, year)
        resp = requests.post(url, auth=self.auth, json=kwargs)
        if not resp.ok:
            raise TaxeeError(resp.content)
        return resp.json()


class TaxeeAuth(AuthBase):
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, req):
        req.headers['Authorization'] = 'Bearer {}'.format(self.api_key)
        return req


class TaxeeError(Exception):
    pass
