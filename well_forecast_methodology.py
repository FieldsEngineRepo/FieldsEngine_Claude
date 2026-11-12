
Well Production Forecasting

Input: 
	- Monthly production data by well for individual commodities
		- Forecast only Crude Oil, Natural Gas, Condensate, NGLs, LNG
		- Only active producing wells?
	- Cost inputs by well
		- Stored in US_Wells.dbo.tblUSWell_TypeInputs
		- Stored in global_well_variables (US_Wells.dbo.tblUSWell_GlobalVariables)
		- Stored in other tables?
	- Commodity prices
		- Stored in US_Wells.dbo.tblUSWell_Prices and US_Wells.dbo.tblUSWell_PricesValue
Output: 
	- Best-fitting arps decline curve annualized and projected to end of well life (default of 25 years?) by commodity
	- EUR Crude Oil, EUR Natural Gas, EUR Condensate, EUR NGLs, Total EUR
	- Gross revenue, Capex, Opex, Pre-tax Cash Flow, Discounted Pre-tax Cash Flow, Post-tax Cash Flow, Discounted Post-tax Cash Flow, Fiscal Take, Pre-tax Breakevens, Post-tax Breakevens

Process:
	- Forecast production for each commodity using different decline curve
		- Use get_prod_data() to retrieve all historical production data for each well by commodity >> {commodity: {prod_month: prod_value for prod_month in prod_periods} for commodity in ['Crude Oil', 'Natural Gas', 'Condensate', 'NGLs']}
		- Normalize to peak production month (divide values by peak for peak_% ?)
		- Run each commodity production dataset through find_fit_curve()
	- Annualize production for each commodity
	- Use commodity prices, cost inputs, and commodity production data to generate economic forecast
	- Adjust well life or stop production based on economic limits




# ---------------------------------------------------------------------------------------------------------------
curvefit_data = wa.find_curve_fit(curve_params=self.typewell_curve_params, optimize=False, commodity=self.commodity, store_curve=True)

self.curvefit_id = curvefit_data['curvefit_id']
self.curvefit_prod_data = curvefit_data['curve data']
self.phase_pct = self.decline_curve_inputs['typewell']['{}_phase_pct'.format(self.comm)]['value']

annual_eur_data = wa.annualize_prod_data({self.commodity: self.curvefit_prod_data}, phase_split=self.phase_pct, main_comm=self.comm)

self.annual_prod_data = annual_eur_data
self.getTypewellCostInputs()

eur_totals = wa.get_eur_totals(annual_eur_data)
self.updateEURtotals(eur_totals)

if self.commodity == 'Crude Oil':
    comm_id = '1'
else:
    comm_id = '2'

self.typewell_econ_outputs[self.comm]['pretax_npv']['value'], self.typewell_econ_outputs[self.comm]['pretax_irr']['value'], self.well_econ = wa.calc_well_economics(annual_prod_data=self.annual_prod_data, cost_inputs=self.typewell_cost_inputs[self.comm], curvefit_id=self.curvefit_id)
self.typewell_econ_outputs[self.comm]['pretax_breakeven_oil']['value'], self.typewell_econ_outputs[self.comm]['pretax_breakeven_gas']['value'] = wa.calculate_pre_tax_breakeven(well_econ=self.well_econ, commodity_id=comm_id)
self.setTypewellEconOutputs()


# ---------------------------------------------------------------------------------------------------------------
all_typewell_data, curve_params = wa.generate_type_curve(prod_config=self.data_configs[self.display_id],
														 decline_curve_params=self.typewell_curve_params,
														 store_curve=True, 
														 period_limit_str=self.period_limit_str,
														 prod_limit_str=self.prod_limit_str,
														 well_id_list=self.well_ids)

self.updateCurveParams(curve_params[comm], 'typewell')
self.curvefit_id = curve_params['curvefit_id']
self.typewell_id = curve_params['typewell_id']
self.where_str = curve_params['where_str']
self.sql_prod_data[self.display_id] = self.where_str

self.all_typewell_prod_data = {well_id: all_typewell_data[well_id] for well_id in all_typewell_data.keys() if well_id != 'average_prod_curve'}

self.typewell_prod_data = all_typewell_data['average_prod_curve']
self.curvefit_prod_data = curve_params['curve data']
self.phase_pct = self.decline_curve_inputs['typewell']['{}_phase_pct'.format(self.comm)]['value']
annual_eur_data = wa.annualize_prod_data(self.curvefit_prod_data, phase_split=self.phase_pct, main_comm=self.comm)
self.annual_prod_data = annual_eur_data
eur_totals = wa.get_eur_totals(annual_eur_data)
self.updateEURtotals(eur_totals)
self.costInputsLoad(plot=False)