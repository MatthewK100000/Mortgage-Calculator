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
- ``interest_rate``: The annual interest rate, not the APR.
- ``monthly_payment``: The monthly payment

You may provide all four arguments or just three 

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
