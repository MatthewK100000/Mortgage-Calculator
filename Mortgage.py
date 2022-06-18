import numpy as np 
import pandas as pd 
from scipy.optimize import newton,bisect
from scipy.special import comb
from math import log
from datetime import date
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt 
import warnings


warnings.simplefilter("always")


class ExcessParameterFound(UserWarning):
	pass


class FixedRateCalculator:

	def __init__(self, **kwargs):

		self._check_parameter_validity(**kwargs)

		arguments = kwargs.keys()

		if {'loan_size', 'interest_rate', 'monthly_payment', 'num_months'}.issubset(arguments):
			self.loan_size = kwargs['loan_size']
			self.interest_rate = kwargs['interest_rate']
			self.monthly_payment = kwargs['monthly_payment']
			self.num_months = kwargs['num_months']


		elif {'loan_size','interest_rate','num_months'}.issubset(arguments) and ('monthly_payment' not in arguments):
			self.loan_size = kwargs['loan_size']
			self.interest_rate = kwargs['interest_rate']
			self.num_months = kwargs['num_months']

			self.monthly_payment = self._solve_for_monthly_payment()


		elif {'monthly_payment','num_months','interest_rate'}.issubset(arguments) and ('loan_size' not in arguments):
			self.monthly_payment = kwargs['monthly_payment']
			self.interest_rate = kwargs['interest_rate']
			self.num_months = kwargs['num_months']

			self.loan_size = self._solve_for_principal()


		elif {'loan_size','monthly_payment','interest_rate'}.issubset(arguments) and ('num_months' not in arguments):
			self.loan_size = kwargs['loan_size']
			self.monthly_payment = kwargs['monthly_payment']
			self.interest_rate = kwargs['interest_rate']

			self.num_months = self._solve_for_months()


		elif {'loan_size','monthly_payment','num_months'}.issubset(arguments) and ('interest_rate' not in arguments):
			self.loan_size = kwargs['loan_size']
			self.monthly_payment = kwargs['monthly_payment']
			self.num_months = kwargs['num_months']

			poly = self._construct_interest_rate_poly()
			poly_deriv = self._construct_interest_rate_poly_deriv()
			self.interest_rate = self._solve_for_interest_rate(poly, poly_deriv)
			if self.interest_rate < 0:
				warnings.warn("Negative interest rate returned. The monthly payment times the number of months is less than the size of the loan.", UserWarning)
			elif self.interest_rate > 0.10:
				warnings.warn("Interest rate is unusually high (> 10%). The monthly payment times the number of months is much greater than the size of the loan.", UserWarning)
			elif self.interest_rate < 0.005:
				warnings.warn("Interest rate is unusually small (< 0.5%).", UserWarning)
			else:
				pass


		else:
			raise Exception("Not enough parameters. Expect all or three of `loan_size`, `monthly_payment`, `num_months`, `interest_rate`.")



	def amortization_schedule(self, start_year = None, start_month = None):

		if (start_year is not None) and (start_month is not None):
			if (not isinstance(start_year,int)) and (not isinstance(start_month,int)):
				raise Exception("`start_year` and `start_month` must be integers.")
			elif start_month not in {i for i in range(1,13)}:
				raise Exception("`start_month` must be a valid month.")

			data = {
			'Month': [(date(year = start_year, month = start_month, day = 1) + relativedelta(months=i)).strftime('%b %Y') for i in range(0,self.num_months)],
			'Payment': [self.monthly_payment for i in range(1,self.num_months+1)],
			'Principal': [self.principal_payed_per_month(i) for i in range(1,self.num_months+1)],
			'Interest': [self.interest_payed_per_month(i) for i in range(1,self.num_months+1)]
			}

		else:
			data = {
			'Month': [i for i in range(1,self.num_months + 1)],
			'Payment': [self.monthly_payment for i in range(1,self.num_months + 1)],
			'Principal': [self.principal_payed_per_month(i) for i in range(1,self.num_months + 1)],
			'Interest': [self.interest_payed_per_month(i) for i in range(1,self.num_months + 1)]
			}

		schedule = pd.DataFrame(data)
		schedule['Balance'] = self.loan_size - schedule.loc[:,['Principal']].cumsum()
		schedule['Total Interest'] = schedule.loc[:,['Interest']].cumsum()
		schedule['% ownership'] = 100*(1 - schedule['Balance']/self.loan_size)
		return schedule.loc[:,['Month','Payment','Principal','Interest','Balance','Total Interest','% ownership']]



	def total_interest_payed(self):
		return self.total_payed_to_lender() - self.loan_size



	def total_payed_to_lender(self):
		return self.monthly_payment*self.num_months



	def interest_payed_per_month(self,month):
		if not isinstance(month,int):
			raise Exception("`month` must be integer greater than 0.")
		elif month < 1:
			raise Exception("`month` must be integer greater than 0.")
		else:
			pass

		return (self.loan_size*self.interest_rate/12 - self.monthly_payment)*(1 + self.interest_rate/12)**(month - 1) + self.monthly_payment



	def principal_payed_per_month(self, month):
		if not isinstance(month,int):
			raise Exception("`month` must be integer greater than 0.")
		elif month < 1:
			raise Exception("`month` must be integer greater than 0.")

		return self.monthly_payment - self.interest_payed_per_month(month)



	@classmethod
	def limit_on_interest_payed(cls, loan_size, num_months, limit_on_interest):
		
		cls._check_parameter_validity(**{'loan_size':loan_size, 'num_months': num_months})

		if (not isinstance(limit_on_interest,int)) and (not isinstance(limit_on_interest,float)):
			raise Exception("Parameter `limit_on_interest` must be int/float and above zero.")
		else:
			if limit_on_interest < 0:
				raise Exception("Parameter `limit_on_interest` must be int/float and above zero.")


		monthly_payment = loan_size + limit_on_interest
		monthly_payment /= num_months

		mortgage_instance = cls(loan_size = loan_size, monthly_payment = monthly_payment, num_months = num_months)

		print('For a loan of size: {}, '.format(loan_size))
		print('and a limit of {} (total payment to lender {}), '.format(limit_on_interest, loan_size + limit_on_interest))
		print('on a time period of {} months, '.format(num_months))
		print('amounting to a monthly payment of {}, '.format(monthly_payment))
		print('...')
		print('the time to realize that opportunity is when the interest rate reaches {}%'.format(round(100*mortgage_instance.interest_rate,3)))

		return mortgage_instance



	def _solve_for_monthly_payment(self):
		return (self.loan_size*(self.interest_rate/12)*(1 + self.interest_rate/12)**self.num_months) / ((1 + self.interest_rate/12)**self.num_months - 1)



	def _solve_for_principal(self):
		return self.monthly_payment*((1 + self.interest_rate/12)**self.num_months - 1) / ((self.interest_rate/12)*(1 + self.interest_rate/12)**self.num_months)



	def _solve_for_months(self):
		return int(-log(1 - ((self.interest_rate/12)*self.loan_size/self.monthly_payment)) / log(1 + self.interest_rate/12))



	def _construct_interest_rate_poly(self):
		coeff =  np.append( self.monthly_payment*comb(N = self.num_months, k = np.arange(1,self.num_months+1)) - self.loan_size*comb(N = self.num_months, k = np.arange(0,self.num_months)), -self.loan_size)[::-1]
		return np.poly1d(coeff)



	def _construct_interest_rate_poly_deriv(self):
		coeff = np.append( np.arange(1,self.num_months) * ( self.monthly_payment*comb(N = self.num_months, k = np.arange(2,self.num_months+1)) - self.loan_size*comb(N = self.num_months, k = np.arange(1,self.num_months)) ), -self.num_months*self.loan_size)[::-1]
		return np.poly1d(coeff)



	@staticmethod
	def _solve_for_interest_rate(poly,poly_deriv,x0 = 0.5, maxiter = 100):
		root, result = newton(func = poly,
								x0 = x0,
								fprime = poly_deriv,
								maxiter = maxiter,
								full_output = True,
								disp = False
							) 

		if not result.converged:
			# fallback to bisection method

			root, result = bisect(f = poly,
									a = 0,
									b = 1,
									maxiter = maxiter,
									full_output = True,
									disp = False
								)

			if not result.converged:
				raise Exception("Bisection method is the last resort after Newton's method, and the root finder did not converge.")

		return 12*root



	@classmethod
	def from_down_payment_and_total(cls, **kwargs):

		if not {'total','down_payment'}.issubset(kwargs.keys()):
			raise Exception("Parameter `total` and `down_payment` not detected. Please provide these parameters in this alternative constructor.")

		if 'loan_size' in kwargs.keys():
			raise warnings.warn("Unused parameter `loan_size` detected. Provided value will be overwritten.",ExcessParameterFound)

		new_kwargs = kwargs
		new_kwargs.pop('loan_size',None)

		if (not isinstance(new_kwargs['total'], float)) and (not isinstance(new_kwargs['total'],int)):
			raise Exception("Parameter `total` must be float/int and above zero.")
		
		if new_kwargs['total'] <= 0:
			raise Exception("Parameter `total` must be float and above zero.")

		if (not isinstance(new_kwargs['down_payment'],float)) and (not isinstance(new_kwargs['down_payment'],int)):
			raise Exception("Parameter `down_payment` must be float and above zero.")

		if new_kwargs['down_payment'] <= 0:
			raise Exception("Parameter `down_payment` must be float and above zero.")

		if new_kwargs['down_payment'] >= new_kwargs['total']:
			raise Exception("Parameter `total` must be greater than parameter `down_payment`.")

		new_kwargs['loan_size'] = new_kwargs['total'] - new_kwargs['down_payment']
		del new_kwargs['total']
		del new_kwargs['down_payment']

		return cls(**new_kwargs)


	@staticmethod
	def check_down_payment_and_total()



	@staticmethod
	def _check_parameter_validity(**kwargs):

		for arg in kwargs.keys():
			if arg == 'loan_size':
				error_message = "Parameter `loan_size` must be int/float and above zero."

				if (not isinstance(kwargs['loan_size'],float)) and (not isinstance(kwargs['loan_size'],int)):
					raise Exception(error_message)
				else:
					if kwargs['loan_size'] <= 0:
						raise Exception(error_message)

			elif arg == 'interest_rate':
				error_message = "Parameter `interest_rate` must be float between 0 and 1 (exclusive)."

				if not isinstance(kwargs['interest_rate'],float):
					raise Exception(error_message)
				else:
					if kwargs['interest_rate'] >= 1 or kwargs['interest_rate'] <=0:
						raise Exception(error_message)

			elif arg == 'monthly_payment':
				error_message = "Parameter `monthly_payment` must be int/float and above zero."

				if (not isinstance(kwargs['monthly_payment'], float)) and (not isinstance(kwargs['monthly_payment'],int)):
					raise Exception(error_message)
				else:
					if kwargs['monthly_payment'] <= 0:
						raise Exception(error_message)

			elif arg == 'num_months':
				error_message = "Parameter `num_months` must be int and at least one month."

				if not isinstance(kwargs['num_months'], int):
					raise Exception(error_message)
				else:
					if kwargs['num_months'] < 1:
						raise Exception(error_message)

			else:
				warnings.warn("Unused parameter `{}` was detected.".format(arg),ExcessParameterFound)
