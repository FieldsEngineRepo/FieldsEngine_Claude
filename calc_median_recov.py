import globaldata as gd

def update_median_recov_factor(debug=False):
	conn = gd.get_connection()
	curr = conn.cursor()
	resource_types = gd.get_data('resource_type', 'asset_data', cursor=curr, sql_where='resource_type IS NOT NULL')
	sql_update = "UPDATE asset_data SET avg_recov_factor={} WHERE resource_type='{}' AND `status`='Discovered' AND reserve_type IN ('Gas in Place', 'Oil in Place', 'Prospective');"
	for resource_type in resource_types:
		recov_factors = gd.get_data('recov_factor', 'asset_data', cursor=curr, distinct=False, datatype='float', sql_where="resource_type='{}' AND IFNULL(recov_factor,0)>0".format(resource_type))
		if len(recov_factors):
			median_recov_factor = gd.get_median(recov_factors)
		else:
			median_recov_factor = 0.285
		if debug: print sql_update.format(median_recov_factor, resource_type)
		curr.execute(sql_update.format(median_recov_factor, resource_type))
		gd.commit(curr)
	curr.close()
	conn.close()
	

if __name__=='__main__':
	'''
	CBM: 0.13603
	Conventional Gas: 0.53292
	Conventional Oil: 0.29244
	Heavy Oil: 0.1144
	Oil Sands 0.11049
	Unconventional Gas 0.12859
	Unconventional Oil 0.0561

	'''
	update_median_recov_factor(debug=True)
