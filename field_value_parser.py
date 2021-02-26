from pathlib import Path
from sys import argv
from yaml import FullLoader, load


def filter_nones_from_dict(a_dict):
	no_nones = dict()

	for key, value in a_dict.items():
		if value is not None:
			no_nones[key] = value

	return no_nones


def parse_field_values(field_config_path):
	if type(field_config_path) is not Path:
		field_config_path = Path(field_config_path)

	with field_config_path.open(encoding="utf8") as config_stream:
		return load(config_stream, FullLoader)


def print_dictionary(a_dict):
	for key, value in a_dict.items():
		print(str(key) + ": " + str(value))


if __name__ == "__main__":
	try:
		fild_file_path = argv[1]
	except IndexError:
		print("The path to a field file must be provided as an argument.")
		exit()

	field_values = parse_field_values(fild_file_path)
	field_values = filter_nones_from_dict(field_values)
	print_dictionary(field_values)
