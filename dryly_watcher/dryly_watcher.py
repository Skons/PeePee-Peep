import requests
import logging, logging.handlers
import json
import os
import time, datetime

def in_between(now, start, end):
	if start <= end:
		return start <= now < end
	else: # over midnight e.g., 23:30-04:15
		return start <= now or now < end

try:
	import socket
	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	## Create an abstract socket, by prefixing it with null.
	s.bind( '\0dryly_watcher')
except socket.error as e:
	print(f"Process already running. Error code '{e.args[0]}'. Error '{e.args[1]}'. Exiting")
	exit()

dryly_base_url = 'https://api.dryly.app/'

# get config file
current_folder = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(current_folder,"dryly_watcher.json")
if os.path.isfile(config_file) == False:
	raise Exception(f"Unable to find config file '{config_file}'")

with open(config_file) as file:
  config_file_contents = file.read()

try:
	configuration = json.loads(config_file_contents)
except ValueError:  # includes simplejson.decoder.JSONDecodeError
	raise Exception(f"Decoding configuration file '{config_file}' has failed")

# define logger
loglevel = 'info'
if 'log' in configuration:
	if 'level' in configuration['log']:
		loglevel = configuration['log']['level'].upper()

log_file = os.path.join(current_folder,"dryly_watcher.log")
formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(name)s %(levelname)s	%(message)s','%Y-%m-%d %H:%M:%S')
log_handler = logging.handlers.RotatingFileHandler(log_file,maxBytes=20000000,backupCount=2)
log_handler.setFormatter(formatter)
#log_handler = logging.StreamHandler(sys.stdout)
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(loglevel)

# define variables from configuration
if "access_token" in configuration['authentication']:
	logger.info("Starting up with known access_token")
	access_token = configuration['authentication']['access_token']
else:
	#dryly_login_url = base_url + '/auth/loginbear'
	dryly_login_url = dryly_base_url + 'auth/login?email=' + configuration['authentication']['email'] + '&password=' + configuration['authentication']['password']
	try:
		response = requests.post(dryly_login_url)
		logger.info(f"Status Code of '{dryly_login_url}' is '{response.status_code}'")
	except requests.exceptions.RequestException as e:
		logger.error('%s', e)
		exit()

	authentication_object = response.json()
	if authentication_object['status'] != "success":
		logger.error(f"Authentication failed with status '{authentication_object['status']}'")
		exit()

	access_token = authentication_object['access_token']
	configuration['authentication']['access_token'] = access_token
	configuration_object = json.dumps(configuration)
	with open(config_file, "w") as outfile:
		outfile.write(configuration_object)

dryly_notification_url = dryly_base_url + 'v1/notifications'
home_assistant_url = configuration['home_assistant']['url'].strip('/') + ":" + str(configuration['home_assistant']['port']) + '/api/states/input_boolean.' + configuration['home_assistant']['input_boolean']
logger.info(f"Input boolean that will be updates '{home_assistant_url}'")
headers = {
	'Authorization': 'Bearer ' + configuration['home_assistant']['access_token'],
	'content-type': 'application/json'
}
payload = {"state":"on"}

wait = configuration['configuration']['wait']
if wait < 5:
	logger.info(f"The wait time '{wait}' is too low. Setting it to 5 seconds")
	wait = 5

while True:
	if in_between(datetime.datetime.now().time(), datetime.time(20), datetime.time(8)):
		logger.debug(f"It is night")
		try:
			response = requests.get(dryly_notification_url,headers={'Authorization': f"Bearer {access_token}"})
			logger.info(f"Status Code of '{dryly_notification_url}' is '{response.status_code}'")
		except requests.exceptions.RequestException as e:
			logger.error('%s', e)
			exit()
		notification_result = response.json()

		notification_result.sort(key=lambda x: x['id'], reverse=True)
		if len(notification_result) > 0 and configuration['notification']['last'] != notification_result[0]['id']:
			try:
				r = requests.post(home_assistant_url, json=payload, headers=headers, timeout=10)
				logger.info(f"Home assistant Status Code '{r.status_code}'")
			except requests.exceptions.RequestException as e:  # This is the correct syntax
				logger.error('%s', e)

			logger.info(f"New notification with id '{notification_result[0]['id']}', title '{notification_result[0]['title']}', message '{notification_result[0]['message']}', read status '{notification_result[0]['read_status']}' and created_at '{notification_result[0]['created_at']}'")
			configuration['notification']['last'] = notification_result[0]['id']
			configuration_object = json.dumps(configuration)
			with open(config_file, "w") as outfile:
				outfile.write(configuration_object)
	else:
		logger.debug(f"It is day, no action")
	time.sleep(wait)
