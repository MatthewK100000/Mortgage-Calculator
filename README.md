# Mortgage-Calculator
A class which provides convenient methods to solve for and visualize fixed rate mortgage inquiries

## Usage
### Header
``` python
from Mortgage import FixedRateCalculator
```

### Instantiation
There are four main arguments: 
- ``loan_size``: Size of the loan.
- ``num_months``: Duration of the mortgage in months.
- ``interest_rate``: The annual interest rate, not the APR. Between 0 and 1.
- ``monthly_payment``: The monthly payment


You may provide all four arguments or just three. Any missing argument will be completely determined by the three arguments submitted. Submitting any three arguments, with the last one to be determined, is like framing different questions. See the following examples.

#### Solving For the Monthly Payment
Let's say you want to take a loan out for $200,000 at an annual interest rate of 3%. How much would you have to pay per month if you want to pay it off by 15 years (180 months)?
```python
mortgage = FixedRateCalculator(loan_size = 200_000, interest_rate = 0.03, num_months = 180)
print(mortgage.monthly_payment) # prints 1381.1632805560034
```
So you'd have to pay about $1,381.16 per month.

#### Solving For the Size of the Loan
Now, let's say you are able to pay no more than $1,500 per month for a 30 year loan, with the annual interest rate sitting at 5%. What loan can you afford to take?
```python
mortgage = FixedRateCalculator(monthly_payment = 1_500, num_months = 360, interest_rate = 0.05)
print(mortgage.loan_size) # prints 279422.4255691129
```
Looks like you the biggest loan you can afford to take is about $279,422. 

#### Solving for the Duration
You have a loan out for $200,000 sitting at an annual interest rate of 1.32%. You want to pay it off as soon as possible, but can't afford to pay more than $1,900 per month. How long will it take for you to pay it off?
```python
mortgage = FixedRateCalculator(loan_size = 200_000, interest_rate = 0.0132, monthly_payment = 1_900)
print(mortgage.num_months) # prints 111
```
You'll pay it off by 111 months, or 9.25 years. 

#### Solving for the Interest Rate
This one is interesting. Suppose you missed out on the low interest rates. You want to buy a home for $150,000, pay it off by 10 years with a monthly payment at $1,375. When the interest rates start coming down again, at one point must you take that loan out?
```python
mortgage = FixedRateCalculator(loan_size = 150_000, num_months = 120, monthly_payment = 1_375)
print(round(100*mortgage.interest_rate,2),'%') # prints 1.92%
```
So you must run to the bank when the annual interest rate reaches 1.92%. 

The above examples ignore the possibility of lower rates and refinancing, but at least give you a picture of the kind of parameters you can operate in and plan accordingly.

### From Limit on Interest

alternative constructor investor standpoint

### Total Payed and Interest Payed


### Amortization schedule



## Recommended Dependencies
- Python (3.6.4 or greater)
  - [warnings](https://docs.python.org/3.6/library/warnings.html), [math](https://docs.python.org/3.6/library/math.html), [datetime](https://docs.python.org/3.6/library/datetime.html?highlight=datetime#module-datetime)
- [NumPy](https://numpy.org/) (version 1.15.3 or greater)
- [SciPy](https://scipy.org/) (version 1.5.4 or greater)
- [Pandas](https://pandas.pydata.org/) (version 0.25.3 or greater)
- [Dateutil](https://dateutil.readthedocs.io/en/stable/) (version 2.7.3 or greater)

## Underlying Math
Since github markdown does not currently support latex formulas, you may view the mathematical appendix [here](https://github.com/MatthewK100000/Mortgage-Calculator/blob/main/Math/mathematical%20background%20v1.0.pdf).
