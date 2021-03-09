"""
Given a YAML file, this module allows to extract the name-value pairs that
define the content of a PDF file's fields. If this module is executed with the
path to a YAML file as its argument, it will print those pairs in the console.
In the YAML file, the fields' name and value must be stated as follows.
field1: value1
field2: value2
...
"""


from pathlib import Path
from sys import argv
from yaml import FullLoader, load


def filter_values_from_dict(a_dict, unwanted_vals):
	"""
	Creates a dictionary containing the items from a_dict minus those whose
	value is in unwanted_vals. a_dict is not modified.

	Args:
		a_dict (dict): any dictionary
		unwanted_vals: a list, set or tuple containing the values to filter

	Returns:
		dict: a dictionary containing the items of a_dict except the unwanted
		values
	"""
	wanted_items = dict()

	for key, value in a_dict.items():
		if value not in unwanted_vals:
			wanted_items[key] = value

	return wanted_items


def parse_field_values(field_setting_path, allow_nones=False):
	"""
	Parses a YAML file that defines field values. The association of the
	fields' name and value is stored in a dictionary returned by the function.

	Args:
		field_setting_path (pathlib.Path): the path to the YAML file
		allow_nones (bool): if False, the returned dictionary does not contain
			None values. Defaults to False.

	Returns:
		dict: a dictionary matching the fields' name with their value
	"""
	field_values = None
	with field_setting_path.open(encoding="utf8") as field_setting_stream:
		field_values = load(field_setting_stream, FullLoader)

		if not allow_nones:
			field_values = filter_values_from_dict(field_values, (None,))

	return field_values


def print_dictionary(a_dict):
	"""
	Prints a dictionary's items in the console in the following format.
	Key: value

	Args:
		a_dict (dict): any dictionary
	"""
	for key, value in a_dict.items():
		print(str(key) + ": " + str(value))


if __name__ == "__main__":
	try:
		field_setting_path = Path(argv[1])
	except IndexError:
		print("The path to a field setting file must be provided as an argument.")
		exit()

	field_values = parse_field_values(field_setting_path)
	print_dictionary(field_values)
