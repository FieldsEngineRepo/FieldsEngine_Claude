

'''
0. Set plateau_start_indx = plateau_end_indx = -1
1. Start from first point < i=0 >
2. if i is index for last point:
       2a. go to step 4
   else:
       2b. Calculate % change to next value < i/(i+1) >
3. if change is less than 5%:
       if plateau_start_indx == -1
           3a. set plateau_start_indx = i then repeat step 2
       else:
           3b. set plateau_end_indx = i then repeat step 2
   if change is greater than 5%:
       3c. repeat step 2

4. if plateau_start_indx = plateau_end_indx = -1:
       4a. no change to arps_input
   else:
       4b. arps_input = arps_input[:plateau_start_indx] + arps_input[plateau_end_indx:]
'''


PLAT_RANGE_PCT = 0.02

def get_change_pct(data_points, indx_a, indx_b):
    change_pct = 0
    if (indx_a < len(data_points)) and (indx_b < len(data_points)):
        change_pct = float(1 - (float(min(data_points[indx_a], data_points[indx_b])) / float(max(data_points[indx_a], data_points[indx_b]))))
    return change_pct


def collapse_flat_prod(arps_input, debugMode=False):
    prod_input        = []
    plateau_points    = []
    if debugMode:
        print ''
        print '******************************************'
        print 'arps_input: {}'.format(arps_input)
    for i in range(len(arps_input) - 1):
        plat_check_points = list(set(plateau_points + [i + 1]))
        change_pcts = [round(get_change_pct(arps_input, i, j), 3) for j in plat_check_points]
        max_change_pct = max(change_pcts)
        if debugMode:
            print '({})        change_pcts: {}'.format(i, change_pcts)
            print '({})     max_change_pct: {}'.format(i, max_change_pct)
        if max_change_pct <= PLAT_RANGE_PCT:
            plateau_points.append(i)
        else:
            prod_input.append(arps_input[i])
            plateau_points = []
        if debugMode:
            print '({})      plateau points: {}'.format(i, plateau_points)
            print '({})          prod_input: {}'.format(i, prod_input)
            print ''
    prod_input.append(arps_input[-1])
    return prod_input

if __name__=='__main__':
    test_input  = [1000, 970, 971, 970.5, 972, 969, 930, 910, 911, 911, 912, 909, 885]
    test_output = collapse_flat_prod(test_input)
    print test_output