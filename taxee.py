import requests
import os

class Taxee():

    def __init__(self,api_key=None):
        if api_key is not None:
            self.API_KEY = api_key
        else:
            try:
                self.API_KEY = os.environ['TAXEE_API_KEY']
            except:
                self.API_KEY = None

        self.header = dict()
        self.header['Authorization'] = 'Bearer ' + str(self.API_KEY)

        self.base_url = 'https://taxee.io/api/v2/'


    #returns the response from the taxee api's Federal Tax Brackets
    def get_federal_tax_brackets(self,year):
        url = self.base_url + '/federal/' + str(year)
        return requests.get(url,headers=self.header)

    #returns a dictionary of TaxStatistic instances
    def federal_tax_brackets(self,year):
        response = self.get_federal_tax_brackets(year)

        if response.status_code == 200:
            data = response.json()
        else:
            return None

        result = dict()

        for filing_status, data in data.items():
            tax_statistic = TaxStatistic(filing_status,year,data)
            result[filing_status] = tax_statistic

        return result

    #returns the response from the taxee api's State Tax Brackets
    def get_state_tax_brackets(self,year,state_abbreviation):
        url = self.base_url + '/state/' + str(year) + '/' + state_abbreviation
        return requests.get(url,headers=self.header)

    #returns a dictionary of TaxStatistic instances
    def state_tax_brackets(self,year,state):
        response = self.get_state_tax_brackets(year,state)

        if response.status_code == 200:
            data = response.json()
        else:
            return None

        result = dict()

        for filing_status, data in data.items():
            tax_statistic = TaxStatistic(filing_status,year,data,state=state)
            result[filing_status] = tax_statistic

        return result

    #returns a request from the income tax part of the API
    def post_income_tax(self,year,pay_rate,filing_status,state):
        url = self.base_url + 'calculate/' + str(year)
        data = {'pay_rate':pay_rate,'filing_status':filing_status,'state':state}
        return requests.post(url,headers=self.header,data=data)

    #returns an instance of IncomeTax
    def income_tax(self,year,pay_rate,filing_status,state):
        response = self.post_income_tax(year,pay_rate,filing_status,state)

        if response.status_code == 200:
            data = response.json()
        else:
            return None

        fica_tax    = data['annual']['fica']['amount']
        federal_tax = data['annual']['federal']['amount']
        state_tax   = data['annual']['state']['amount']

        return IncomeTax(year,pay_rate,filing_status,state,fica_tax,federal_tax,state_tax)




class IncomeTax():
    def __init__(self,year,gross,filing_status,state,fica_tax,federal_tax,state_tax):
        self.year           = year
        self.filing_status  = filing_status
        self.state          = state
        self.gross          = gross
        self.fica_tax       = fica_tax
        self.federal_tax    = federal_tax
        self.state_tax      = state_tax

    def net_income(self):
        return self.gross - self.fica_tax - self.federal_tax - self.state_tax


class TaxStatistic():
    def __init__(self,filing_status,year,data,state=None):
        self.filing_status = filing_status
        self.year = year
        self.state = state

        self.deductions = list()
        self.tax_brackets = list()
        self.exemptions = list()

        self.__build__(data)


    def __build__(self,data):
        for component, array in data.items():

            if component == 'income_tax_brackets':
                for tax_bracket_data in array:
                    tax_bracket = self.__create_tax_bracket__(tax_bracket_data)
                    self.tax_brackets.append(tax_bracket)

            if component == 'deductions':
                for deduction_data in array:
                    deduction = self.__create_deduction__(deduction_data)
                    self.deductions.append(deduction)

            if component == 'exemptions':
                for exemption_data in array:
                    exemption = self.__create_exemption__(exemption_data)
                    self.exemptions.append(exemption)


    def __create_tax_bracket__(self,data):
        try:    bracket = data['bracket']
        except: bracket = None

        try:    marginal_rate = data['marginal_rate']
        except: marginal_rate = None

        try:    marginal_capital_gain_rate = data['marginal_capital_gain_rate']
        except: marginal_capital_gain_rate = None

        try:    amount = data['amount']
        except: amount = None

        return IncomeTaxBracket(bracket,marginal_rate,marginal_capital_gain_rate,amount)


    def __create_deduction__(self,data):
        try:    name = data['deduction_name']
        except: name = None

        try:    amount = data['deduction_amount']
        except: amount = None

        return Deduction(name,amount)


    def __create_exemption__(self,data):
        try:    name = data['exemption_name']
        except: name = None

        try:    amount = data['exemption_amount']
        except: amount = None

        return Exemption(name,amount)

    def __str__(self):
        result = "Tax Statistics for " + self.filing_status + " filers for year " + str(self.year);
        if self.state is not None: rest += " in " + self.state
        return result


class Deduction():
    def __init__(self,name,amount):
        self.name = name
        self.amount = amount

class Exemption():
    def __init__(self,name,amount):
        self.name = name
        self.amount = amount

class IncomeTaxBracket():
    def __init__(self,bracket,marginal_rate,marginal_capital_gain_rate,amount):
        self.bracket = bracket
        self.marginal_rate = marginal_rate
        self.marginal_capital_gain_rate = marginal_capital_gain_rate
        self.amount = amount

if __name__ == "__main__":
    print("Name = " + __name__)
else:
    print("Name = " + __name__)
