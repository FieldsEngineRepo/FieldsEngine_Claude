import globaldata as gd
import codecs
import io

TX_FILE_DIR = gd.DATA_DIR + 'well_data\\'
HEX_FILE_DIR = TX_FILE_DIR + 'tx_gas_data_hex\\'
HEX_IN_FILE = 'tx_gas_data_{}.txt'
HEX_OUT_FILE = 'tx_gas_data_{}_converted.txt'

INPUT_FILE = HEX_FILE_DIR + 'tx_gas_data_{}_converted.txt'
HEADER_FILE = gd.DATA_DIR + 'tx_{}_header_data.txt'
OUPUT_FILE = TX_FILE_DIR + 'tx_gas_well_data_1_processed.txt'

FILE_NUMS = [
    '001',
    '002',
    '003',
    '004',
    '005',
    '006',
    '007',
    '008',
    '009',
    '010',
    '011',
    '012',
    '013',
    '014',
    '015',
    '016',
    '017',
    '018',
    '019',
    '020',
    '021',
    '022',
    '023',
    '024',
    '025',
    '026',
    '027',
    '028',
    '029',
    '030',
    '031',
    '032',
    '033',
    '034',
    '035',
    '036',
    '037',
    '038',
    '039',
    '040',
    '041',
    '042',
    '043',
    '044',
    '045',
    '046',
    '047',
    '048',
    '049',
    '050',
    '051',
    '052',
    '053',
    '054',
    '055',
    '056',
    '057',
    '058',
    '059',
    '060',
    '061',
    '062',
    '063',
    '064',
    '065',
    '066',
    '067',
    '068',
    '069',
    '070',
    '071',
    '072',
    '073',
    '074',
    '075',
    '076',
    '077',
    '078',
    '079',
    '080',
    '081',
    '082',
    '083',
    '084',
    '085',
    '086',
    '087',
    '088',
    '089',
    '090',
    '091',
    '092',
    '093',
    '094',
    '095',
    '096',
    '097',
    '098',
    '099',
    '100',
    '101',
    '102',
    '103',
    '104',
    '105',
    '106',
    '107',
    '108',
    '109',
    '110',
    '111',
    '112',
    '113',
    '114',
    '115',
    '116',
    '117',
    '118',
    '119',
    '120',
    '121',
    '122',
    '123',
    '124',
    '125',
    '126',
    '127',
    '128',
    '129',
    '130',
    '131',
    '132',
    '133',
    '134',
    '135',
    '136',
    '137',
    '138',
    '139',
    '140',
    '141',
    '142',
    '143',
    '144',
    '145',
    '146',
    '147',
    '148',
    '149',
    '150',
    '151',
    '152',
    '153',
    '154',
    '155',
    '156',
    '157',
    '158',
    '159',
    '160',
    '161',
    '162'
]

tx_table_data = {
    'tx_gas_altf'  : [
        (2, 'record_key', 0),
        (1, 'transfer_code', 0),
        (9, 'transfer_amount', 0),
        (19, 'data_filler_4', 0)
    ],
    'tx_gas_c1'    : [
        (2, 'record_key', 0),
        (6, 'gc1_key', 0),
        (1, 'gc1_number_of_eff_cycles', 0),
        (4, 'gc1_test_year', 0),
        (2, 'gc1_test_month', 0),
        (2, 'gc1_test_day', 0),
        (1, 'gc1_type_test_flag', 0),
        (32,'gc1_other_remark', 0),
        (9, 'gc1_subst_capability', 0),
        (9, 'data_filler_10', 0),
        (1, 'gc1_engineer_flag', 0),
        (32, 'gc1_certifier_name', 0),
        (9, 'data_filler_12', 0)
    ],
    'tx_gas_frmds' : [
        (2, 'record_key', 0),
        (20, 'forms_description', 0),
        (6, 'data_filler_3', 0)
    ],
    'tx_gas_frmlk' : [
        (2, 'record_key', 0),
        (4, 'form_lack_code', 0),
        (6, 'data_filler_3', 0)
    ],
    'tx_gas_g1'    : [
        (2, 'record_key', 0),
        (8, 'g1_key', 0),
        (4, 'g1_test_year', 0),
        (2, 'g1_test_month', 0),
        (2, 'g1_test_day', 0),
        (9, 'g1_potential', 0),
        (5, 'g1_slope', 3),
        (5, 'g1_siwh', 0),
        (5, 'g1_bhp', 0),
        (5, 'g1_gas_gravity', 3),
        (3, 'g1_cond_gravity', 1),
        (5, 'g1_gor', 0),
        (9, 'g1_test_gas', 0),
        (1, 'g1_admin_add_flag', 0),
        (6, 'data_filler_15', 0)
    ],
    'tx_gas_g10'   : [
        (2, 'record_key', 0),
        (4, 'g10_cycle_key', 0),
        (2, 'g10_day_key', 0),
        (4, 'g10_eff_year', 0),
        (2, 'g10_eff_month', 0),
        (2, 'g10_eff_day', 0),
        (4, 'g10_test_year', 0),
        (2, 'g10_test_month', 0),
        (2, 'g10_test_day', 0),
        (1, 'g10_type_test_flag', 0),
        (9, 'g10_deliverability', 0),
        (7, 'g10_daily_cond', 1),
        (7, 'g10_daily_water', 0),
        (5, 'g10_gas_gravity', 3),
        (3, 'g10_cond_gravity', 1),
        (5, 'g10_ratio', 0),
        (7, 'g10_siwh', 0),
        (5, 'g10_flow_press', 0),
        (9, 'g10_potential', 0),
        (5, 'g10_bhp', 0),
        (1, 'g10_cd_shutin', 0),
        (7, 'g10_whp_shutin_well', 0),
        (5, 'g10_rock_press', 0),
        (9, 'g10_cal_del_pote', 0),
        (4, 'g10_issue_year', 0),
        (2, 'g10_issue_month', 0),
        (2, 'g10_issue_day', 0),
        (4, 'g10_shutin_year', 0),
        (2, 'g10_shutin_month', 0),
        (1, 'g10_annual_cmgl_tst_flag', 0),
        (1, 'g10_survey_counted_flag', 0),
        (1, 'g10_filed_edi_flag', 0),
        (1, 'g10_2yr_survey_counted_flag', 0),
        (4, 'g10_whp_test_year', 0),
        (2, 'g10_whp_test_month', 0),
        (2, 'g10_whp_test_day', 0),
        (2, 'data_filler_37', 0)
    ],
    'tx_gas_prval' : [
        (2, 'record_key', 0),
        (4, 'allow_eff_year_prev', 0),
        (2, 'allow_eff_month_prev', 0),
        (2, 'allow_eff_day_prev', 0),
        (4, 'allow_iss_year_prev', 0),
        (2, 'allow_iss_month_prev', 0),
        (2, 'allow_iss_day_prev', 0),
        (9, 'allow_cycle_amt_prev', 0),
        (9, 'allow_daily_amt_prev', 0),
        (2, 'allow_code_prev', 0),
        (9, 'top_schedule_allow_prev', 0),
        (8, 'word_allow_prev', 0),
        (9, 'spec_allow_daily_prev', 0),
        (1, 'special_allow_code_prev', 0),
        (9, 'liquid_allow_prev', 0),
        (1, 'liquid_allow_code_prev', 0),
        (9, '49b_daily_rate_prev', 0),
        (5, 'data_filler_18', 0),
        (2, 'perm_exc_cycs_prev', 0),
        (7, 'data_filler_20', 0),
        (1, 'data_filler_21', 0),
        (9, 'cal_del_pote_prev', 0),
        (1, 'cal_del_pote_chng_flag', 0),
        (9, 'deliv_prev', 0),
        (1, 'deliv_chng_flag', 0),
        (5, 'bhp_prev', 0),
        (1, 'bhp_chng_flag', 0),
        (7, 'siwh_prev', 0),
        (1, 'siwh_chng_flag', 0),
        (5, 'rock_press_prev', 0),
        (1, 'rock_press_chng_flag', 0),
        (11, 'acres_prev', 4),
        (1, 'acres_chng_flag', 0),
        (7, 'acre_feet_prev', 1),
        (1, 'acre_feet_chng_flag', 0),
        (2, 'well_type_prev', 0),
        (33, 'allow_remarks_prev', 0),
        (1, '14b2_code_prev', 0),
        (4, 'deliv_ltr_eff_yr_prev', 0),
        (2, 'deliv_ltr_eff_mo_prev', 0),
        (2, 'deliv_ltr_eff_da_prev', 0),
        (4, 'test_year_prev', 0),
        (2, 'test_month_prev', 0),
        (2, 'test_day_prev', 0),
        (9, 'lease_percent_reserves_prev', 4),
        (36, 'data_filler_43', 0)
    ],
    'tx_gas_pvg10' : [
        (2, 'record_key', 0),
        (4, 'g10_cycle_key_prev', 0),
        (2, 'g10_day_key_prev', 0),
        (4, 'g10_eff_year_prev', 0),
        (2, 'g10_eff_month_prev', 0),
        (2, 'g10_eff_day_prev', 0),
        (4, 'g10_test_year_prev', 0),
        (2, 'g10_test_month_prev', 0),
        (2, 'g10_test_day_prev', 0),
        (1, 'g10_type_test_flag_prev', 0),
        (9, 'g10_deliverability_prev', 0),
        (7, 'g10_daily_cond_prev', 1),
        (7, 'g10_daily_water_prev', 0),
        (5, 'g10_gas_gravity_prev', 3),
        (3, 'g10_cond_gravity_prev', 1),
        (5, 'g10_ratio_prev', 0),
        (7, 'g10_siwh_prev', 0),
        (5, 'g10_flow_press_prev', 0),
        (9, 'g10_potential_prev', 0),
        (5, 'g10_bhp_prev', 0),
        (1, 'g10_cd_shutin_prev', 0),
        (7, 'g10_whp_shutin_well_prev', 0),
        (5, 'g10_rock_press_prev', 0),
        (9, 'g10_cal_del_pote_prev', 0),
        (4, 'g10_issue_year_prev', 0),
        (2, 'g10_issue_month_prev', 0),
        (2, 'g10_issue_day_prev', 0),
        (4, 'g10_shutin_year_prev', 0),
        (2, 'g10_shutin_month_prev', 0),
        (1, 'g10_ann_cmgl_tst_flag_prev', 0),
        (1, 'g10_survey_cnted_flag_prev', 0),
        (1, 'g10_filing_edi_prev_flag', 0),
        (1, 'g10_2yr_srvy_cnted_flag_prv', 0),
        (4, 'g10_whp_test_year_prev', 0),
        (2, 'g10_whp_test_month_prev', 0),
        (2, 'g10_whp_test_day_prev', 0),
        (2, 'data_filler_37', 0)
    ],
    'tx_gas_remark': [
        (2, 'record_key', 0),
        (3, 'remark_key', 0),
        (4, 'remark_year', 0),
        (2, 'remark_mon', 0),
        (2, 'remark_day', 0),
        (66, 'remark_text', 0),
        (1, 'well_print_on_ledger_flag', 0),
        (13, 'data_filler_8', 0)
    ],
    'tx_gas_root'  : [
        (2, 'record_key', 0),
        (8, 'root_key', 0),
        (1, 'on_off_sched_indicator', 0),
        (1, 'gas_or_oil', 0),
        (2, 'numeric_district', 0),
        (6, 'rrc_id', 0),
        (6, 'well_number', 0),
        (2, 'remove_from_sched_reasn', 0),
        (4, 'remove_from_sched_year', 0),
        (2, 'remove_from_sched_month', 0),
        (2, 'remove_from_sched_day', 0),
        (1, 'prob_prevent_allow_flag', 0),
        (1, 'bay_or_estuary', 0),
        (4, 'last_utilized_year', 0),
        (2, 'last_utilized_month', 0),
        (2, 'last_utilized_day', 0),
        (1, 'except_to_svy_test_flag', 0),
        (8, 'reclassed_well_pointer', 0),
        (2, 'survey_eff_century', 0),
        (2, 'survey_eff_year', 0),
        (2, 'survey_eff_month', 0),
        (25, 'data_filler_22', 0),
        (1, 'subject_to_14b2_flag', 0),
        (1, 'uic_violation_flag', 0),
        (1, 'legal_violation_flag', 0),
        (1, 'ext_for_state_plug_flag', 0),
        (1, 'cert_hb_1975_flag', 0),
        (2, 'cert_effective_cc', 0),
        (2, 'cert_effective_yy', 0),
        (2, 'cert_effective_mm', 0),
        (2, 'certification_ltr_cc', 0),
        (2, 'certification_ltr_yy', 0),
        (2, 'certification_ltr_mm', 0),
        (2, 'certification_ltr_dd', 0),
        (4, 'shut_in_ccyy', 0),
        (2, 'shut_in_mm', 0),
        (1, 'pend_removal_14b2_flag', 0),
        (116, 'data_filler_38', 0)
    ],
    'tx_gas_rptcy' : [
        (2, 'record_key', 0),
        (6, 'report_cycle_date', 0),
        (4, 'allow_effect_year', 0),
        (2, 'allow_effect_mon', 0),
        (2, 'allow_effect_day', 0),
        (4, 'allow_issue_year', 0),
        (2, 'allow_issue_mon', 0),
        (2, 'allow_issue_day', 0),
        (2, 'type_wells', 0),
        (9, 'allowable_cycle_amt', 0),
        (9, 'allowable_daily_amt', 0),
        (2, 'allowable_code', 0),
        (8, 'word_allowable', 0),
        (2, 'assigned_allow_code', 0),
        (9, 'assigned_allow', 0),
        (2, 'adjusted_allow_code', 0),
        (9, 'adjusted_allow_amt', 0),
        (9, 'administrative_allow', 0),
        (9, 'special_allow_daily_amt', 0),
        (1, 'special_allow_code', 0),
        (9, 'liquid_allow_amt', 0),
        (1, 'liquid_allow_code', 0),
        (9, '49b_daily_rate_amt', 0),
        (1, 'past_prod_changed_flag', 0),
        (1, 'high_daily_chngd_flag', 0),
        (1, 'is_a_pf_well_flag', 0),
        (1, 'k2_special_allow_flag', 0),
        (1, 'h15_violation_flag', 0),
        (2, 'perm_exc_cycs', 0),
        (11, 'acres', 4),
        (7, 'acre_feet', 1),
        (9, 'cal_del_pote', 0),
        (5, 'bhp', 0),
        (7, 'siwh', 0),
        (5, 'rock_press', 0),
        (4, 'deliv_letter_effect_yr', 0),
        (2, 'deliv_letter_effect_mo', 0),
        (2, 'deliv_letter_effect_da', 0),
        (9, 'deliverability', 0),
        (9, 'top_schedule_allowable', 0),
        (1, 'exc_to_g10_test_flag', 0),
        (33, 'allowable_remarks', 0),
        (1, 'auto_special_flag', 0),
        (1, 'no_supplement_flag', 0),
        (2, 'highest_daily_avg_cc', 0),
        (2, 'highest_daily_avg_year', 0),
        (2, 'highest_daily_avg_month', 0),
        (9, 'highest_daily_average', 0),
        (4, '12_month_peak_year', 0),
        (2, '12_month_peak_month', 0),
        (9, '12_month_peak', 0),
        (1, 'g10_bhp_except_flag', 0),
        (1, 'g10_sip_except_flag', 0),
        (1, 'dpt_code_except_flag', 0),
        (1, '14b2_code', 0),
        (4, '14b2_year', 0),
        (2, '14b2_month', 0),
        (3, 'bh_temperature', 0),
        (1, 'panhandle_comp_code', 0),
        (8, 'field_deliverability_share', 2),
        (1, 'admin_allow_flag', 0),
        (4, 'test_year', 0),
        (2, 'test_month', 0),
        (2, 'test_day', 0),
        (1, 'tmp_monthly_flag', 0),
        (1, 'recommenced_well_flag', 0),
        (1, 'permanent_gas_well_flag', 0),
        (7, 'data_filler_71', 0)
    ],
    'tx_gas_sb126' : [
        (2, 'record_key', 0),
        (1, 'sb126_cert_flag', 0),
        (2, 'sb126_cert_effect_cc', 0),
        (2, 'sb126_cert_effect_yy', 0),
        (2, 'sb126_cert_effect_mm', 0),
        (2, 'sb126_cert_ltr_cc', 0),
        (2, 'sb126_cert_ltr_yy', 0),
        (2, 'sb126_cert_ltr_mm', 0),
        (2, 'sb126_cert_ltr_dd', 0),
        (2, 'sb126_turnaround_ltr_cc', 0),
        (2, 'sb126_turnaround_ltr_yy', 0),
        (2, 'sb126_turnaround_ltr_mm', 0),
        (2, 'sb126_turnaround_ltr_dd', 0),
        (2, 'data_filler_14', 0)
    ],
    'tx_gas_seal'  : [
        (2, 'record_key', 0),
        (2, 'sealed_effective_century', 0),
        (2, 'sealed_effective_year', 0),
        (2, 'sealed_effective_month', 0),
        (2, 'sealed_reason', 0),
        (4, 'sealed_issue_year', 0),
        (2, 'sealed_issue_month', 0),
        (2, 'sealed_issue_day', 0),
        (2, 'sealed_issued_by', 0),
        (4, 'seal_removed_year', 0),
        (2, 'seal_removed_month', 0),
        (2, 'seal_removed_day', 0),
        (9, 'data_filler_13', 0)
    ],
    'tx_gas_uic'   : [
        (2, 'record_key', 0),
        (9, 'uic_control_number', 0),
        (1, 'h_10_required_flag', 0),
        (2, 'uic_status_century', 0),
        (2, 'uic_status_year', 0),
        (2, 'uic_status_month', 0),
        (2, 'uic_status_day', 0),
        (1, 'prev_h_10_status', 0),
        (1, 'roll_segment_flag', 0),
        (30, 'data_filler_6', 0)
    ],
    'tx_oil_altf'  : [
        (2, 'record_key', 0),
        (1, 'transfer_from_to', 0),
        (4, 'max_can_recv', 0),
        (4, 'total_actual_transfer', 0),
        (1, 'actual_transfer_type', 0),
        (6, 'data_filler_7', 0)
    ],
    'tx_oil_etds'  : [
        (2, 'record_key', 0),
        (8, 'e_tx_designated_wl_key', 0),
        (12, 'data_filler_3', 0)
    ],
    'tx_oil_etex'  : [
        (2, 'record_key', 0),
        (2, 'eswa_bonus_amt', 0),
        (2, 'tswa_bonus_amt', 0),
        (1, 'well_is_clat_flag', 0),
        (1, 'well_is_designated_flag', 0),
        (1, 'well_is_key_well_flag', 0),
        (50, 'well_clat_remarks', 0),
        (1, 'water_oil_ratio_exc_flg', 0),
        (1, 'water_well_shut_down', 0),
        (4, 'clat_removal_year', 0),
        (2, 'clat_removal_month', 0),
        (2, 'clat_removal_day', 0),
        (3, 'clat_plugged_out_amt', 0),
        (1, 'clat_plugged_out_code', 0),
        (4, 'data_filler_15', 0)
    ],
    'tx_oil_frmds' : [
        (2, 'record_key', 0),
        (20, 'forms_description', 0),
        (206, 'data_filler_3', 0)
    ],
    'tx_oil_frmlk' : [
        (2, 'record_key', 0),
        (4, 'form_lacking', 0),
        (222, 'data_filler_3', 0)
    ],
    'tx_oil_phbal' : [
        (2, 'record_key', 0),
        (1, 'well_lost_compl_2_8_flag', 0),
        (4, 'lost_compl_2_8_year', 0),
        (2, 'lost_compl_2_8_month', 0),
        (2, 'lost_compl_2_8_day', 0),
        (41, 'data_filler_6', 0)
    ],
    'tx_oil_phprod': [
        (2, 'record_key', 0),
        (9, 'casinghead_gas_amount', 0),
        (9, 'casinghead_gas_percent', 5),
        (50, 'data_filler_4', 0)
    ],
    'tx_oil_prval' : [
        (2, 'record_key', 0),
        (4, 'prev_effective_year', 0),
        (2, 'prev_effective_month', 0),
        (2, 'prev_effective_day', 0),
        (4, 'prev_issue_year', 0),
        (2, 'prev_issue_month', 0),
        (2, 'prev_issue_day', 0),
        (7, 'prev_work_potential', 1),
        (1, 'data_filler_9', 0),
        (5, 'prev_allow_amount', 0),
        (7, 'prev_gas_limit', 0),
        (5, 'prev_gas_oil_ratio', 0),
        (30, 'prev_remarks', 0),
        (2, 'allowable_codes_prv', 0),
        (1, 'allow_limited_cd_prv', 0),
        (2, 'type_wells_prv', 0),
        (7, 'well_monthly_allow_prv', 0),
        (9, 'csh_monthly_limit_prv', 0),
        (1, '14b2_code_prv', 0),
        (1, 'etex_pro_marg_prv', 0),
        (2, 'etex_oil_trns_prv', 0),
        (2, 'etex_gas_trns_prv', 0),
        (1, 'allocation_prv_flag', 0),
        (1, 'data_filler_23', 0)
    ],
    'tx_oil_pvtyp' : [
        (2, 'record_key', 0),
        (2, 'prev_well_type', 0),
        (224, 'data_filler_3', 0)
    ],
    'tx_oil_pvw10' : [
        (2, 'record_key', 0),
        (4, 'w10_cycle_key_prev', 0),
        (2, 'w10_day_key_prev', 0),
        (4, 'w10_eff_year_prev', 0),
        (2, 'w10_eff_month_prev', 0),
        (2, 'w10_eff_day_prev', 0),
        (1, 'w10_type_status_flag_prev', 0),
        (1, 'w10_producing_method_prev', 0),
        (20, 'w10_prd_meth_other_rpt_prev', 0),
        (4, 'w10_test_year_prev', 0),
        (2, 'w10_test_month_prev', 0),
        (2, 'w10_test_day_prev', 0),
        (7, 'w10_daily_oil_prev', 1),
        (5, 'w10_daily_water_prev', 0),
        (7, 'w10_daily_gas_prev', 0),
        (5, 'w10_gas_oil_ratio_prev', 0),
        (7, 'w10_siwh_pressure_prev', 0),
        (4, 'w10_siwh_year_prev', 0),
        (2, 'w10_siwh_month_prev', 0),
        (6, 'data_filler_20', 0),
        (2, 'w10_type_well_flag_prev', 0),
        (6, 'data_filler_22', 0),
        (4, 'w10_issue_year_prev', 0),
        (2, 'w10_issue_month_prev', 0),
        (2, 'w10_issue_day_prev', 0),
        (1, 'w10_filing_edi_prev_flag', 0),
        (9, 'data_filler_25', 0)
    ],
    'tx_oil_remark': [
        (2, 'record_key', 0),
        (3, 'remark_key', 0),
        (4, 'remark_year', 0),
        (2, 'remark_mon', 0),
        (2, 'remark_day', 0),
        (66, 'remark_text', 0),
        (1, 'well_print_on_ledger_flag', 0),
        (13, 'data_filler_8', 0)
    ],
    'tx_oil_root'  : [
        (2, 'record_key', 0),
        (8, 'root_key', 0),
        (1, 'on_off_sched_indicator', 0),
        (1, 'oil_or_gas', 0),
        (2, 'numeric_district', 0),
        (5, 'lease_number', 0),
        (1, 'unit_number', 0),
        (6, 'well_number', 0),
        (2, 'remove_from_sched_reasn', 0),
        (4, 'remove_from_sched_year', 0),
        (2, 'remove_from_sched_month', 0),
        (2, 'remove_from_sched_day', 0),
        (8, 'reclassed_well_pointer', 0),
        (1, 'prob_prevent_allow_flag', 0),
        (1, 'data_filler_15', 0),
        (5, 'reservoir', 0),
        (1, 'bay_or_estuary', 0),
        (4, 'data_filler_18', 0),
        (1, 'w10_exc_to_svy_flag', 0),
        (3, 'onshore_co_code', 0),
        (9, 'original_potential', 3),
        (3, 'data_filler_22', 0),
        (1, 'unit_no', 0),
        (5, 'unit_value', 3),
        (2, 'survey_eff_century', 0),
        (2, 'survey_eff_year', 0),
        (2, 'survey_eff_month', 0),
        (8, 'new_wb_connect_date', 0),
        (1, 'subject_to_14b2_flag', 0),
        (1, 'uic_violation_flag', 0),
        (1, 'legal_violation_flag', 0),
        (1, 'ext_for_state_plug_flag', 0),
        (1, 'cert_hb_1975_flag', 0),
        (2, 'cert_effective_cc', 0),
        (2, 'cert_effective_yy', 0),
        (2, 'cert_effective_mm', 0),
        (2, 'certification_ltr_cc', 0),
        (2, 'certification_ltr_yy', 0),
        (2, 'certification_ltr_mm', 0),
        (2, 'certification_ltr_dd', 0),
        (4, 'shut_in_ccyy', 0),
        (2, 'shut_in_mm', 0),
        (1, 'pend_removal_14b2_flag', 0),
        (116, 'data_filler_44', 0)
    ],
    'tx_oil_rptcy' : [
        (2, 'record_key', 0),
        (6, 'report_cycle_date', 0),
        (7, 'acres', 2),
        (5, 'acre_feet', 0),
        (5, 'net_acre_feet', 0),
        (5, 'bhp', 0),
        (7, 'working_potential', 1),
        (1, 'tolerance_acres_flag', 0),
        (4, 'effective_year', 0),
        (2, 'effective_month', 0),
        (2, 'effective_day', 0),
        (4, 'issue_year', 0),
        (2, 'issue_month', 0),
        (2, 'issue_day', 0),
        (5, 'allowable_amount', 0),
        (7, 'limit', 0),
        (5, 'oil_ratio', 0),
        (30, 'report_cycle_remark', 0),
        (7, 'original_oil_in_place', 0),
        (2, 'allowable_codes_rpt', 0),
        (1, 'allow_limited_cd_rpt', 0),
        (2, 'type_wells_rpt', 0),
        (3, 'sand_thickness', 0),
        (1, 'co_reg_depth_code', 0),
        (1, 'net_gor_code', 0),
        (5, 'net_gor', 0),
        (1, 'special_allow_code', 0),
        (5, 'special_allow_amt', 0),
        (1, '14b2_code', 0),
        (4, '14b2_year', 0),
        (2, '14b2_month', 0),
        (5, 'water_production', 0),
        (5, 'frozen_potential', 0),
        (1, 'producing_method_rpt', 0),
        (20, 'other_prod_method_rpt', 0),
        (7, 'well_monthly_allowable', 0),
        (5, 'lowest_perforation', 0),
        (1, 'data_filler_38', 0),
        (1, 'w10_exc_to_test_flag', 0),
        (4, 'test_year', 0),
        (2, 'test_month', 0),
        (2, 'test_day', 0),
        (1, 'retest_flag', 0),
        (5, '12_hour_potential', 0),
        (1, 'bonus_code', 0),
        (3, 'bonus_amount', 0),
        (1, 'eb_flag', 0),
        (1, 'allow_pote_gor_chg_flag', 0),
        (9, 'csh_monthly_limit', 0),
        (1, 'eb_change_month_flag', 0),
        (7, 'well_top', 0),
        (1, 'panhandle_comp_code', 0),
        (1, 'panhandle_sub_code', 0),
        (1, 'h15_violation_flag', 0),
        (1, 'allocation_flag', 0),
        (6, 'data_filler_56', 0)
    ],
    'tx_oil_sb126' : [
        (2, 'record_key', 0),
        (1, 'sb126_cert_flag', 0),
        (2, 'sb126_cert_effect_cc', 0),
        (2, 'sb126_cert_effect_yy', 0),
        (2, 'sb126_cert_effect_mm', 0),
        (2, 'sb126_cert_ltr_cc', 0),
        (2, 'sb126_cert_ltr_yy', 0),
        (2, 'sb126_cert_ltr_mm', 0),
        (2, 'sb126_cert_ltr_dd', 0),
        (2, 'sb126_turnaround_ltr_cc', 0),
        (2, 'sb126_turnaround_ltr_yy', 0),
        (2, 'sb126_turnaround_ltr_mm', 0),
        (2, 'sb126_turnaround_ltr_dd', 0),
        (2, 'data_filler_14', 0)
    ],
    'tx_oil_seal'  : [
        (2, 'record_key', 0),
        (2, 'sealed_effective_century', 0),
        (2, 'sealed_effective_year', 0),
        (2, 'sealed_effective_month', 0),
        (2, 'sealed_reason', 0),
        (4, 'sealed_issue_year', 0),
        (2, 'sealed_issue_month', 0),
        (2, 'sealed_issue_day', 0),
        (2, 'sealed_issued_by', 0),
        (4, 'seal_removed_year', 0),
        (2, 'seal_removed_month', 0),
        (2, 'seal_removed_day', 0),
        (9, 'data_filler_13', 0)
    ],
    'tx_oil_tfwl'  : [
        (2, 'record_key', 0),
        (8, 'well_transferred', 0),
        (1, 'transfer_type', 0),
        (4, 'oil_transfer', 0),
        (4, 'gas_transfer', 0),
        (13, 'data_filler_6', 0)
    ],
    'tx_oil_uic'   : [
        (2, 'record_key', 0),
        (9, 'uic_control_number', 0),
        (1, 'h_10_required_flag', 0),
        (2, 'uic_status_century', 0),
        (2, 'uic_status_year', 0),
        (2, 'uic_status_month', 0),
        (2, 'uic_status_day', 0),
        (1, 'prev_h_10_status', 0),
        (1, 'roll_segment_flag', 0),
        (30, 'data_filler_6', 0)
    ],
    'tx_oil_w10'   : [
        (2, 'record_key', 0),
        (4, 'w10_cycle_key', 0),
        (2, 'w10_day_key', 0),
        (4, 'w10_eff_year', 0),
        (2, 'w10_eff_month', 0),
        (2, 'w10_eff_day', 0),
        (1, 'w10_type_status_flag', 0),
        (1, 'w10_producing_method', 0),
        (20, 'w10_prod_meth_other_rpt', 0),
        (4, 'w10_test_year', 0),
        (2, 'w10_test_month', 0),
        (2, 'w10_test_day', 0),
        (7, 'w10_daily_oil', 1),
        (5, 'w10_daily_water', 0),
        (7, 'w10_daily_gas', 0),
        (5, 'w10_gas_oil_ratio', 0),
        (7, 'w10_siwh_pressure', 0),
        (4, 'w10_siwh_year', 0),
        (2, 'w10_siwh_month', 0),
        (6, 'data_filler_20', 0),
        (2, 'w10_type_well_flag', 0),
        (6, 'data_filler_22', 0),
        (4, 'w10_issue_year', 0),
        (2, 'w10_issue_month', 0),
        (2, 'w10_issue_day', 0),
        (1, 'w10_survey_counted_flag', 0),
        (1, 'w10_filed_edi_flag', 0),
        (1, 'w10_allocation_flag', 0),
        (1, 'w10_2yr_survey_counted_flag', 0),
        (6, 'data_filler_28', 0)
    ]
}

tx_wb_table_data = {
	'tx_wb_root': [
		(2,'record_key',0),
		(3,'api_cnty',0),
		(5,'api_unique',0),
		(2,'nxt_avail_suffix',0),
		(2,'nxt_avail_hole_chge_nbr',0),
		(2,'field_district',0),
		(3,'res_cnty_code',0),
		(1,'orig_compl_cc',0),
		(2,'orig_compl_cent',0),
		(2,'orig_compl_yy',0),
		(2,'orig_compl_mm',0),
		(2,'orig_compl_dd',0),
		(5,'total_depth',0),
		(5,'valid_fluid_level',0),
		(2,'cert_revoked_cc',0),
		(2,'cert_revoked_yy',0),
		(2,'cert_revoked_mm',0),
		(2,'cert_revoked_dd',0),
		(2,'certification_denial_cc',0),
		(2,'certification_denial_yy',0),
		(2,'certification_denial_mm',0),
		(2,'certification_denial_dd',0),
		(1,'denial_reason_flag',0),
		(1,'error_api_assign_code',0),
		(8,'refer_correct_api_nbr',0),
		(8,'dummy_api_number',0),
		(8,'date_dummy_replaced',0),
		(6,'newest_drl_pmt_nbr',0),
		(1,'cancel_expire_code',0),
		(1,'filler_1',0),
		(1,'except_13_a',0),
		(1,'fresh_water_flag',0),
		(1,'plug_flag',0),
		(8,'previous_api_nbr',0),
		(1,'completion_data_ind',0),
		(1,'hist_date_source_flag',0),
		(1,'filler_2',0),
		(2,'ex14b2_count',0),
		(1,'designation_hb_1975_flag',0),
		(2,'designation_effec_cc',0),
		(2,'designation_effec_yy',0),
		(2,'designation_effec_mm',0),
		(2,'designation_revised_cc',0),
		(2,'designation_revised_yy',0),
		(2,'designation_revised_mm',0),
		(2,'designation_letter_cc',0),
		(2,'designation_letter_yy',0),
		(2,'designation_letter_mm',0),
		(2,'designation_letter_dd',0),
		(2,'certification_effec_cc',0),
		(2,'certification_effec_yy',0),
		(2,'certification_effec_mm',0),
		(1,'water_land_code',0),
		(6,'total_bonded_depth',0),
		(7,'override_est_plug_cost',0),
		(4,'shut_in_year',0),
		(2,'shut_in_month',0),
		(6,'override_bonded_depth',0),
		(1,'subj_to_14b2_flag',0),
		(1,'pend_removal_14b2_flag',0),
		(1,'orphan_well_hold_flag',0),
		(1,'w3x_well_flag',0),
		(6,'filler_3',0),
		(80,'data_filler_end',0)
	],
	'tx_wb_compl': [
		(2,'record_key',0),
		(1,'oil_gas_code',0),
		(13,'oil_gas_key',0),
		(2,'gas_dist',0),
		(6,'gas_well_no',0),
		(1,'multi_well_rec_nbr',0),
		(2,'api_suffix',0),
		(18,'filler_4',0),
		(1,'active_inactive_code',0),
		(40,'filler_5',0),
		(1,'dwn_hole_commingle_code',0),
		(34,'filler_6',0),
		(1,'created_from_pi_flag',0),
		(7,'rule_37_nbr',0),
		(5,'filler_7',0),
		(5,'filler_8',0),
		(10,'filler_9',0),
		(4,'filler_10',0),
		(2,'filler_11',0),
		(1,'p_15',0),
		(1,'p_12',0),
		(8,'plug_date_pointer',0),
		(6,'filler_12',0),
		(76,'data_filler_end',0)
	],
	'tx_wb_date': [
		(2,'record_key',0),
		(8,'file_key',0),
		(8,'file_date',0),
		(8,'filler_13',0),
		(1,'except_rule_11',0),
		(1,'cement_affidavit',0),
		(1,'g_5',0),
		(1,'w_12',0),
		(1,'dir_survey',0),
		(8,'w2_g1_date',0),
		(2,'compl_century',0),
		(2,'compl_year',0),
		(2,'compl_month',0),
		(2,'compl_day',0),
		(8,'drl_compl_date',0),
		(5,'plugb_depth1',0),
		(5,'plugb_depth2',0),
		(6,'water_injection_nbr',0),
		(5,'salt_wtr_nbr',0),
		(8,'filler_14',0),
		(1,'remarks_ind',0),
		(4,'elevation',0),
		(2,'elevation_code',0),
		(8,'log_file_rba',0),
		(10,'docket_nbr',0),
		(1,'psa_well_flag',0),
		(1,'allocation_well_flag',0),
		(6,'filler_15',0),
		(130,'data_filler_end',0)
	],
	'tx_wb_rmks': [
		(2,'record_key',0),
		(3,'rmk_lne_cnt',0),
		(1,'rmk_type_code',0),
		(70,'remarks',0),
		(171,'data_filler_end',0)
	],
	'tx_wb_tube': [
		(2,'record_key',0),
		(3,'segment_counter',0),
		(2,'tubing_inches',0),
		(2,'fr_numerator',0),
		(2,'fr_denominator',0),
		(5,'depth_set',0),
		(5,'packer_set',0),
		(10,'filler_16',0),
		(16,'filler_17',0),
		(200,'data_filler_end',0)
	],
	'tx_wb_case': [
		(2,'record_key',0),
		(3,'casing_count',0),
		(2,'cas_inch',0),
		(2,'cas_frac_num',0),
		(2,'cas_frac_denom',0),
		(8,'cas_wt_table',0),
		(5,'casing_depth_set',0),
		(5,'mlti_stg_tool_dpth',0),
		(5,'amount_of_cement',0),
		(1,'cement_measurement',0),
		(2,'hole_inch',0),
		(2,'hole_frac_num',0),
		(2,'hole_frac_denom',0),
		(1,'filler_18',0),
		(7,'top_of_cement_casing',0),
		(5,'amount_casing_left',0),
		(50,'filler_19',0),
		(143,'data_filler_end',0)
	],
	'tx_wb_perf': [
		(2,'record_key',0),
		(3,'perf_count',0),
		(5,'from_perf',0),
		(5,'to_perf',0),
		(2,'open_hole_code',0),
		(10,'filler_20',0),
		(220,'data_filler_end',0)
	],
	'tx_wb_line': [
		(2,'record_key',0),
		(3,'line_count',0),
		(2,'lin_inch',0),
		(2,'lin_frac_num',0),
		(2,'lin_frac_denom',0),
		(5,'sacks_of_cement',0),
		(5,'top_of_liner',0),
		(5,'bottom_of_liner',0),
		(20,'filler_21',0),
		(201,'data_filler_end',0)
	],
	'tx_wb_form': [
		(2,'record_key',0),
		(3,'formation_cntr',0),
		(32,'formation_name',0),
		(5,'formation_depth',0),
		(5,'filler_22',0),
		(200,'data_filler_end',0)
	],
	'tx_wb_sqeze': [
		(2,'record_key',0),
		(3,'squeeze_cntr',0),
		(5,'squeeze_upper_depth',0),
		(5,'squeeze_lower_depth',0),
		(50,'squeeze_kind_amount',0),
		(7,'filler_23',0),
		(175,'data_filler_end',0)
	],
	'tx_wb_fresh': [
		(2,'record_key',0),
		(3,'fresh_water_cntr',0),
		(8,'twdb_date',0),
		(1,'surface_casing_deter_code',0),
		(4,'uqwp_from',0),
		(4,'uqwp_to',0),
		(10,'filler_24',0),
		(215,'data_filler_end',0)
	],
	'tx_wb_oldloc': [
		(2,'record_key',0),
		(32,'lease_name',0),
		(52,'sec_blk_survey_loc',0),
		(4,'well_loc_miles',0),
		(6,'well_loc_direction',0),
		(13,'well_loc_nearest_town',0),
		(28,'filler_25',0),
		(28,'dist_from_survey_lines',0),
		(28,'dist_direct_near_well',0),
		(28,'filler_26',0),
		(26,'data_filler_end',0)
	],
	'tx_wb_newloc': [
		(2,'record_key',0),
		(3,'loc_county',0),
		(6,'abstract',0),
		(55,'survey',0),
		(10,'block_number',0),
		(8,'section',0),
		(4,'alt_section',0),
		(6,'alt_abstract',0),
		(6,'feet_from_sur_sect_1',0),
		(13,'direc_from_sur_sect_1',0),
		(6,'feet_from_sur_sect_2',0),
		(13,'direc_from_sur_sect_2',0),
		(10,'wgs84_latitude',7),
		(10,'wgs84_longitude',7),
		(5,'filler_27',0),
		(2,'plane_zone',0),
		(10,'plane_coordinate_east',2),
		(10,'plane_coordinate_north',2),
		(1,'verification_flag',0),
		(1,'filler_28',0),
		(66,'data_filler_end',0)
	],
	'tx_wb_plug': [
		(2,'record_key',0),
		(8,'date_w3_filed',0),
		(8,'date_well_bore_plugged',0),
		(5,'plug_total_depth',0),
		(32,'plug_cement_comp',0),
		(1,'plug_mud_filled',0),
		(12,'plug_mud_applied',0),
		(3,'plug_mud_weight',0),
		(4,'filler_29',0),
		(8,'plug_dril_perm_date',0),
		(6,'plug_dril_perm_no',0),
		(8,'plug_dril_comp_date',0),
		(1,'plug_log_attached',0),
		(32,'plug_log_released_to',0),
		(1,'plug_type_log',0),
		(5,'plug_fresh_water_depth',0),
		(40,'plug_uwqp',0),
		(1,'plug_material_left',0),
		(1,'plug_oil_gas_code',0),
		(13,'plug_oil_gas_key',0),
		(2,'plug_gas_dist',0),
		(6,'plug_gas_well_no',0),
		(1,'plug_type_well',0),
		(1,'plug_multi_compl_flag',0),
		(1,'plug_cem_aff',0),
		(1,'plug_13a',0),
		(8,'plug_log_released_date',0),
		(8,'plug_log_file_rba',0),
		(7,'state_funded_plug_number',0),
		(21,'filler_30',0)
	],
	'tx_wb_plrmks': [
		(2,'record_key',0),
		(3,'plug_rmk_lne_cnt',0),
		(1,'plug_rmk_type_code',0),
		(70,'plug_remarks',0),
		(171,'data_filler_end',0)
	],
	'tx_wb_plrec': [
		(2,'record_key',0),
		(3,'plug_number',0),
		(5,'nbr_of_cement_sacks',0),
		(5,'meas_top_of_plug',0),
		(5,'bottom_tube_pipe_depth',0),
		(5,'plug_calc_top',0),
		(6,'plug_type_cement',0),
		(19,'filler_31',0),
		(197,'data_filler_end',0)
	],
	'tx_wb_plcase': [
		(2,'record_key',0),
		(6,'plg_cas_counter',0),
		(2,'plug_cas_inch',0),
		(2,'plug_cas_frac_num',0),
		(2,'plug_cas_frac_denom',0),
		(3,'plug_wgt_whole',0),
		(1,'plug_wgt_tenths',0),
		(5,'plug_amt_put',0),
		(5,'plug_amt_left',0),
		(2,'plug_hole_inch',0),
		(2,'plug_hole_frac_num',0),
		(2,'plug_hole_frac_denom',0),
		(20,'filler_32',0),
		(193,'data_filler_end',0)
	],
	'tx_wb_plperf': [
		(2,'record_key',0),
		(3,'plug_perf_counter',0),
		(5,'plug_from_perf',0),
		(5,'plug_to_perf',0),
		(1,'plug_open_hole_indicator',0),
		(19,'filler_33',0),
		(212,'data_filler_end',0)
	],
	'tx_wb_plname': [
		(2,'record_key',0),
		(8,'plug_field_no',0),
		(32,'plug_field_name',0),
		(6,'plug_oper_no',0),
		(32,'plug_oper_name',0),
		(32,'plug_lease_name',0),
		(135,'data_filler_end',0)
	],
	'tx_wb_drill': [
		(2,'record_key',0),
		(6,'permit_number',0),
		(14,'filler_34',0),
		(225,'data_filler_end',0),
	],
	'tx_wb_wellid': [
		(2,'record_key',0),
		(1,'oil_gas_code',0),
		(13,'oil_gas_key',0),
		(11,'filler_35',0),
		(220,'data_filler_end',0)
	],
	'tx_wb_14b2': [
		(2,'record_key',0),
		(1,'oil_gas_code',0),
		(13,'oil_gas_key',0),
		(6,'application_number',0),
		(2,'gas_district',0),
		(1,'ext_status_flag',0),
		(1,'ext_cancelled_reason',0),
		(2,'ext_approved_cent',0),
		(2,'ext_approved_year',0),
		(2,'ext_approved_month',0),
		(2,'ext_approved_day',0),
		(2,'ext_exp_cent',0),
		(2,'ext_exp_year',0),
		(2,'ext_exp_month',0),
		(2,'ext_exp_day',0),
		(2,'ext_denied_cent',0),
		(2,'ext_denied_year',0),
		(2,'ext_denied_month',0),
		(2,'ext_denied_day',0),
		(2,'ext_hist_cent',0),
		(2,'ext_hist_year',0),
		(2,'ext_hist_month',0),
		(2,'ext_hist_day',0),
		(1,'mech_integ_viol_flag',0),
		(1,'plug_order_sf_hold_flag',0),
		(1,'pollution_viol_flag',0),
		(1,'field_ops_hold_flag',0),
		(1,'h15_problem_flag',0),
		(1,'h15_not_filed_flag',0),
		(1,'oper_delq_flag',0),
		(1,'district_hold_sfp_flag',0),
		(1,'dist_sf_clean_up_flag',0),
		(1,'dist_state_plug_flag',0),
		(1,'good_faith_viol_flag',0),
		(1,'well_other_viol_flag',0),
		(1,'w3c_surf_eqp_viol_flag',0),
		(1,'w3x_viol_flag',0),
		(7,'filler_36',0),
		(1,'hb2259_w3x_pub_ent',0),
		(1,'hb2259_w3x_10pct',0),
		(1,'hb2259_w3x_bonding',0),
		(1,'hb2259_w3x_h13_eor',0),
		(1,'hb2259_w3x_aop',0),
		(1,'hb2259_w3x_mit',0),
		(1,'hb2259_w3x_escrow',0),
		(8,'w3x_filing_key',0),
		(8,'w3x_aop_received_date',0),
		(8,'w3x_aop_fee_rcvd_date',0),
		(8,'w3x_h15_fee_rcvd_date',0),
		(5,'w3x_escrow_fund_whole',0),
		(2,'w3x_escrow_fund_decimal',0),
		(1,'60_day_letter_sent_flag',0),
		(1,'w1x_36_needs_bond_flag',0),
		(1,'w1x_36_type_coverage',0),
		(9,'w1x_36_amt_filed',0),
		(5,'w1x_36_surety',0),
		(2,'w1x_36_exp_cent',0),
		(2,'w1x_36_exp_year',0),
		(2,'w1x_36_exp_mon',0),
		(2,'w1x_36_exp_day',0),
		(20,'w1x_36_bond_number',0),
		(32,'filler_37',0),
		(45,'data_filler_end',0)
	],
	'tx_wb_h15': [
		(2,'record_key',0),
		(8,'h15_date_key',0),
		(1,'h15_status',0),
		(6,'h15_operator',0),
		(4,'next_test_ccyy',0),
		(2,'next_test_mm',0),
		(2,'h15_district',0),
		(8,'h15_field',0),
		(1,'h15_hist_wellbore_flag',0),
		(2,'h15_hist_well_cc',0),
		(2,'h15_hist_well_yy',0),
		(2,'h15_hist_well_mm',0),
		(2,'h15_hist_well_dd',0),
		(1,'h15_w1x_well',0),
		(1,'h15_oil_gas_code',0),
		(5,'h15_lease_nbr',0),
		(6,'h15_well_nbr',0),
		(6,'h15_gasid_nbr',0),
		(2,'h15_test_cc',0),
		(2,'h15_test_yy',0),
		(2,'h15_test_mm',0),
		(2,'h15_test_dd',0),
		(6,'h15_base_usable_water',0),
		(1,'h15_type_test_flag',0),
		(6,'h15_top_of_fluid',0),
		(1,'h15_fluid_test_flag',0),
		(1,'h15_mech_integ_test_flag',0),
		(1,'h15_mech_test_reason_flag',0),
		(2,'h15_alternate_test_period',0),
		(20,'h15_other_mit_test_type',0),
		(2,'h15_status_cc',0),
		(2,'h15_status_yy',0),
		(2,'h15_status_mm',0),
		(2,'h15_status_dd',0),
		(1,'h15_no_date_well_flag',0),
		(1,'h15_record_from_edi_flag',0),
		(2,'h15_keyed_cc',0),
		(2,'h15_keyed_yy',0),
		(2,'h15_keyed_mm',0),
		(2,'h15_keyed_dd',0),
		(2,'h15_changed_cc',0),
		(2,'h15_changed_yy',0),
		(2,'h15_changed_mm',0),
		(2,'h15_changed_dd',0),
		(1,'h15_previous_status',0),
		(1,'h15_uic_test_flag',0),
		(1,'h15_2yrs_approved_flag',0),
		(1,'h15_mail_hold_flag',0),
		(1,'h15_10yr_inactive_flag',0),
		(1,'h15_w3x_well_flag',0),
		(13,'filler_38',0),
		(95,'data_filler_end',0)
	],
	'tx_wb_h15rmk': [
		(2,'record_key',0),
		(3,'h15_remark_key',0),
		(70,'h15_remark_text',0),
		(7,'filler_39',0),
		(165,'data_filler_end',0)
	],
	'tx_wb_sb126': [
		(2,'record_key',0),
		(1,'sb126_designation_flag',0),
		(2,'sb126_desig_effec_cc',0),
		(2,'sb126_desig_effec_yy',0),
		(2,'sb126_desig_effec_mm',0),
		(2,'sb126_desig_revised_cc',0),
		(2,'sb126_desig_revised_yy',0),
		(2,'sb126_desig_revised_mm',0),
		(2,'sb126_desig_letter_cc',0),
		(2,'sb126_desig_letter_yy',0),
		(2,'sb126_desig_letter_mm',0),
		(2,'sb126_desig_letter_dd',0),
		(2,'sb126_cert_effec_cc',0),
		(2,'sb126_cert_effec_yy',0),
		(2,'sb126_cert_effec_mm',0),
		(2,'sb126_cert_revoked_cc',0),
		(2,'sb126_cert_revoked_yy',0),
		(2,'sb126_cert_revoked_mm',0),
		(2,'sb126_cert_revoked_dd',0),
		(2,'sb126_cert_denial_cc',0),
		(2,'sb126_cert_denial_yy',0),
		(2,'sb126_cert_denial_mm',0),
		(2,'sb126_cert_denial_dd',0),
		(1,'sb126_denial_reason_flag',0),
		(16,'filler_40',0),
		(185,'data_filler_end',0)
	],
	'tx_wb_dastat': [
		(2,'record_key',0),
		(7,'stat_num',0),
		(2,'uniq_num',0),
		(1,'deleted_flag',0),
		(10,'filler_41',0),
		(225,'data_filler_end',0)
	],
	'tx_wb_w3c': [
		(2,'record_key',0),
		(1,'w3c_1yr_flag',0),
		(8,'w3c_1yr_filed_date',0),
		(6,'w3c_1yr_filing_oper',0),
		(1,'w3c_5yr_flag',0),
		(8,'w3c_5yr_filed_date',0),
		(6,'w3c_5yr_filing_oper',0),
		(1,'w3c_10yr_flag',0),
		(8,'w3c_10yr_filed_date',0),
		(6,'w3c_10yr_filing_oper',0),
		(8,'w3c_14b2_removal_date',0),
		(1,'w3c_extension_flag',0),
		(4,'w3c_extension_year',0),
		(2,'w3c_extension_month',0),
		(2,'w3c_extension_day',0),
		(1,'w3c_5yr_flag_previous',0),
		(1,'w3c_10yr_flag_previous',0),
		(36,'filler_42',0),
		(145,'data_filler_end',0)
	],
	'tx_wb_14b2rm': [
		(2,'record_key',0),
		(3,'14b2_rmk_lne_cnt',0),
		(8,'14b2_rmk_date',0),
		(8,'14b2_rmk_userid',0),
		(66,'14b2_remarks',0),
		(15,'filler_43',0),
		(145,'data_filler_end',0)
	]
}

tx_oil = {
    '01': (2, 8, 1, 1, 2, 5, 1, 6, 2, 4, 2, 2, 8, 1, 1, 5, 1, 4, 1, 3, 5, 3, 1, 3, 2, 2, 2, 8, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 4, 2, 1, 116),
    '02': [
        (2, False, 'rrc_tape_rec_id'),
        (6, False, 'report_cycle_date'),
        (7, True, 'acres'),
        (5, True, 'acre_feet'),
        (5, True, 'net_acre_feet'),
        (5, True, 'bhp'),
        (7, True, 'working_potential'),
        (1, False, 'tolerance_acres'),
        (4, False, 'effective_year'),
        (2, False, 'effective_month'),
        (2, False, 'effective_day'),
        (4, False, 'issue_year'),
        (2, False, 'issue_month'),
        (2, False, 'issue_day'),
        (5, True, 'allowable_amount'),
        (7, True, 'gas_limit'),
        (5, True, 'gas_oil_ratio'),
        (30, False, 'report_cycle_remark'),
        (7, True, 'original_oil_in_place'),
        (2, False, 'allowable_code'),
        (1, False, 'allow_limit_cd'),
        (2, False, 'type_wells'),
        (3, False, 'sand_thickness'),
        (1, False, 'co_reg_depth_code'),
        (1, False, 'net_gor_code'),
        (5, True, 'net_gor'),
        (1, False, 'special_allow_code'),
        (5, True, 'special_allow_amount'),
        (1, False, '14B2_code'),
        (4, False, '14B2_year'),
        (2, False, '14B2_month'),
        (5, True, 'water_production'),
        (5, True, 'frozen_potential'),
        (1, False, 'producing_method'),
        (20, False, 'other_prod_method'),
        (7, True, 'well_monthly_allowable'),
        (5, True, 'lowest_perforation'),
        (1, False, 'filler'),
        (1, False, 'w10_exc_to_test_flag'),
        (4, False, 'test_year'),
        (2, False, 'test_month'),
        (2, False, 'test_day'),
        (1, False, 'retest_flag'),
        (5, True, '12_hour_potential'),
        (1, False, 'bonus_code'),
        (3, False, 'bonus_amount'),
        (1, False, 'eb_flag'),
        (1, False, 'allow_pote_gor_chg_flag'),
        (9, True, 'cash_monthly_limit'),
        (1, False, 'eb_change_month_flag'),
        (7, True, 'top_allowable_amount'),
        (1, False, 'panhandle_comp_code'),
        (1, False, 'panhandle_sub_code'),
        (1, False, 'h15_violation_flag'),
        (1, False, 'oil_allocation_flag'),
        (6, False, 'filler_2')
    ],
    '03': (2, 226),
    '04': (2, 226),
    '05': (2, 226),
    '06': (2, 226),
    '07': (2, 226),
    '08': (2, 226),
    '09': (2, 226),
    '10': (2, 226),
    '11': (2, 226),
    '12': (2, 226),
    '13': (2, 226),
    '14': (2, 226),
    '15': (2, 226),
    '16': (2, 226),
    '26': (2, 226),
    '28': (2, 226)
}

comp_3_conv = {
    '00': 'f0f0',
    '01': 'f0f1',
    '02': 'f0f2',
    '03': 'f0f3',
    '04': 'f0f4',
    '05': 'f0f5',
    '06': 'f0f6',
    '07': 'f0f7',
    '08': 'f0f8',
    '09': 'f0f9',
    '10': 'f1f0',
    '11': 'f1f1',
    '12': 'f1f2',
    '13': 'f1f3',
    '14': 'f1f4',
    '15': 'f1f5',
    '16': 'f1f6',
    '17': 'f1f7',
    '18': 'f1f8',
    '19': 'f1f9',
    '20': 'f2f0',
    '21': 'f2f1',
    '22': 'f2f2',
    '23': 'f2f3',
    '24': 'f2f4',
    '25': 'f2f5',
    '26': 'f2f6',
    '27': 'f2f7',
    '28': 'f2f8',
    '29': 'f2f9',
    '30': 'f3f0',
    '31': 'f3f1',
    '32': 'f3f2',
    '33': 'f3f3',
    '34': 'f3f4',
    '35': 'f3f5',
    '36': 'f3f6',
    '37': 'f3f7',
    '38': 'f3f8',
    '39': 'f3f9',
    '40': 'f4f0',
    '41': 'f4f1',
    '0a': 'f0',
    '0b': 'f0',
    '0c': 'f0',
    '0d': 'f0',
    '0e': 'f0',
    '0f': 'f0',
    'ff': '40',
    'a0': 'f0',
    'b0': 'f0',
    'c0': 'f0',
    'd0': 'f0',
    'e0': 'f0',
    '42': 'f4f2',
    '43': 'f4f3',
    '44': 'f4f4',
    '45': 'f4f5',
    '46': 'f4f6',
    '47': 'f4f7',
    '48': 'f4f8',
    '49': 'f4f9',
    '50': 'f5f0',
    '51': 'f5f1',
    '52': 'f5f2',
    '53': 'f5f3',
    '54': 'f5f4',
    '55': 'f5f5',
    '56': 'f5f6',
    '57': 'f5f7',
    '58': 'f5f8',
    '59': 'f5f9',
    '60': 'f6f0',
    '61': 'f6f1',
    '62': 'f6f2',
    '63': 'f6f3',
    '64': 'f6f4',
    '65': 'f6f5',
    '66': 'f6f6',
    '67': 'f6f7',
    '68': 'f6f8',
    '69': 'f6f9',
    '70': 'f7f0',
    '71': 'f7f1',
    '72': 'f7f2',
    '73': 'f7f3',
    '74': 'f7f4',
    '75': 'f7f5',
    '76': 'f7f6',
    '77': 'f7f7',
    '78': 'f7f8',
    '79': 'f7f9',
    '80': 'f8f0',
    '81': 'f8f1',
    '82': 'f8f2',
    '83': 'f8f3',
    '84': 'f8f4',
    '85': 'f8f5',
    '86': 'f8f6',
    '87': 'f8f7',
    '88': 'f8f8',
    '89': 'f8f9',
    '90': 'f9f0',
    '91': 'f9f1',
    '92': 'f9f2',
    '93': 'f9f3',
    '94': 'f9f4',
    '95': 'f9f5',
    '96': 'f9f6',
    '97': 'f9f7',
    '98': 'f9f8',
    '99': 'f9f9',
    '1a': 'f1',
    '1b': 'f1',
    '1c': 'f1',
    '1d': 'f1',
    '1e': 'f1',
    '1f': 'f1',
    '2a': 'f2',
    '2b': 'f2',
    '2c': 'f2',
    '2d': 'f2',
    '2e': 'f2',
    '2f': 'f2',
    '3a': 'f3',
    '3b': 'f3',
    '3c': 'f3',
    '3d': 'f3',
    '3e': 'f3',
    '3f': 'f3',
    '4a': 'f4',
    '4b': 'f4',
    '4c': 'f4',
    '4d': 'f4',
    '4e': 'f4',
    '4f': 'f4',
    '5a': 'f5',
    '5b': 'f5',
    '5c': 'f5',
    '5d': 'f5',
    '5e': 'f5',
    '5f': 'f5',
    '6a': 'f6',
    '6b': 'f6',
    '6c': 'f6',
    '6d': 'f6',
    '6e': 'f6',
    '6f': 'f6',
    '7a': 'f7',
    '7b': 'f7',
    '7c': 'f7',
    '7d': 'f7',
    '7e': 'f7',
    '7f': 'f7',
    '8a': 'f8',
    '8b': 'f8',
    '8c': 'f8',
    '8d': 'f8',
    '8e': 'f8',
    '8f': 'f8',
    '9a': 'f9',
    '9b': 'f9',
    '9c': 'f9',
    '9d': 'f9',
    '9e': 'f9',
    '9f': 'f9',
    'a1': 'a1',
    'a2': 'a2',
    'a3': 'a3',
    'a4': 'a4',
    'a5': 'a5',
    'a6': 'a6',
    'a7': 'a7',
    'a8': 'a8',
    'a9': 'a9',
    'aa': 'aa',
    'ab': 'ab',
    'ac': 'ac',
    'ad': 'ad',
    'ae': 'ae',
    'af': 'af',
    'b1': 'b1',
    'b2': 'b2',
    'b3': 'b3',
    'b4': 'b4',
    'b5': 'b5',
    'b6': 'b6',
    'b7': 'b7',
    'b8': 'b8',
    'b9': 'b9',
    'ba': 'ba',
    'bb': 'bb',
    'bc': 'bc',
    'bd': 'bd',
    'be': 'be',
    'bf': 'bf',
    'c1': 'c1',
    'c2': 'c2',
    'c3': 'c3',
    'c4': 'c4',
    'c5': 'c5',
    'c6': 'c6',
    'c7': 'c7',
    'c8': 'c8',
    'c9': 'c9',
    'ca': 'ca',
    'cb': 'cb',
    'cc': 'cc',
    'cd': 'cd',
    'ce': 'ce',
    'cf': 'cf',
    'd1': 'd1',
    'd2': 'd2',
    'd3': 'd3',
    'd4': 'd4',
    'd5': 'd5',
    'd6': 'd6',
    'd7': 'd7',
    'd8': 'd8',
    'd9': 'd9',
    'da': 'da',
    'db': 'db',
    'dc': 'dc',
    'dd': 'dd',
    'de': 'de',
    'df': 'df',
    'e1': 'e1',
    'e2': 'e2',
    'e3': 'e3',
    'e4': 'e4',
    'e5': 'e5',
    'e6': 'e6',
    'e7': 'e7',
    'e8': 'e8',
    'e9': 'e9',
    'ea': 'ea',
    'eb': 'eb',
    'ec': 'ec',
    'ed': 'ed',
    'ee': 'ee',
    'ef': 'ef',
    'f1': 'f1',
    'f2': 'f2',
    'f3': 'f3',
    'f4': 'f4',
    'f5': 'f5',
    'f6': 'f6',
    'f7': 'f7',
    'f8': 'f8',
    'f9': 'f9',
    'fa': 'fa',
    'fb': 'fb',
    'fc': 'fc',
    'fd': 'fd',
    'fe': 'fe',
    'f0': 'f0'
}

comp_3_conv2 = {
    '00': 'f0f0',
    '01': 'f0f1',
    '02': 'f0f2',
    '03': 'f0f3',
    '04': 'f0f4',
    '05': 'f0f5',
    '06': 'f0f6',
    '07': 'f0f7',
    '08': 'f0f8',
    '09': 'f0f9',
    '10': 'f1f0',
    '11': 'f1f1',
    '12': 'f1f2',
    '13': 'f1f3',
    '14': 'f1f4',
    '15': 'f1f5',
    '16': 'f1f6',
    '17': 'f1f7',
    '18': 'f1f8',
    '19': 'f1f9',
    '20': 'f2f0',
    '21': 'f2f1',
    '22': 'f2f2',
    '23': 'f2f3',
    '24': 'f2f4',
    '25': 'f2f5',
    '26': 'f2f6',
    '27': 'f2f7',
    '28': 'f2f8',
    '29': 'f2f9',
    '30': 'f3f0',
    '31': 'f3f1',
    '32': 'f3f2',
    '33': 'f3f3',
    '34': 'f3f4',
    '35': 'f3f5',
    '36': 'f3f6',
    '37': 'f3f7',
    '38': 'f3f8',
    '39': 'f3f9',
    '40': 'f4f0',
    '41': 'f4f1',
    '0a': 'f040',
    '0b': 'f040',
    '0c': 'f040',
    '0d': 'f040',
    '0e': 'f040',
    '0f': 'f040',
    'ff': '4040',
    'a0': 'f040',
    'b0': 'f040',
    'c0': 'f040',
    'd0': 'f040',
    'e0': 'f040',
    '42': 'f4f2',
    '43': 'f4f3',
    '44': 'f4f4',
    '45': 'f4f5',
    '46': 'f4f6',
    '47': 'f4f7',
    '48': 'f4f8',
    '49': 'f4f9',
    '50': 'f5f0',
    '51': 'f5f1',
    '52': 'f5f2',
    '53': 'f5f3',
    '54': 'f5f4',
    '55': 'f5f5',
    '56': 'f5f6',
    '57': 'f5f7',
    '58': 'f5f8',
    '59': 'f5f9',
    '60': 'f6f0',
    '61': 'f6f1',
    '62': 'f6f2',
    '63': 'f6f3',
    '64': 'f6f4',
    '65': 'f6f5',
    '66': 'f6f6',
    '67': 'f6f7',
    '68': 'f6f8',
    '69': 'f6f9',
    '70': 'f7f0',
    '71': 'f7f1',
    '72': 'f7f2',
    '73': 'f7f3',
    '74': 'f7f4',
    '75': 'f7f5',
    '76': 'f7f6',
    '77': 'f7f7',
    '78': 'f7f8',
    '79': 'f7f9',
    '80': 'f8f0',
    '81': 'f8f1',
    '82': 'f8f2',
    '83': 'f8f3',
    '84': 'f8f4',
    '85': 'f8f5',
    '86': 'f8f6',
    '87': 'f8f7',
    '88': 'f8f8',
    '89': 'f8f9',
    '90': 'f9f0',
    '91': 'f9f1',
    '92': 'f9f2',
    '93': 'f9f3',
    '94': 'f9f4',
    '95': 'f9f5',
    '96': 'f9f6',
    '97': 'f9f7',
    '98': 'f9f8',
    '99': 'f9f9',
    '1a': 'f140',
    '1b': 'f140',
    '1c': 'f140',
    '1d': 'f140',
    '1e': 'f140',
    '1f': 'f140',
    '2a': 'f240',
    '2b': 'f240',
    '2c': 'f240',
    '2d': 'f240',
    '2e': 'f240',
    '2f': 'f240',
    '3a': 'f340',
    '3b': 'f340',
    '3c': 'f340',
    '3d': 'f340',
    '3e': 'f340',
    '3f': 'f340',
    '4a': 'f440',
    '4b': 'f440',
    '4c': 'f440',
    '4d': 'f440',
    '4e': 'f440',
    '4f': 'f440',
    '5a': 'f540',
    '5b': 'f540',
    '5c': 'f540',
    '5d': 'f540',
    '5e': 'f540',
    '5f': 'f540',
    '6a': 'f640',
    '6b': 'f640',
    '6c': 'f640',
    '6d': 'f640',
    '6e': 'f640',
    '6f': 'f640',
    '7a': 'f740',
    '7b': 'f740',
    '7c': 'f740',
    '7d': 'f740',
    '7e': 'f740',
    '7f': 'f740',
    '8a': 'f840',
    '8b': 'f840',
    '8c': 'f840',
    '8d': 'f840',
    '8e': 'f840',
    '8f': 'f840',
    '9a': 'f940',
    '9b': 'f940',
    '9c': 'f940',
    '9d': 'f940',
    '9e': 'f940',
    '9f': 'f940',
    'a1': 'a140',
    'a2': 'a240',
    'a3': 'a340',
    'a4': 'a440',
    'a5': 'a540',
    'a6': 'a640',
    'a7': 'a740',
    'a8': 'a840',
    'a9': 'a940',
    'aa': 'aa40',
    'ab': 'ab40',
    'ac': 'ac40',
    'ad': 'ad40',
    'ae': 'ae40',
    'af': 'af40',
    'b1': 'b140',
    'b2': 'b240',
    'b3': 'b340',
    'b4': 'b440',
    'b5': 'b540',
    'b6': 'b640',
    'b7': 'b740',
    'b8': 'b840',
    'b9': 'b940',
    'ba': 'ba40',
    'bb': 'bb40',
    'bc': 'bc40',
    'bd': 'bd40',
    'be': 'be40',
    'bf': 'bf40',
    'c1': 'c140',
    'c2': 'c240',
    'c3': 'c340',
    'c4': 'c440',
    'c5': 'c540',
    'c6': 'c640',
    'c7': 'c740',
    'c8': 'c840',
    'c9': 'c940',
    'ca': 'ca40',
    'cb': 'cb40',
    'cc': 'cc40',
    'cd': 'cd40',
    'ce': 'ce40',
    'cf': 'cf40',
    'd1': 'd140',
    'd2': 'd240',
    'd3': 'd340',
    'd4': 'd440',
    'd5': 'd540',
    'd6': 'd640',
    'd7': 'd740',
    'd8': 'd840',
    'd9': 'd940',
    'da': 'da40',
    'db': 'db40',
    'dc': 'dc40',
    'dd': 'dd40',
    'de': 'de40',
    'df': 'df40',
    'e1': 'e140',
    'e2': 'e240',
    'e3': 'e340',
    'e4': 'e440',
    'e5': 'e540',
    'e6': 'e640',
    'e7': 'e740',
    'e8': 'e840',
    'e9': 'e940',
    'ea': 'ea40',
    'eb': 'eb40',
    'ec': 'ec40',
    'ed': 'ed40',
    'ee': 'ee40',
    'ef': 'ef40',
    'f1': 'f140',
    'f2': 'f240',
    'f3': 'f340',
    'f4': 'f440',
    'f5': 'f540',
    'f6': 'f640',
    'f7': 'f740',
    'f8': 'f840',
    'f9': 'f940',
    'fa': 'fa40',
    'fb': 'fb40',
    'fc': 'fc40',
    'fd': 'fd40',
    'fe': 'fe40',
    'f0': 'f040'
}

comp_3_conv_ = {
    '00': '3030',
    '01': '3031',
    '02': '3032',
    '03': '3033',
    '04': '3034',
    '05': '3035',
    '06': '3036',
    '07': '3037',
    '08': '3038',
    '09': '3039',
    '10': '3130',
    '11': '3131',
    '12': '3132',
    '13': '3133',
    '14': '3134',
    '15': '3135',
    '16': '3136',
    '17': '3137',
    '18': '3138',
    '19': '3139',
    '20': '3230',
    '21': '3231',
    '22': '3232',
    '23': '3233',
    '24': '3234',
    '25': '3235',
    '26': '3236',
    '27': '3237',
    '28': '3238',
    '29': '3239',
    '30': '3330',
    '31': '3331',
    '32': '3332',
    '33': '3333',
    '34': '3334',
    '35': '3335',
    '36': '3336',
    '37': '3337',
    '38': '3338',
    '39': '3339',
    '40': '3430',
    '41': '3431',
    '0a': '30',
    '0b': '30',
    '0c': '30',
    '0d': '30',
    '0e': '30',
    '0f': '30',
    'ff': '40',
    'a0': '30',
    'b0': '30',
    'c0': '30',
    'd0': '30',
    'e0': '30',
    '42': '3432',
    '43': '3433',
    '44': '3434',
    '45': '3435',
    '46': '3436',
    '47': '3437',
    '48': '3438',
    '49': '3439',
    '50': '3530',
    '51': '3531',
    '52': '3532',
    '53': '3533',
    '54': '3534',
    '55': '3535',
    '56': '3536',
    '57': '3537',
    '58': '3538',
    '59': '3539',
    '60': '3630',
    '61': '3631',
    '62': '3632',
    '63': '3633',
    '64': '3634',
    '65': '3635',
    '66': '3636',
    '67': '3637',
    '68': '3638',
    '69': '3639',
    '70': '3730',
    '71': '3731',
    '72': '3732',
    '73': '3733',
    '74': '3734',
    '75': '3735',
    '76': '3736',
    '77': '3737',
    '78': '3738',
    '79': '3739',
    '80': '3830',
    '81': '3831',
    '82': '3832',
    '83': '3833',
    '84': '3834',
    '85': '3835',
    '86': '3836',
    '87': '3837',
    '88': '3838',
    '89': '3839',
    '90': '3930',
    '91': '3931',
    '92': '3932',
    '93': '3933',
    '94': '3934',
    '95': '3935',
    '96': '3936',
    '97': '3937',
    '98': '3938',
    '99': '3939',
    '1a': '31',
    '1b': '31',
    '1c': '31',
    '1d': '31',
    '1e': '31',
    '1f': '31',
    '2a': '32',
    '2b': '32',
    '2c': '32',
    '2d': '32',
    '2e': '32',
    '2f': '32',
    '3a': '33',
    '3b': '33',
    '3c': '33',
    '3d': '33',
    '3e': '33',
    '3f': '33',
    '4a': '34',
    '4b': '34',
    '4c': '34',
    '4d': '34',
    '4e': '34',
    '4f': '34',
    '5a': '35',
    '5b': '35',
    '5c': '35',
    '5d': '35',
    '5e': '35',
    '5f': '35',
    '6a': '36',
    '6b': '36',
    '6c': '36',
    '6d': '36',
    '6e': '36',
    '6f': '36',
    '7a': '37',
    '7b': '37',
    '7c': '37',
    '7d': '37',
    '7e': '37',
    '7f': '37',
    '8a': '38',
    '8b': '38',
    '8c': '38',
    '8d': '38',
    '8e': '38',
    '8f': '38',
    '9a': '39',
    '9b': '39',
    '9c': '39',
    '9d': '39',
    '9e': '39',
    '9f': '39',
    'a1': 'a1',
    'a2': 'a2',
    'a3': 'a3',
    'a4': 'a4',
    'a5': 'a5',
    'a6': 'a6',
    'a7': 'a7',
    'a8': 'a8',
    'a9': 'a9',
    'aa': 'aa',
    'ab': 'ab',
    'ac': 'ac',
    'ad': 'ad',
    'ae': 'ae',
    'af': 'af',
    'b1': 'b1',
    'b2': 'b2',
    'b3': 'b3',
    'b4': 'b4',
    'b5': 'b5',
    'b6': 'b6',
    'b7': 'b7',
    'b8': 'b8',
    'b9': 'b9',
    'ba': 'ba',
    'bb': 'bb',
    'bc': 'bc',
    'bd': 'bd',
    'be': 'be',
    'bf': 'bf',
    'c1': 'c1',
    'c2': 'c2',
    'c3': 'c3',
    'c4': 'c4',
    'c5': 'c5',
    'c6': 'c6',
    'c7': 'c7',
    'c8': 'c8',
    'c9': 'c9',
    'ca': 'ca',
    'cb': 'cb',
    'cc': 'cc',
    'cd': 'cd',
    'ce': 'ce',
    'cf': 'cf',
    'd1': 'd1',
    'd2': 'd2',
    'd3': 'd3',
    'd4': 'd4',
    'd5': 'd5',
    'd6': 'd6',
    'd7': 'd7',
    'd8': 'd8',
    'd9': 'd9',
    'da': 'da',
    'db': 'db',
    'dc': 'dc',
    'dd': 'dd',
    'de': 'de',
    'df': 'df',
    'e1': 'e1',
    'e2': 'e2',
    'e3': 'e3',
    'e4': 'e4',
    'e5': 'e5',
    'e6': 'e6',
    'e7': 'e7',
    'e8': 'e8',
    'e9': 'e9',
    'ea': 'ea',
    'eb': 'eb',
    'ec': 'ec',
    'ed': 'ed',
    'ee': 'ee',
    'ef': 'ef',
    'f1': 'f1',
    'f2': 'f2',
    'f3': 'f3',
    'f4': 'f4',
    'f5': 'f5',
    'f6': 'f6',
    'f7': 'f7',
    'f8': 'f8',
    'f9': 'f9',
    'fa': 'fa',
    'fb': 'fb',
    'fc': 'fc',
    'fd': 'fd',
    'fe': 'fe',
    'f0': 'f0'
}

comp_3_nums = {
    'cc': 3036,
    'cd': 3037,
    'ce': 3038,
    'cf': 3039,
    'da': 3430,
    'db': 3431,
    'e2': 3432,
    'e4': 3433,
    'e0': 3434,
    'e1': 3435,
    'e3': 3436,
    'e5': 3437,
    'e7': 3438,
    'f1': 3439,
    '26': 3530,
    'e9': 3531,
    'ea': 3532,
    'eb': 3533,
    'e8': 3534,
    'ed': 3535,
    'ee': 3536,
    'ef': 3537,
    'ec': 3538,
    'df': 3539,
    '2d': 3630,
    '2f': 3631,
    'c2': 3632,
    'c4': 3633,
    'c0': 3634,
    'c1': 3635,
    'c3': 3636,
    'c5': 3637,
    'c7': 3638,
    'd1': 3639,
    'f8': 3730,
    'c9': 3731,
    'ca': 3732,
    'cb': 3733,
    'c8': 3734,
    'cd': 3735,
    'ce': 3736,
    'cf': 3737,
    'cc': 3738,
    '60': 3739,
    'd8': 3830,
    '61': 3831,
    '62': 3832,
    '63': 3833,
    '64': 3834,
    '65': 3835,
    '66': 3836,
    '67': 3837,
    '68': 3838,
    '69': 3839,
    'b0': 3930,
    '6a': 3931,
    '6b': 3932,
    '6c': 3933,
    '6d': 3934,
    '6e': 3935,
    '6f': 3936,
    '70': 3937,
    '71': 3938,
    '72': 3939,
    '41': 3130,
    '42': 3131,
    '43': 3132,
    '44': 3133,
    '45': 3134,
    '46': 3135,
    '47': 3136,
    '48': 3137,
    '49': 3138,
    '4a': 3139,
    '4b': 3230,
    '4c': 3231,
    '4d': 3232,
    '4e': 3233,
    '4f': 3234,
    '50': 3235,
    '51': 3236,
    '52': 3237,
    '53': 3238,
    '54': 3239,
    '55': 3330,
    '56': 3331,
    '57': 3332,
    '58': 3333,
    '59': 3334,
    '5a': 3335

}

tx_oil_well_info_cols = [
    'well_root_no',
    'district_no',
    'lease_no',
    'well_no',
    'rrc_tape_rec_id',
    'report_cycle_date',
    'acres',
    'acre_feet',
    'net_acre_feet',
    'bhp',
    'working_potential',
    'tolerance_acres',
    'effective_year',
    'effective_month',
    'effective_day',
    'issue_year',
    'issue_month',
    'issue_day',
    'allowable_amount',
    'gas_limit',
    'gas_oil_ratio',
    'report_cycle_remark',
    'original_oil_in_place',
    'allowable_code',
    'allow_limit_cd',
    'type_wells',
    'sand_thickness',
    'co_reg_depth_code',
    'net_gor_code',
    'net_gor',
    'special_allow_code',
    'special_allow_amount',
    '14B2_code',
    '14B2_year',
    '14B2_month',
    'water_production',
    'frozen_potential',
    'producing_method',
    'other_prod_method',
    'well_monthly_allowable',
    'lowest_perforation',
    'filler',
    'w10_exc_to_test_flag',
    'test_year',
    'test_month',
    'test_day',
    'retest_flag',
    '12_hour_potential',
    'bonus_code',
    'bonus_amount',
    'eb_flag',
    'allow_pote_gor_chg_flag',
    'cash_monthly_limit',
    'eb_change_month_flag',
    'top_allowable_amount',
    'panhandle_comp_code',
    'panhandle_sub_code',
    'h15_violation_flag',
    'oil_allocation_flag'
]

wb_hex_data = {
    '09': [42],
    '10': [10, 15]
}

comp_3_data = {
    'oil': {
        'f0f1': [20, 61, 62, 63, 64, 65, 70, 71, 72],
        'f0f2': [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 83, 84, 85, 86, 94, 97, 98, 99, 101, 102, 103, 111, 112, 113, 114, 115, 116, 138, 139, 140, 141, 142, 143, 144, 145, 156, 157, 158, 162, 165, 166, 167, 168, 169, 171, 172, 173, 174],
        'f0f3': [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 69, 70, 71, 72, 73, 74, 75, 76, 77],
        'f1f0': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'f1f3': [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],
        'f1f4': [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64]
    },
    'gas': {
        'f2f4': [4, 5, 6, 7, 8],
        'f2f5': [
            19, 20, 21, 22, 23,
            24, 25, 26, 27, 28,
            31, 32, 33, 34, 35,
            44, 45, 46, 47, 48,
            50, 51, 52, 53, 54,
            56, 57, 58, 59, 60,
            61, 62, 63, 64, 65,
            68, 69, 70, 71,
            73, 74, 75, 76, 77,
            79, 80, 81, 82, 83,
            85, 86, 87,
            89, 90, 91, 92,
            94, 95, 96,
            98, 99, 100, 101, 102, 103,
            105, 106, 107, 108,
            162, 163, 164, 165, 166
        ],
        'f2f0': [
            51, 52, 53, 54, 55,
            56, 57, 58, 59, 60
        ],
        '3230': [
            52, 53, 54, 55, 56,
            57, 58, 59, 60, 61
        ],
        'f2f1': [
            27, 28, 29, 30, 31,
            32, 33, 34, 35, 36,
            49, 50, 51, 52, 53,
            56, 57, 58, 59, 60,
            61, 62, 63, 64, 65,
            66, 67, 68, 69, 70,
            72, 73, 74, 75, 76,
            78, 79, 80, 81, 82,
            90, 91, 92, 93, 94, 95,
            96, 97, 98, 99,
            100, 101, 102, 103, 104,
            105, 106, 107,
            108, 109, 110, 111,
            112, 113, 114,
            123, 124, 125, 126, 127,
            128, 129, 130, 131, 132,
            175, 176, 177, 178, 179,
            186, 187, 188, 189, 190#,
            #204, 205, 206, 207, 208,
            #209,
            #222, 223, 224, 225, 226
        ],
        'f1f9': [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74],
        'f1f8': [
            26, 27, 28, 29, 30,
            31, 32, 33, 34,
            35, 36, 37, 38,
            39, 40, 41,
            42, 43,
            44, 45, 46,
            47, 48, 49, 50,
            51, 52, 53,
            54, 55, 56, 57, 58,
            59, 60, 61,
            63, 64, 65, 66,
            67, 68, 69,
            70, 71, 72, 73, 74
        ],
        'f1f7': [
            19, 20, 21, 22, 23,
            24, 25, 26,
            27, 28, 29,
            30, 31, 32,
            33, 34, 35,
            36, 37,
            38, 39, 40,
            41, 42, 43, 44, 45
        ]
    }
}

rec_comp_3_data = {
    'oil': {
        '03': [
            (19, 5),
            (24, 3),
            (27, 4),
            (31, 3),
            (69, 4),
            (73, 5),
        ],
        '14': [
            (47, 4),
            (51, 3),
            (54, 4),
            (58, 3),
            (61, 4)
        ],
        '02': [
            (9, 4),
            (13, 3),
            (16, 3),
            (19, 3),
            (22, 4),
            (43, 3),
            (46, 4),
            (50, 3),
            (83, 4),
            (97, 3),
            (101, 3),
            (111, 3),
            (114, 3),
            (138, 4),
            (142, 4),
            (156, 3),
            (165, 5),
            (171, 4)
        ],
        '13': [
            (47, 4),
            (51, 3),
            (54, 4),
            (58, 3),
            (61, 4)
        ],
        '10': [
            (3, 5),
            (8, 5)
        ],
        '01': [
            (61, 5)
        ]
    },
    'gas': {
        '17': [
            (19, 5),
            (24, 3),
            (27, 3),
            (30, 3),
            (33, 3),
            (36, 2),
            (38, 3),
            (41, 5)
        ],
        '18': [
            (26, 5),
            (31, 4),
            (35, 4),
            (39, 3),
            (42, 2),
            (44, 3),
            (47, 4),
            (51, 3),
            (54, 5),
            (59, 3),
            (63, 4),
            (67, 3),
            (70, 5)
        ],
        '19': [
            (26, 5),
            (31, 4),
            (35, 4),
            (39, 3),
            (42, 2),
            (44, 3),
            (47, 4),
            (51, 3),
            (54, 5),
            (59, 3),
            (63, 4),
            (67, 3),
            (70, 5)
        ],
        '20': [(51, 1)],
        '21': [
            (27, 5),
            (32, 5),
            (49, 5),
            (56, 5),
            (61, 5),
            (66, 5),
            (72, 5),
            (78, 5),
            (90, 6),
            (96, 4),
            (100, 5),
            (105, 3),
            (108, 4),
            (112, 3),
            (123, 5),
            (128, 5),
            (175, 5),
            (186, 3)
        ],
        '24': [(4, 5)],
        '25': [
            (19, 5),
            (24, 5),
            (31, 5),
            (44, 5),
            (50, 5),
            (56, 10),
            (68, 4),
            (73, 5),
            (79, 5),
            (85, 3),
            (89, 4),
            (94, 3),
            (98, 6),
            (105, 4),
            (162, 5)
        ]
    }
}

tx_record_tables = {
    'oil': {
        '01': 'tx_oil_root',
        '02': 'tx_oil_rptcy',
        '03': 'tx_oil_prval',
        '04': 'tx_oil_frmlk',
        '05': 'tx_oil_frmds',
        '06': 'tx_oil_etex',
        '07': 'tx_oil_etds',
        '08': 'tx_oil_altf',
        '09': 'tx_oil_tfwl',
        '10': 'tx_oil_phprod',
        '11': 'tx_oil_pvtyp',
        '12': 'tx_oil_phbal',
        '13': 'tx_oil_w10',
        '14': 'tx_oil_pvw10',
        '15': 'tx_oil_remark',
        '16': 'tx_oil_seal',
        '26': 'tx_oil_uic',
        '28': 'tx_oil_sb126'
    },
    'gas': {
        '01': 'tx_gas_root',
        '15': 'tx_gas_remark',
        '16': 'tx_gas_seal',
        '17': 'tx_gas_g1',
        '18': 'tx_gas_g10',
        '19': 'tx_gas_pvg10',
        '20': 'tx_gas_c1',
        '21': 'tx_gas_rptcy',
        '22': 'tx_gas_frmlk',
        '23': 'tx_gas_frmds',
        '24': 'tx_gas_altf',
        '25': 'tx_gas_prval',
        '27': 'tx_gas_uic',
        '28': 'tx_gas_sb126'
    }
}

tx_wb_record_tables = {
    '01': 'tx_wb_root',
    '02': 'tx_wb_compl',
    '03': 'tx_wb_date',
    '04': 'tx_wb_rmks',
    '05': 'tx_wb_tube',
    '06': 'tx_wb_case',
    '07': 'tx_wb_perf',
    '08': 'tx_wb_line',
    '09': 'tx_wb_form',
    '10': 'tx_wb_sqeze',
    '11': 'tx_wb_fresh',
    '12': 'tx_wb_oldloc',
    '13': 'tx_wb_newloc',
    '14': 'tx_wb_plug',
    '15': 'tx_wb_plrmks',
    '16': 'tx_wb_plrec',
    '17': 'tx_wb_plcase',
    '18': 'tx_wb_plperf',
    '19': 'tx_wb_plname',
    '20': 'tx_wb_drill',
    '21': 'tx_wb_wellid',
    '22': 'tx_wb_14b2',
    '23': 'tx_wb_h15',
    '24': 'tx_wb_h15rmk',
    '25': 'tx_wb_sb126',
    '26': 'tx_wb_dastat',
    '27': 'tx_wb_w3c',
    '28': 'tx_wb_14b2rm'
}

tx_oil_gas_key_data = {
    '02': [
        '03',
        '04',
        '05',
        '06',
        '07',
        '08',
        '09',
        '10',
        '11'
    ],
    '14': [
        '15',
        '16',
        '17',
        '18',
        '19'
    ],
    '22': [
        '28'
    ],
    '21': [
    ]
}

tx_oil_gas_key_tables = [
    '02',
    '03'
    '07',
    '09',
    '14',
    '18',
    '21',
    '22'
]


def update_oil_gas_key_id(curr, index_table, wb_table, debug=False):
    sql_update = "UPDATE {} AS a, {} AS b SET a.oil_gas_key=b.oil_gas_key, a.oil_gas_code=b.oil_gas_code, a.lease_no=b.lease_no, a.well_no=b.well_no, a.district_no=b.district_no WHERE a.file_source_line={} AND b.file_source_line={}"
    target_src_lines = gd.get_data('file_source_line', '{}'.format(wb_table), database='us_wells', cursor=curr, datatype='int')
    src_line_count   = len(target_src_lines)
    src_line_num     = 1
    if debug: print 'source_lines: {}'.format(target_src_lines)
    for source_line in target_src_lines:
        print '({}) - {}/{}: {}'.format(wb_table, src_line_num, src_line_count, source_line)
        max_source_line = gd.get_data('file_source_line AS max_source_line', '{}'.format(index_table), database='us_wells', cursor=curr, single_value=True, datatype='int', sql_where='file_source_line < {} ORDER BY file_source_line DESC LIMIT 1'.format(int(source_line)))
        if debug: print sql_update.format(wb_table, index_table, source_line, max_source_line)
        curr.execute(sql_update.format(wb_table, index_table, source_line, max_source_line))
        gd.commit(curr)
        src_line_num += 1


def update_wb_oil_gas_key_data(debug=False):
    conn = gd.get_connection(database='us_wells')
    curr = conn.cursor()
    for index_rec_key in tx_oil_gas_key_data.keys():
        index_table = tx_wb_record_tables[index_rec_key]
        for wb_table in [tx_wb_record_tables[rec_key] for rec_key in tx_oil_gas_key_data[index_rec_key] if rec_key in tx_oil_gas_key_tables]:
            update_oil_gas_key_id(curr, index_table, wb_table, debug=debug)
    curr.close()
    conn.close()


def get_comp_3_cols(data_comm='oil'):
    comp_3_data_ = {}
    for rec_key in rec_comp_3_data[data_comm].keys():
        rec_comp_3_cols = []
        for start_indx, data_len in rec_comp_3_data[data_comm][rec_key]:
            rec_comp_3_cols += range(start_indx, start_indx + data_len)
        hex_rec_key = 'f{}f{}'.format(rec_key[0], rec_key[1])
        comp_3_data_[hex_rec_key] = rec_comp_3_cols
    return comp_3_data_


def convert_file(input_dir, input_file):
    with io.open(input_dir + input_file, 'r', encoding="cp037") as ebc_file:
        for fileline in ebc_file:
            print 0, fileline
            repr(codecs.encode(fileline, 'latin-1'))


def convert_ebc_file(input_dir, output_dir, input_file, output_file, data_comm='oil', debug=False):
    output_text = ''
    input_filename = input_file[:-4]
    data_comm = input_file[3:6].lower()
    column_hex = {col: [] for col in range(1, 229)}
    with open(input_dir + input_file, 'r') as ebc_file:
        fileline_num = 1
        output_doc_num = 1
        fileline = ' ' * 228
        if '162' in input_file:
            fileline_max = 50525
        else:
            fileline_max = 51200
        while fileline_num < fileline_max:
            if fileline_num % 500 == 0:
                print '{} -- {}% processed ({}/{}) '.format(input_file, round(100 * (float(fileline_num) / float(fileline_max)), 1), fileline_num, fileline_max)
            fileline = ebc_file.read(228)
            linedata = repr(codecs.encode(fileline, "hex"))[1:]
            output_line = ''
            for col in range(1, 229):
                start_indx = (col - 1) * 2
                end_indx = (col) * 2
                hex_val = linedata[start_indx:end_indx]
                if col > 2:
                    record_key = output_line[:4]
                    if record_key in comp_3_data[data_comm].keys() and col in comp_3_data[data_comm][record_key]:
                        hex_val = comp_3_conv[hex_val]
                    elif record_key == 'f2f1':
                        if 203 < col < 210:
                            hex_val = comp_3_conv2[hex_val]
                        elif col > 221:
                            hex_val = 'f0'
                output_line += hex_val
                if debug:
                    column_hex[col].append(hex_val)
            try:
                output_line = codecs.decode(output_line, 'hex')
                output_line = output_line.decode('cp500').encode('latin-1')
                output_text += (output_line + '\n')
            except:
                with open(output_dir + '{}_'.format(fileline_num) + output_file, 'w') as outfile:
                    outfile.write(output_text)
            fileline_num += 1
    if debug:
        for col in range(1, 229):
            print 'col {}: {}'.format(col, column_hex[col])
    with open(output_dir + output_file, 'w') as outfile:
        outfile.write(output_text)


def parse_datalines(output_data, input_file):
    conn = gd.get_connection(server='mysql', database='well_data')
    curr = conn.cursor()
    col_str = ', '.join(tx_oil_well_info_cols)
    var_str = ', '.join(['%s'] * len(tx_oil_well_info_cols))
    print len(tx_oil_well_info_cols), var_str.count('%s'), len(tx_oil['02'])
    sql_insert = 'INSERT INTO tx_oil_well_input ({}) VALUES ({})'.format(col_str, var_str)
    sql_record = 'INSERT INTO tx_record_data (well_root_no, district_no, lease_no, well_no, file_source, file_line_num, record_key, data_comm, record_text) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    well_count = len(output_data.keys())
    well_num = 1
    for well_root_id in output_data.keys():
        well_root_no = well_root_id[2:10]
        district_no = well_root_id[12:14]
        lease_no = well_root_id[14:19]
        well_no = well_root_id[20:26]
        well_info = output_data[well_root_id]
        print 'well({}): {}/{}'.format(well_root_id[:26], well_num, well_count)
        for record_key in well_info.keys():
            well_records = well_info[record_key]
            well_rec_count = len(well_records)
            well_rec_num = 1
            for well_record, dataline_num in well_records:
                last_indx = 0
                record_data = (well_root_no, district_no, lease_no, well_no)
                if record_key == '02':
                    for i in range(len(tx_oil[record_key][:-1])):
                        segment_len = tx_oil[record_key][i][0]
                        is_comp_3 = tx_oil[record_key][i][1]
                        curr_indx = last_indx + segment_len
                        segment_rec = gd.decode_str(well_record[last_indx:curr_indx], encoding='latin-1')
                        if is_comp_3 and 0:
                            test_rec = codecs.decode(segment_rec, 'cp500').encode('cp500')
                            hex_rec = codecs.encode(test_rec, 'hex')
                            new_hex = ''
                            for col in range(len(test_rec)):
                                hex_char = hex_rec[col * 2:(col + 1) * 2].lower()
                                if hex_char in comp_3_nums.keys():
                                    hex_char = str(comp_3_nums[hex_char])
                                new_hex += hex_char
                            new_hex = codecs.decode(new_hex, 'hex').encode('latin-1')
                            segment_rec = str(int(new_hex))
                        record_data += (segment_rec,)
                        last_indx = curr_indx
                    try:
                        curr.execute(sql_insert, record_data)
                        gd.commit(curr)
                    except:
                        rec_data = ()
                        for rec in record_data:
                            try:
                                test_rec = codecs.encode(rec, 'latin-1')
                            except:
                                test_rec = codecs.decode(rec, 'cp500').encode('cp500')
                                hex_rec = codecs.encode(test_rec, 'hex')
                                new_hex = ''
                                for col in range(len(test_rec)):
                                    hex_char = hex_rec[col * 2:(col + 1) * 2]
                                    if hex_char in comp_3_nums.keys():
                                        hex_char = str(comp_3_nums[hex_char])
                                    new_hex += hex_char
                                new_hex = codecs.decode(new_hex, 'hex').encode('latin-1')
                                rec = int(new_hex)
                            rec_data += (rec,)
                        curr.execute(sql_insert, rec_data)
                        gd.commit(curr)
                else:
                    data_comm = input_file[3:6].upper()
                    record_data += (input_file, dataline_num, record_key, data_comm, well_record)
                    try:
                        curr.execute(sql_record, record_data)
                        gd.commit(curr)
                    except:
                        print 'SQL error: {} - {} - {} - {} - {} - {} - {} - {}'.format(well_root_no, district_no, lease_no, well_no, input_file, dataline_num, record_key, data_comm)
                well_rec_num += 1
        well_num += 1
    curr.close()
    conn.close()


def store_record_data(output_data, input_file):
    conn = gd.get_connection(server='mysql', database='well_data')
    curr = conn.cursor()
    sql_record = 'INSERT INTO tx_{}_record_data (well_root_no, district_no, lease_no, well_no, file_source, file_line_num, record_key, data_comm, record_text) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    well_count = len(output_data.keys())
    well_num = 1
    for well_root_id in output_data.keys():
        well_root_no = well_root_id[2:10]
        district_no = well_root_id[12:14]
        lease_no = well_root_id[14:20]
        well_no = well_root_id[20:26]
        well_info = output_data[well_root_id]
        print 'well({}): {}/{}'.format(well_root_id[:26], well_num, well_count)
        #for record_key in [rec_key for rec_key in well_info.keys() if rec_key not in ['01', '15']]:
        for record_key in ['21']:
            well_records = well_info[record_key]
            well_rec_count = len(well_records)
            well_rec_num = 1
            for well_record, dataline_num in well_records:
                last_indx = 0
                data_comm = input_file[3:6].upper()
                if record_key == '20' and 0:
                    try:
                        well_record = well_record.decode('utf-8')
                    except:
                        well_record = well_record.encode('utf-8')
                    test_rec = codecs.decode(well_record, 'cp500').encode('cp500')
                    rec_data = codecs.encode(test_rec, 'hex')
                    print '*' * 100
                    rec_output = ''
                    rec_print = ''
                    for col in range(1, 229):
                        start_indx = (col - 1) * 2
                        end_indx = (col) * 2
                        hex_val = rec_data[start_indx:end_indx]
                        print 1, hex_val
                        hex_rec_key = '3230'
                        if col in comp_3_data[data_comm.lower()][hex_rec_key]:
                            hex_val = comp_3_conv_[hex_val]
                            print 2, hex_val
                        rec_output += hex_val
                        rec_print += hex_val + ' '
                    print 'rec_print: {}'.format(rec_print)
                    print 'rec_output: {}'.format(rec_output)
                    rec_output = codecs.decode(rec_output, 'hex')
                    # rec_output = rec_output.decode('cp500').encode('latin-1')
                    rec_output = rec_output.encode('latin-1')
                    well_record = rec_output
                record_data = (well_root_no, district_no, lease_no, well_no, input_file, dataline_num, record_key, data_comm, well_record)
                try:
                    curr.execute(sql_record.format(data_comm), record_data)
                    gd.commit(curr)
                except:
                    try:
                        record_data = (well_root_no, district_no, lease_no, well_no, input_file, dataline_num, record_key, data_comm, (well_record[:-1].strip()).encode('utf-8'))
                        print '1 SQL error: {}-{}-{}-{}-{}-{}-{}-{}'.format(well_root_no, district_no, lease_no, well_no, input_file, dataline_num, record_key, data_comm)
                        print '1 {}'.format((sql_record.format(data_comm) % record_data).encode('utf-8'))
                    except:
                        print '2 SQL error: {}-{}-{}-{}-{}-{}-{}-{}'.format(well_root_no, district_no, lease_no, well_no, input_file, dataline_num, record_key, data_comm)
                        print '2 {}'.format((sql_record.format(data_comm) % record_data).decode('utf-8'))
                    curr.execute(sql_record.format(data_comm), record_data)
                    gd.commit(curr)
                well_rec_num += 1
        well_num += 1
    curr.close()
    conn.close()


def process_tx_oil_data(input_dir, input_file):
    output_data = {'': {record_key: [] for record_key in tx_oil.keys()}}
    with io.open(input_dir + input_file, encoding='latin-1') as tx_file:
        datalines = tx_file.readlines()
        root_segment = ''
        dataline_count = len(datalines)
        dataline_num = 1
        for dataline in datalines:
            print 'processing line: {}/{}'.format(dataline_num, dataline_count)
            record_key = dataline[:2]
            if record_key == '01':
                root_segment = dataline[:112]
                output_data[root_segment] = {rec_key: [] for rec_key in tx_oil.keys()}
            output_data[root_segment][record_key].append((dataline, dataline_num))
            dataline_num += 1
    parse_datalines(output_data, input_file)


def process_tx_data(input_dir, infile_temp, file_nums, data_comm):
    root_segment = ''
    for file_num in file_nums:
        input_file = infile_temp.format(file_num)
        output_data = {root_segment: {record_key: [] for record_key in tx_record_tables[data_comm].keys()}}
        with io.open(input_dir + input_file, encoding='latin-1') as tx_file:
            datalines = tx_file.readlines()
            dataline_count = len(datalines)
            dataline_num = 1
            last_dataline = ''
            for dataline in datalines:
                print 'processing line: {}/{}'.format(dataline_num, dataline_count)
                record_key = dataline[:2]
                if record_key == '01':
                    root_segment = dataline[:112]
                    output_data[root_segment] = {rec_key: [] for rec_key in tx_record_tables[data_comm].keys()}
                try:
                    output_data[root_segment][record_key].append((dataline, dataline_num))
                except:
                    output_data[root_segment][last_dataline[:2]][-1][0] += dataline
                last_dataline = dataline
                dataline_num += 1
        store_record_data(output_data, input_file)


def store_wb_record_data(output_data, input_file, root_segments):
    conn = gd.get_connection(server='mysql', database='us_wells')
    curr = conn.cursor()
    sql_record = 'INSERT INTO tx_wellbore_record_data (record_key, wellbore_api_root, county_no, unique_api, district_no, total_depth, file_source, file_source_line, data_table, root_segment, record_text) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    well_count = len(output_data.keys())
    well_num = 1
    for well_root_id in root_segments:
        root_segment      = well_root_id
        record_key        = well_root_id[:2]
        wellbore_api_root = well_root_id[2:10]
        county_no         = well_root_id[2:5]
        unique_api        = well_root_id[5:10]
        district_no       = well_root_id[14:16]
        total_depth       = well_root_id[28:33]
        file_source       = input_file
        well_info         = output_data[well_root_id]
        print 'well({}): {}/{}'.format(wellbore_api_root, well_num, well_count)
        for record_key in ['23']:
            well_records = well_info[record_key]
            well_rec_count = len(well_records)
            well_rec_num = 1
            for well_record, file_source_line in well_records:
                well_rec_len = len(well_record)
                try:
                    record_data = (record_key, wellbore_api_root, county_no, unique_api, district_no, total_depth, file_source, file_source_line, tx_wb_record_tables[record_key], root_segment, well_record)
                    print  '{}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}'.format(*record_data)
                    curr.execute(sql_record, record_data)
                    gd.commit(curr)
                except:
                    well_record = '*'*20
                    record_data = (record_key, wellbore_api_root, county_no, unique_api, district_no, total_depth, file_source, file_source_line, tx_wb_record_tables[record_key], root_segment, well_record)
                    print  '{}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}  --  {}'.format(*record_data)
                    curr.execute(sql_record, record_data)
                    gd.commit(curr)
                well_rec_num += 1
        well_num += 1
    curr.close()
    conn.close()


def process_tx_wb_data(input_dir='D:\\Documents\\', infile_temp='dbf900_{}.txt', file_nums=['01']):
    root_segment = ''
    root_segments = []
    for file_num in file_nums:
        input_file = infile_temp.format(file_num)
        output_data = {root_segment: {record_key: [] for record_key in tx_wb_record_tables.keys()}}
        with open(input_dir + input_file) as tx_file:
            datalines = tx_file.readlines()
            dataline_count = len(datalines)
            dataline_num = 1
            last_dataline = ''
            for dataline in datalines:
                print 'processing line: {}/{}'.format(dataline_num, dataline_count)
                record_key = dataline[:2]
                if record_key == '01':
                    root_segment = dataline[:162]
                    root_segments.append(root_segment)
                    output_data[root_segment] = {rec_key: [] for rec_key in tx_wb_record_tables.keys()}
                try:
                    output_data[root_segment][record_key].append((dataline, dataline_num))
                except:
                    output_data[root_segment][last_dataline[:2]][-1][0] += dataline
                last_dataline = dataline
                dataline_num += 1
        store_wb_record_data(output_data, input_file, root_segments)


def extract_read_data(data_comm):
    record_keys = {
        'oil': [
            'WLROOT',
            'WLORPTCY',
            'WLOPRVAL',
            'WLOFRMLK',
            'WLOFRMDS',
            'WLOETEX',
            'WLOETDS',
            'WLOALTF',
            'WLOTFWL',
            'WLPHPROD',
            'WLOPVTYP',
            'WLPHBAL',
            'WLOW10',
            'WLOPVW10',
            'WLREMARK',
            'WLSEAL',
            'WLOUIC',
            'WLSB126'
        ],
        'gas': [
            'WLROOT',
            'WLREMARK',
            'WLSEAL',
            'WLGG1',
            'WLGG10',
            'WLGPVG10',
            'WLGC1',
            'WLGRPTCY',
            'WLGFRMLK',
            'WLGFRMDS',
            'WLGALTF',
            'WLGPRVAL',
            'WLGUIC',
            'WLSB126'
        ]
    }
    tape_data = {
        'oil': {rec_key: {} for rec_key in record_keys['oil']},
        'gas': {rec_key: {} for rec_key in record_keys['gas']}
    }
    with open(HEADER_FILE.format(data_comm)) as tx_file:
        datalines = tx_file.readlines()
        record_key = ''
        in_record_key_sec = 0
        in_record_col_sec = 1
        for dataline in datalines:
            if '*' * 65 in dataline:
                in_record_key_sec = (1 - in_record_key_sec)
                in_record_col_sec = (1 - in_record_col_sec)
            if 'SEGMENT_NAME:' in dataline:
                line_parts = dataline.split()
                record_key = [line_part.strip()[13:] for line_part in line_parts if 'SEGMENT_NAME:' in line_part][0]
                in_record_key_sec = 1
                in_record_col_sec = 0
            if in_record_col_sec:
                try:
                    line_parts = dataline.split()
                    if line_parts and line_parts[0] in ['02', '03', '05', '10'] and ' PIC-' in dataline and dataline[-2:] != '.\n':
                        record_segment = line_parts[1]
                        tape_data[data_comm][record_key][record_segment] = {'data_type': '', 'default_val': '', 'start_indx': 0}
                        for line_part in line_parts:
                            if 'PIC-' in line_part:
                                tape_data[data_comm][record_key][record_segment]['data_type'] = line_part.strip()
                            elif 'VALUE' in line_part:
                                tape_data[data_comm][record_key][record_segment]['default_val'] = line_part.strip()
                            elif line_part == line_parts[-1] and line_part.isdigit():
                                tape_data[data_comm][record_key][record_segment]['start_indx'] = int(line_part.strip())
                except:
                    pass

    for record_key in tape_data[data_comm].keys():
        for rec_segment in tape_data[data_comm][record_key].keys():
            rec_data = tape_data[data_comm][record_key][rec_segment]
            print '{},{},{},{},{},{}'.format(record_key, data_comm.upper(), rec_segment, rec_data['data_type'], rec_data['default_val'], rec_data['start_indx'])


def create_tx_data_tables(tx_data_table=None, data_comm='oil'):
    conn = gd.get_connection(server='mysql', database='well_data')
    curr = conn.cursor()
    sql_drop = 'DROP TABLE IF EXISTS {}'
    sql_create = \
        '''
        CREATE TABLE `{0}` (
          `id` INT(11) NOT NULL AUTO_INCREMENT,
          `well_root_no` VARCHAR(8) DEFAULT NULL,
          `api_number` VARCHAR(20) DEFAULT NULL,
          `lease_no` VARCHAR(6) DEFAULT NULL,
          `well_no` VARCHAR(6) DEFAULT NULL,
          `district_no` VARCHAR(2) DEFAULT NULL,
          `oil_gas_code` CHAR(1) DEFAULT NULL,
          {1}`root_segment` VARCHAR(350) DEFAUL NULL,
          `record_text` VARCHAR(350) DEFAULT NULL,
          PRIMARY KEY (`id`),
          INDEX well_root_indx (`well_root_no`),
          INDEX well_api_indx (`api_number`),
          INDEX lease_indx (`lease_no`),
          INDEX well_no_indx (`lease_no`, `well_no`),
          INDEX district_indx (`district_no`),
          INDEX record_key_indx (`record_key`)
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin-1'''
    if tx_data_table:
        tx_data_tables = [tx_data_table]
    else:
        tx_data_tables = gd.get_data(param='data_table', table='tx_header_data', database='well_data', sql_where='data_comm="{}"'.format(data_comm))
    print tx_data_tables

    for data_table in [table for table in tx_data_tables if table != 'tx_oil_rptcy']:
        col_create = ''
        tbl_schema_data = gd.get_data('column_name, sql_data_type', table='tx_header_data', sql_where='data_table="{}" ORDER BY header_position'.format(data_table), datatype='plural', database='well_data')
        for col_name, data_type in tbl_schema_data:
            col_create += '`{}` {} DEFAULT NULL,\n  '.format(col_name, data_type)
        try:
            curr.execute(sql_drop.format(data_table))
            gd.commit(curr)
            curr.execute(sql_create.format(data_table, col_create))
            gd.commit(curr)
        except:
            print sql_create.format(data_table, col_create)
    curr.close()
    conn.close()


def create_tx_wb_data_tables(tx_data_table=None):
    conn = gd.get_connection(server='mysql', database='us_wells')
    curr = conn.cursor()
    sql_drop = 'DROP TABLE IF EXISTS {}'
    sql_create = \
        '''
CREATE TABLE us_wells.`{0}` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `wellbore_api_root` VARCHAR(8) DEFAULT NULL,
  `well_root_no` VARCHAR(8) DEFAULT NULL,
  `api_number` VARCHAR(20) DEFAULT NULL,
  `lease_no` VARCHAR(6) DEFAULT NULL,
  `well_no` VARCHAR(6) DEFAULT NULL,
  `district_no` VARCHAR(2) DEFAULT NULL,
  {1}`root_segment` VARCHAR(350) DEFAULT NULL,
  `record_text` VARCHAR(350) DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX well_root_indx (`well_root_no`),
  INDEX wellbore_api_indx (`wellbore_api_root`),
  INDEX well_api_indx (`api_number`),
  INDEX lease_indx (`lease_no`),
  INDEX well_no_indx (`lease_no`, `well_no`),
  INDEX district_indx (`district_no`),
  INDEX record_key_indx (`record_key`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8'''
    if tx_data_table:
        tx_data_tables = [tx_data_table]
    else:
        tx_data_tables = gd.get_data(param='data_table', table='tx_wellbore_header_data', database='us_wells', sql_where='NOT data_table="tx_wb_root"')

    print tx_data_tables

    for data_table in tx_data_tables:
        col_create = ''
        tbl_schema_data = gd.get_data('column_name, sql_data_type', table='tx_wellbore_header_data', sql_where='data_table="{}" ORDER BY header_position'.format(data_table), datatype='plural', database='us_wells')
        for col_name, data_type in tbl_schema_data:
            col_create += '`{}` {} DEFAULT NULL,\n  '.format(col_name, data_type)
        #try:
        curr.execute(sql_drop.format(data_table))
        gd.commit(curr)
        curr.execute(sql_create.format(data_table, col_create))
        gd.commit(curr)
        #except:
        #    print sql_create.format(data_table, col_create)
    curr.close()
    conn.close()


def insert_decimal():
    conn = gd.get_connection(server='mysql', database='well_data')
    curr = conn.cursor()
    tx_data_tables = gd.get_data(param='data_table', table='tx_header_data', database='well_data', sql_where='sql_data_type LIKE "DECIMAL%"')
    for data_table in tx_data_tables:
        sql_update = "UPDATE {0} SET {1}=CONCAT(SUBSTR({1},1,LENGTH({1})-{2}), '.', SUBSTR({1}, (LENGTH({1})-{2})+1, {2}))"
        dec_col_data = gd.get_data('column_name, sql_data_type', 'tx_header_data', database='well_data', sql_where='sql_data_type LIKE "DECIMAL%"')
        for col_name, data_type in dec_col_data:
            decimal_vals = int(data_type[-2])
            curr.execute(sql_update.format(data_table, col_name, decimal_vals))
            gd.commit(curr)
    curr.close()
    conn.close()


def add_indexing_cols(update=False, debug=False):
    conn = gd.get_connection(server='mysql', database='well_data')
    curr = conn.cursor()
    sql_alter = \
        '''
        ALTER TABLE {}
          ADD COLUMN well_root_no VARCHAR(8) DEFAULT NULL AFTER id,
          ADD COLUMN lease_no VARCHAR(5) DEFAULT NULL AFTER well_root_no,
          ADD COLUMN well_no VARCHAR(6) DEFAULT NULL AFTER lease_no,
          ADD COLUMN district_no VARCHAR(2) DEFAULT NULL AFTER well_no
          ADD COLUMN record_text VARCHAR(250) DEFAULT NULL;'''
    sql_update = 'UPDATE {} SET well_root_no=SUBSTR(well_root_id,3,8), lease_no=SUBSTR(well_root_id,15,5), well_no=SUBSTR(well_root_id,21,6), district_no=SUBSTR(well_root_id,13,2)'
    tx_data_tables = gd.get_data('data_table', 'tx_header_data', database='well_data')
    for data_table in tx_data_tables:
        if debug:
            print sql_alter.format(data_table)
            if update: print sql_update.format(data_table)
        curr.execute(sql_alter.format(data_table))
        gd.commit(curr)
        if update:
            curr.execute(sql_update.format(data_table))
            gd.commit(curr)
    curr.close()
    conn.close()


def insert_record_data(debug=False, data_comm='oil', tx_rec_key=None, exclude=[]):
    conn = gd.get_connection(server='mysql', database='well_data')
    curr = conn.cursor()
    sql_insert = 'INSERT INTO {} (well_root_no, well_api, lease_no, well_no, district_no, record_text) (SELECT DISTINCT well_root_no, well_api, lease_no, well_no, district_no, record_text FROM tx_{}_record_data WHERE record_key="{}")'
    if tx_rec_key:
        data_table = tx_record_tables[data_comm][tx_rec_key]
        if debug:
            print sql_insert.format(data_table, data_comm, tx_rec_key)
        curr.execute(sql_insert.format(data_table, data_comm, tx_rec_key))
        gd.commit(curr)
    else:
        tx_record_keys = gd.get_data('record_key', 'tx_{}_record_data'.format(data_comm), database='well_data', sql_where='data_comm="{}"'.format(data_comm))
        for rec_key in [rkey for rkey in tx_record_keys if rkey not in exclude]:
            data_table = tx_record_tables[data_comm][rec_key]
            if debug:
                print sql_insert.format(data_table, data_comm, rec_key)
            curr.execute(sql_insert.format(data_table, data_comm, rec_key))
            gd.commit(curr)
    curr.close()
    conn.close()


def insert_wb_record_data(debug=False, tx_rec_key=None, exclude=[]):
    conn = gd.get_connection(server='mysql', database='us_wells')
    curr = conn.cursor()
    sql_insert = 'INSERT INTO {} (wellbore_api_root, api_number, root_segment, record_text, file_source_line) (SELECT DISTINCT wellbore_api_root, unique_api, root_segment, record_text, file_source_line FROM tx_wellbore_record_data WHERE record_key="{}")'
    if tx_rec_key:
        data_table = tx_wb_record_tables[tx_rec_key]
        if debug:
            print sql_insert.format(data_table, tx_rec_key)
        curr.execute(sql_insert.format(data_table, tx_rec_key))
        gd.commit(curr)
    else:
        tx_record_keys = gd.get_data('record_key', 'tx_wellbore_record_data', database='us_wells')
        for rec_key in [rkey for rkey in tx_record_keys if rkey not in exclude]:
            data_table = tx_wb_record_tables[rec_key]
            print sql_insert.format(data_table, rec_key)
            curr.execute(sql_insert.format(data_table, rec_key))
            gd.commit(curr)
    curr.close()
    conn.close()


def parse_wb_record_data(exclude=[], start_index=1, column_start=0):
    conn = gd.get_connection(server='mysql', database='us_wells')
    curr = conn.cursor()
    sql_alter = 'ALTER TABLE {} CHANGE {} {} VARCHAR({}) DEFAULT NULL'
    sql_update = 'UPDATE {} SET {}=SUBSTR(record_text,{},{})'
    sql_update_dec = 'UPDATE {} SET {}=CONCAT(SUBSTR(record_text,{},{}),".",SUBSTR(record_text,{},{}))'
    record_keys = gd.get_data('record_key', 'tx_wellbore_record_data', database='us_wells')
    start_indx = start_index
    col_start  = column_start
    for rec_key in [rkey for rkey in record_keys if rkey not in exclude]:
        record_table = tx_wb_record_tables[rec_key]
        table_data = tx_wb_table_data[record_table]
        current_index = start_indx
        for data_len, col_name, dec_plcs in table_data[col_start:-1]:
            if dec_plcs:
                data_sub_len = data_len - dec_plcs
                print sql_update_dec.format(record_table, col_name, current_index, data_sub_len, current_index + data_sub_len, dec_plcs)
                try:
                    curr.execute(sql_update_dec.format(record_table, col_name, current_index, data_sub_len, current_index + data_sub_len, dec_plcs))
                    gd.commit(curr)
                except:
                    curr.execute(sql_alter.format(record_table, col_name, col_name, data_len+1))
                    gd.commit(curr)
                    curr.execute(sql_update_dec.format(record_table, col_name, current_index, data_sub_len, current_index + data_sub_len, dec_plcs))
                    gd.commit(curr)
            else:
                print sql_update.format(record_table, col_name, current_index, data_len)
                try:
                    curr.execute(sql_update.format(record_table, col_name, current_index, data_len))
                    gd.commit(curr)
                except:
                    curr.execute(sql_alter.format(record_table, col_name, col_name, data_len+1))
                    gd.commit(curr)
                    curr.execute(sql_update.format(record_table, col_name, current_index, data_len))
                    gd.commit(curr)

            current_index += data_len
        start_indx = 1
        col_start  = 0
    curr.close()
    conn.close()


def parse_record_data(exclude=[], data_comm='oil', start_index=1, column_start=0):
    conn = gd.get_connection(server='mysql', database='well_data')
    curr = conn.cursor()
    sql_update = 'UPDATE {} SET {}=SUBSTR(record_text,{},{})'
    sql_update_dec = 'UPDATE {} SET {}=CONCAT(SUBSTR(record_text,{},{}),".",SUBSTR(record_text,{},{}))'
    record_keys = gd.get_data('record_key', 'tx_{}_record_data'.format(data_comm), database='well_data', sql_where='data_comm="{}"'.format(data_comm))
    for rec_key in [rkey for rkey in record_keys if rkey not in exclude]:
        record_table = tx_record_tables[data_comm][rec_key]
        table_data = tx_table_data[record_table]
        current_index = start_index
        for data_len, col_name, dec_plcs in table_data[column_start:-1]:
            if dec_plcs:
                data_sub_len = data_len - dec_plcs
                print sql_update_dec.format(record_table, col_name, current_index, data_sub_len, current_index + data_sub_len, dec_plcs)
                curr.execute(sql_update_dec.format(record_table, col_name, current_index, data_sub_len, current_index + data_sub_len, dec_plcs))
            else:
                print sql_update.format(record_table, col_name, current_index, data_len)
                curr.execute(sql_update.format(record_table, col_name, current_index, data_len))
            gd.commit(curr)
            current_index += data_len
    curr.close()
    conn.close()



def tx_lease_to_well_prod():
    conn = gd.get_connection(server='mysql', database='us_wells')
    curr = conn.cursor()
    month_names = [
        'jan',
        'feb',
        'mar',
        'apr',
        'may',
        'jun',
        'jul',
        'aug',
        'sep',
        'oct',
        'nov',
        'dec'
    ]
    sql_update = \
    '''
    UPDATE tx_oil_well_production AS a, tx_oil_data AS c 
      SET a.oil_{0}_bbl=c.well_allowable_pct, a.csgd_{0}_mcf=c.well_allowable_pct
      WHERE c.prod_month='{0}' AND a.prod_year=c.prod_year AND a.tx_well_id=c.tx_well_id
    '''
    for prod_month in month_names:
        print sql_update.format(prod_month)
        curr.execute(sql_update.format(prod_month))
        gd.commit(curr)
    sql_update = \
    '''
    UPDATE tx_oil_well_production AS a, tx_well_production AS b, tx_oil_data AS c 
      SET a.oil_{0}_bbl=(c.well_allowable_pct * b.oil_{0}_bbl), a.csgd_{0}_mcf=(c.well_allowable_pct * b.csgd_{0}_mcf) 
      WHERE c.prod_month='{0}' AND a.prod_year=c.prod_year AND a.prod_year=b.prod_year AND a.lease_id=b.lease_id AND a.tx_well_id=c.tx_well_id
    '''
    curr.close()
    conn.close()


def main(input_dir=HEX_FILE_DIR, output_dir=HEX_FILE_DIR, input_file=HEX_IN_FILE, output_file=HEX_OUT_FILE, data_comm='oil', record_key=None, process_wb_data=False, parse_exclude=[], column_start=0, start_index=1, insert_exclude=[], create_tbls=False, table_type='wb', tbl_name='', extract_headers=False, comp_3_cols=False, convert=False, file_nums=[], store=False, insert=False, parse=False, debug=False):
    if create_tbls:
        if table_type == 'og':
            create_tx_data_tables(tx_data_table=tbl_name, data_comm=data_comm)
        elif table_type == 'wb':
            create_tx_wb_data_tables()
    if extract_headers:
        extract_read_data(data_comm)
    if comp_3_cols:
        get_comp_3_cols(data_comm)
    if convert:
        for file_num in file_nums:
            convert_ebc_file(input_dir, output_dir, input_file.format(file_num), output_file.format(file_num), data_comm=data_comm)
    if store:
        process_tx_data(input_dir, infile_temp=HEX_OUT_FILE, file_nums=file_nums, data_comm=data_comm)
    if insert:
        if table_type == 'og':
            insert_record_data(debug=debug, data_comm=data_comm, tx_rec_key=record_key, exclude=insert_exclude)
        elif table_type == 'wb':
            insert_wb_record_data(debug=debug, tx_rec_key=record_key, exclude=insert_exclude)
    if parse:
        if table_type == 'og':
            parse_record_data(data_comm=data_comm, exclude=parse_exclude, start_index=start_index, column_start=column_start)
        elif table_type == 'wb':
            parse_wb_record_data(exclude=parse_exclude, start_index=start_index, column_start=column_start)

    if process_wb_data:
        process_tx_wb_data()


if __name__ == '__main__':
    #update_wb_oil_gas_key_data(debug=True)
    '13','14','15','16','17','18','19','20','21','22','24','25','26','27','28'
    main(process_wb_data=False, data_comm='gas', create_tbls=False, table_type='wb', convert=False, file_nums=FILE_NUMS, store=False, insert=False, parse=True, record_key='23', insert_exclude=['01'], column_start=0, start_index=1, debug=False, tbl_name='tx_gas_c1', parse_exclude=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11','12','13','14','15','16','17','18','19','20','21','22','24','25','26','27','28'])
