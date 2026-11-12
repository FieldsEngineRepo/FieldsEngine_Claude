import globaldata as gd
import os


class DatabaseLogTool:
	def __init__(self, server, database):
		self.server = server
		self.database = database
		self.log_filename = self.get_log_filename()
		self.log_exists = self.log_exists_check()

	def get_log_filename(self):
		return 'database_logs/{}_{}.log'.format(self.server, self.database)

	def log_exists_check(self):
		return os.path.exists(self.log_filename)

	def log_write(self, sql_command, command_time):
		with open(self.log_filename, 'a') as log_file:
			log_output = ''
			if not self.log_exists:
				print 'Creating log: {log_name} for {server_type}/{database_name} database ...'.format(
					log_name=os.path.basename(self.log_filename),
					server_type=self.server,
					database_name=self.database
				)
				log_header = 'Database log for {}/{} Created On: {}\nExecuted At:\t\t\tExecution Time:\t\tCommand Text:\n\n'
				log_output += log_header.format(self.server, self.database, gd.get_datetime())
				self.log_exists = True
			sql_command = sql_command.strip()
			if sql_command[-1] != ';':
				sql_command = sql_command + ';'
			sql_command = sql_command.replace('\n', '\n' + (' ' * 46))
			log_output += '{}\t\t{}\t\t\t{}\n\n'.format(gd.get_datetime(), command_time, sql_command)
			log_file.write(log_output)
	
	def log_read(self, show=False):
		log_dict = {}
		command_num = 1
		with open(self.log_filename, 'r') as log_file:
			for log_entry in log_file.read().split('\n\n')[1:-1]:
				if show:
					print log_entry
				log_components = log_entry.strip().split('\t\t')
				executed_at, execution_time = log_components[:2]
				command_text = ' '.join([command_part.strip() for command_part in log_components[2].split('\n')])
				log_dict[command_num] = (executed_at.strip(), execution_time.strip(), command_text.strip())
				command_num += 1
		return log_dict
	
	
class DatabaseUpdater:
	def __init__(self, server, database):
		self.server = server
		self.database = database
		self.conn = self.get_conn()
		self.curr = self.conn.cursor()
		self.curr_command = ''
		self.command_time = '00:00:00'
		self.log_tool = DatabaseLogTool(self.server, self.database)

	def get_conn(self):
		connection = gd.get_connection(server=self.server, database=self.database)
		return connection

	def close(self):
		self.curr.close()
		self.conn.close()

	def log(self):
		self.log_tool.log_write(self.curr_command, self.command_time)

	def execute(self):
		command_start = gd.get_datetime()
		self.curr.execute(self.curr_command)
		gd.commit(self.curr)
		command_end = gd.get_datetime()
		self.command_time = gd.elapsed_time(command_start, command_end)
		self.log()

	def truncate(self, table):
		self.curr_command = 'TRUNCATE TABLE {}'.format(table)
		self.execute()

	def update(self, sql_command):
		self.curr_command = sql_command
		self.execute()


if __name__ == '__main__':
	db = DatabaseUpdater('sql_server', 'US_Wells_Texas')
	db.update("UPDATE tx_well_details SET process_code=2 \
WHERE well_id IN (SELECT DISTINCT WellID FROM US_Wells.dbo.tblUSWell_Parameters WHERE State_Name!='Texas')")
	db.update("""
UPDATE tx_well_details
SET well_id=b.WellID
FROM tx_well_details a, US_Wells.dbo.tblUSWell_Parameters b
WHERE a.tx_well_id=b.API_Number;""")
	log_dict = db.log_tool.log_read(show=True)


