from globaldata import *

test_config  = {
	1: (0, 1, 1),
	2: (0, 0, 1),
	3: (0, 0, 2),
	4: (0, 0, 3),
	5: (1, 1, 1),
	6: (1, 0, 1),
	7: (1, 0, 2),
	8: (1, 0, 3)
}

arps_group_config = {
	'A': {test_num: (0,) + test_config[test_num] + ('A', test_num) for test_num in test_config.keys()},
	'B': {test_num: (1,) + test_config[test_num] + ('B', test_num) for test_num in test_config.keys()}
}

def run_decline_tests():
    conn = get_connection()
    curr = conn.cursor()
    run_id = get_run_id()
    sql_update = 'UPDATE global_variables SET end_as_arps_initial={}, use_last_decline={}, allow_final_value_peak={}, gen_after_peak_type={} '
    for group in 'AB':
        group_config = arps_group_config[group]
        for test_num in range(1,9):
            print 'Running arps decline test for group-id {}{} ...'.format(group, test_num)
            new_run_id = '{}{}{}'.format(run_id[:13], group, test_num)
            os.system('%cmd% runid {}'.format(new_run_id))
            curr.execute(sql_update.format(*group_config[test_num]))
            commit(curr)
            try:
                os.system('%cmd% create_model -arps-')
            except:
                print 'test failed for {}{}'.format(group, test_num)
    curr.close()
    conn.close()

if __name__ == '__main__':
    run_decline_tests()