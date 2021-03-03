from pathlib import Path
from sys import argv
from yaml import FullLoader, load


def filter_values_from_dict(a_dict, unwanted_vals):
	wanted_items = dict()

	for key, value in a_dict.items():
		if value not in unwanted_vals:
			wanted_items[key] = value

	return wanted_items


def parse_field_values(field_setting_path, allow_nones=False):
	if type(field_setting_path) is not Path:
		field_setting_path = Path(field_setting_path)

	field_values = None
	with field_setting_path.open(encoding="utf8") as field_setting_stream:
		field_values = load(field_setting_stream, FullLoader)

		if not allow_nones:
			field_values = filter_values_from_dict(field_values, (None,))

	return field_values


def print_dictionary(a_dict):
	for key, value in a_dict.items():
		print(str(key) + ": " + str(value))


if __name__ == "__main__":
	try:
		field_setting_path = argv[1]
	except IndexError:
		print("The path to a field setting file must be provided as an argument.")
		exit()

	field_values = parse_field_values(field_setting_path)
	print_dictionary(field_values)
