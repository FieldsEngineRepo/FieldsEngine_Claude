Capex:
	- Take all historical years up to the last year of sourced expenditure and sum total capex using sourced data where available and engine estimate for other years
	historical_capex = sum([annual_capex[capex_year] for capex_year in sourced_capex_years]) + sum([engine_capex[capex_year] for capex_year in engine_capex.keys() if capex_year is not in sourced_capex_years and capex_year < discount_year])
	- Divide this by the sum of the standard engine estimated capex for the same period to get correction factor
	- In model, use sourced capex where available, and adjust other years' engine estimates by multiplying by correction factor
	- Where sourced expenditure is multi-year, allocate according to the spread of engine estimated capex across the same period
Opex:
	- Compare sourced opex to engine estimates for the same year
	- Generate average adjustment factor from these comparisons
	- Adjust both fixed and variable opex estimates by multilpying by this factor
In both these cases we would probably want to say that the adjustment should only be done if the sourced expenditure was in the last 5-10 years, give analysts the option to turn the adjustment off for specific assets, and adjustment is over +/-20%