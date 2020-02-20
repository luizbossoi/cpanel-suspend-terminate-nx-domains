# cpanel-suspend-terminate-nx-domains
This script is used to suspend or terminate cPanel accounts that are no longer in use, not pointing to your domain nameserver.

For example: if "yourdomain.com" is not pointing to "ns1.yourhost.com", this account will be suspended or terminated, based on your needs.

# Configuration
Edit this script and change these variables:

	CONF_USERSPATH = "/var/cpanel/users/"
	CONF_HOSTDOMAIN = "YOURHOST.COM"
	CONF_CPANELSUSPEND = "/scripts/suspendacct"

Where: 
 - "CONF_HOSTDOMAIN" is your main domain nameserver
 - "CONF_USERSPATH" is your cPanel users folder (default is already set)
 - "CONF_CPANELSUSPEND" is the suspend script and can be replaced by "/scripts/removeacct" if you wish to terminate accounts instead of suspend.

# How to run
Just enter python suspend-unused.py

# Requirements
Make sure you have all modules installed, if not, run pip install -r requirements.txt 

#
