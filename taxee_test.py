from taxee import Taxee

api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBUElfS0VZX01BTkFHRVIiLCJodHRwOi8vdGF4ZWUuaW8vdXNlcl9pZCI6IjVhZGI1N2EyNTZhOTBlMDc3Yjk1MTc0NCIsImh0dHA6Ly90YXhlZS5pby9zY29wZXMiOlsiYXBpIl0sImlhdCI6MTUyNDMyNDI1OH0.L5po7FlCskM3n5QynHv3_P1gszmYNKlMwoYfekIWht0'
taxee = Taxee(api_key)

#federal_tax_response = taxee.get_federal_tax_brackets(2018)

#print(federal_tax_response.content)
#
federal_tax = taxee.federal_tax_brackets(2016)
#print(federal_tax_obj.json())


for bracket in federal_tax['single'].tax_brackets:
    print(bracket.amount)

print('\n')
nj_tax = taxee.get_state_tax_brackets(2017,'NJ')

#print(nj_tax.json())

income_tax = taxee.income_tax(2018,68000,'single','NJ')

print(income_tax.year)
print(income_tax.gross)
print(income_tax.state)
print(income_tax.fica_tax)
print(income_tax.federal_tax)
print(income_tax.state_tax)
print(income_tax.net_income())

# for bracket in nj_tax['single'].tax_brackets:
#     print(bracket.bracket)
#     print(bracket.marginal_rate)
#     print(bracket.amount)
