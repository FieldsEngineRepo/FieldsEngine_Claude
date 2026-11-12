import globaldata as gd
import sys

class EngineValidation():
    def __init__(self, test_data=False, run_id=''):
        self.test_data                  = test_data
        self.engine_run_id              = run_id
        self.run_id                     = self.get_run_id()
        #self.int_conn                   = self.get_conn(server_loc='int')
        #self.int_curr                   = self.get_curr(server_loc='int')
        #self.ext_conn                   = self.get_conn(server_loc='ext')
        #self.ext_curr                   = self.get_curr(server_loc='ext')
        self.exp_eligible_asset_count   = self.count_eligible_assets(count_type='expected')
        self.act_eligible_asset_count   = self.count_eligible_assets(count_type='actual')
        self.exp_uncon_model_count      = self.count_uncon_models(count_type='expected')
        self.act_uncon_model_count      = self.count_uncon_models(count_type='actual')
        self.exp_detailed_model_count   = self.count_detailed_models(count_type='expected')
        self.act_detailed_model_count   = self.count_detailed_models(count_type='actual')
        self.exp_disc_field_model_count = self.count_disc_field_models(count_type='expected')
        self.act_disc_field_model_count = self.count_disc_field_models(count_type='actual')


    def get_run_id(self):
        if self.engine_run_id:
            self.run_id = self.engine_run_id
        else:
            self.run_id = gd.get_run_id()
        return self.run_id

    def get_conn(self, server_loc):
        if server_loc == 'int':
            conn = gd.get_connection()
        elif server_loc == 'ext':
            if self.test_data:
                conn = gd.get_connection(server='sql_server', database='OGEngineDataExtract_Effuah', external=True)
            else:
                try:
                    conn = gd.get_connection(server='sql_server', database='OGEngineDataExtract', external=True)
                except:
                    print ' Connection to external server failed. Connecting to internal SQL server ...'
                    conn = gd.get_connection(server='sql_server', database='OGEngineDataExtract', external=False)
        else:
            print 'Server location must be specified as "int" or "ext" depending on if server is internal or external'
            sys.exit(1)
        return conn

    def get_curr(self, server_loc):
        if server_loc in ['int', 'ext']:
            conn = self.get_conn(server_loc)
        else:
            print 'Server location must be specified as "int" or "ext" depending on if server is internal or external'
            sys.exit(1)
        return conn.cursor()

    def count_eligible_assets(self, count_type):
        eligible_asset_count = 0
        if count_type == 'expected':
            param     = "COUNT(DISTINCT asset_id)"
            table     = "assets"
            sql_where = "data_source='Engine' AND asset_relation='Parent' AND `status` IN ('Planned', 'Abandoned', 'Announced', 'Producing', 'Stalled') "
            eligible_asset_count = gd.get_data(param=param, table=table, sql_where=sql_where, datatype='int', single_value=True)
        elif count_type == 'actual':
            param     = "COUNT(DISTINCT asset_id)"
            table     = "param_track"
            sql_where = "session_key LIKE '%{}%'".format(self.run_id)
            eligible_asset_count = gd.get_data(param=param, table=table, sql_where=sql_where, datatype='int', single_value=True)
        return eligible_asset_count

    def count_modelled_assets(self, count_type):
        modelled_asset_count = 0
        if count_type == 'expected':
            param     = "COUNT(DISTINCT asset_id)"
            table     = "param_track"
            sql_where = "session_key LIKE '%{}%' AND NOT fiscal_regime_chosen IS NULL "
            modelled_asset_count = gd.get_data(param=param, table=table, sql_where=sql_where, datatype='int', single_value=True)
        elif count_type == 'actual':
            param       = "COUNT(DISTINCT asset_id)"
            table_1, table_2     = "econ_data", "engine_asset_log"
            sql_where_1 = "run_id='{}'".format(self.run_id)
            sql_where_2 = "run_id='{}' AND model_type IN ('engine', 'unconventional')".format(self.run_id)
            modelled_asset_count_1 = gd.get_data(param=param, table=table_1, sql_where=sql_where_1, datatype='int', single_value=True)
            modelled_asset_count_2 = gd.get_data(param=param, table=table_2, sql_where=sql_where_2, datatype='int', single_value=True)
            try:
                assert(modelled_asset_count_1 == modelled_asset_count_2)
                modelled_asset_count = modelled_asset_count_1
            except AssertionError:
                print 'Modelled asset count test failed. Actual modelled count of {} in econ_data does not equal modelled count of {} in engine_asset_log.'.format(modelled_asset_count_1, modelled_asset_count_2)
        return modelled_asset_count

    def count_uncon_models(self, count_type):
        uncon_model_count = 0
        if count_type == 'expected':
            param      = "COUNT(DISTINCT asset_id)"
            table      = "assets"
            sql_where  = "data_source='Engine' AND asset_relation='Parent' AND `status` IN ('Planned', 'Abandoned', 'Announced', 'Producing', 'Stalled') "
            sql_where += "AND asset_id IN (SELECT DISTINCT asset_id FROM model_rules WHERE param_name='FISCAL' AND param_value LIKE '%Resource%')"
            uncon_model_count = gd.get_data(param=param, table=table, sql_where=sql_where, datatype='int', single_value=True)
        elif count_type == 'actual':
            param     = "COUNT(DISTINCT asset_id)"
            table     = "engine_asset_log"
            sql_where = "run_id='{}' AND model_type='unconventional'".format(self.run_id)
            uncon_model_count = gd.get_data(param=param, table=table, sql_where=sql_where, datatype='int', single_value=True)
        return uncon_model_count

    def count_detailed_models(self, count_type):
        detailed_model_count = 0
        if count_type == 'expected':
            param      = "COUNT(DISTINCT asset_id)"
            table      = "detailed_model_data"
            sql_where  = "asset_id IN (SELECT asset_id FROM assets WHERE asset_relation='Parent' AND `status` IN ('Planned', 'Abandoned', 'Announced', 'Producing', 'Stalled')) "
            sql_where += "AND NOT asset_id IN (SELECT DISTINCT asset_id FROM model_rules WHERE param_name='FISCAL' AND param_value LIKE '%Resource%') "
            detailed_model_count = gd.get_data(param=param, table=table, sql_where=sql_where, datatype='int', single_value=True)
        elif count_type == 'actual':
            param     = "COUNT(DISTINCT asset_id)"
            table     = "engine_asset_log"
            sql_where = "run_id='{}' AND model_type='detailed'".format(self.run_id)
            detailed_model_count = gd.get_data(param=param, table=table, sql_where=sql_where, datatype='int', single_value=True)
        return detailed_model_count

    def count_disc_field_models(self, count_type):
        discovered_field_count = 0
        if count_type == 'expected':
            param      = "COUNT(DISTINCT asset_id)"
            table      = "field_analogues"
            discovered_field_count = gd.get_data(param=param, table=table, datatype='int', single_value=True)
        elif count_type == 'actual':
            param     = "COUNT(DISTINCT asset_id)"
            table     = "engine_asset_log"
            sql_where = "run_id='{}' AND model_type='discovered'".format(self.run_id)
            discovered_field_count = gd.get_data(param=param, table=table, sql_where=sql_where, datatype='int', single_value=True)
        return discovered_field_count

    def count_automated_panoramas(self):
        pass

    def check_row_count(self):
        # number of expected assets * expected rows per asset
        sql_select = \
            '''
        
            '''
        pass

    def check_asset_count(self):
        # number of expected assets vs number of distinct asset_ids
        sql_select = \
            '''
    
            '''
        pass

    def check_for_duplicates(self):
        # number of rows / number of distinct assets vs number of expected rows per asset
        sql_select = \
            '''
    
            '''
        pass

    def check_created_date(self):
        # distinct created dates vs expected dates and associated counts by created date
        sql_select = \
            '''
    
            '''
        pass

    def check_region_count(self):
        # number of assets in each region vs number of distinct asset_ids counted when grouped by region
        sql_select = \
            '''
    
            '''
        pass

    def update_engine_log(self):
        pass

    def generate_engine_log_report(self):
        pass

    def validate_engine_process(self):
        try:
            assert(self.exp_eligible_asset_count == self.act_eligible_asset_count)
            print 'Eligible asset test passed.'
        except AssertionError:
            print 'Eligible asset test failed. Actual eligible asset count of {} does not equal expected eligible asset count of {}'.format(self.act_eligible_asset_count, self.exp_eligible_asset_count)
        assert(self.exp_uncon_model_count == self.act_uncon_model_count)
        print 'Unconventional model test passed'
        assert(self.exp_detailed_model_count == self.act_detailed_model_count)
        print 'Detailed model test passed'
        assert(self.exp_discovered_field_count == self.act_discovered_field_count)
        print 'Discovered model test passed'


if __name__=='__main__':
    EngineValidation(run_id='20190325_191935').validate_engine_process()

