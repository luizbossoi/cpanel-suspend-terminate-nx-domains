# Script developed by @luizbossoi
# This scripts checks the DNS for each cPanel user and suspend their account
# Condition: If their DNS does not match your host domain nameserver
# General config:
CONF_USERSPATH = "/var/cpanel/users/"
CONF_HOSTDOMAIN = "YOURHOST.COM"
CONF_CPANELSUSPEND = "/scripts/suspendacct"

import glob, dns.resolver, configparser, subprocess, os

class bcolors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'

tot_err = 0
tot_ok = 0
files=glob.glob(CONF_USERSPATH + "*")
for file in files:
	suspend_user = False
	suspend_reason = 'Pointing to this server'
	with open(file, 'r') as f:
		config_string = '[cpanel]\n' + f.read()
		config = configparser.ConfigParser()
		config.read_string(config_string)
		user_main_domain = config['cpanel']['DNS']
		try:
			nameservers = dns.resolver.query(user_main_domain,'NS')
			for data in nameservers:
				if (str(data).find(CONF_HOSTDOMAIN)==-1): suspend_user = True

			if(suspend_user == True):
				suspend_reason = 'Domain NS does not point to *.' + CONF_HOSTDOMAIN

		except dns.resolver.NoNameservers:
			suspend_user = True
			suspend_reason = 'No name servers'
			pass
		except dns.resolver.NoAnswer:
			suspend_user = False
			suspend_reason = '* No Answer *'
			pass
		except dns.resolver.NXDOMAIN:
			suspend_user = True
			suspend_reason = 'NX Domain'
			pass
		except dns.resolver.Timeout:
			suspend_user = False
			suspend_reason = '* DNS Query timed out *'
			pass

		print(bcolors.UNDERLINE + "Checking user " + config['cpanel']['user'] + "(" + user_main_domain + ")" + bcolors.ENDC)
		if (suspend_user == True):
			print(bcolors.FAIL + "\tSuspending account - Reason: " + suspend_reason + bcolors.ENDC)
			subprocess.call([CONF_CPANELSUSPEND, config['cpanel']['user']], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
			tot_err = tot_err +1
		else:
			print(bcolors.OKGREEN + "\tAccount not suspended - " + suspend_reason + bcolors.ENDC)
			tot_ok = tot_ok + 1

print(bcolors.HEADER + "-------------------------------------------------" + bcolors.ENDC)
print(bcolors.FAIL + "Total not pointing to this server: " + str(tot_err) + bcolors.ENDC)
print(bcolors.OKGREEN + "Total pointing to this server: " + str(tot_ok) + bcolors.ENDC)

		
