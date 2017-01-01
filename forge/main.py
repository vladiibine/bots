import argparse
import base64

import requests


def get_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'--credentials-file', '-c',
		help='Path to a file containing base64.b64encode("Username:password")')
	parser.add_argument(
		'--login-url', '-l',
		help='Login url of the service which needs to authenticate me',
		default='https://armorgames.com/login')
	parser.add_argument(
		'--game-url', '-g',
		help='URL of the game to be played. Would require to be authenticated by the login service')

	return parser


def extract_credentials_from_file(credentials_file):
	"""
	:param credentials_file:
	:return: the username string and the hex encoded password
	"""
	try:
		with open(credentials_file, 'rb') as thefile:
			content = thefile.read()
			credentials_string = base64.b64decode(content)
			user, pwd = credentials_string.split(b':', 1)
			return user, pwd.hex()
	except (TypeError, IOError) as err:
		raise Exception(
			"Something's wrong with the credentials file: {}:"
			"\n{}".format(credentials_file, str(err)))


def cli_main():
	parser = get_parser()
	args = parser.parse_args()

	user, encoded_password = extract_credentials_from_file(args.credentials_file)

	session = requests.Session()
	response = session.post(
		args.login_url, data={'username': user, 'password': bytes.fromhex(encoded_password)})
	pass


if __name__ == '__main__':
	cli_main()
