import pp

ppservers = ("*",)  # autodiscovery mode on!

# create the job server
job_server = pp.Server(ppservers=ppservers)

print "Starting pp! Local machine has {} workers (cores) available.".format(job_server.get_ncpus())