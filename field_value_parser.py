"""
Given a YAML file, this module allows to extract the name-value pairs that
define the content of a PDF file's fields. If this module is executed with the
path to a YAML file as its argument, it will print those pairs in the console.
In the YAML file, the fields' name and value must be stated as follows.

field1: value1

field2: value2

...

Args:
	1: the path to a YAML file
	2: a string matching a Boolean value. If True, the type of the fields'
		value will be printed. Defaults to False.
		False: "0", "f", "false", "n" or "no"
		True: "1", "t", "true", "y" or "yes"
"""


from pathlib import Path
from sys import argv
from yaml import FullLoader, load


_CHECKBOX_YES = "/Oui"
_CHOICE1 = "/Choix1"
_CHOICE2 = "/Choix2"
_KEY_CHECKED = "Cochée"


def _dict_key_val_str(key, value):
	"""
	Creates a string representing a dictionary item. The string fits this
	format: "<key>: <value>".

	Args:
		key: the key from the dictionary item
		value: the value from the dictionary item

	Returns:
		str: a string representing the dictionary item
	"""
	return str(key) + ": " + str(value)


def _dict_key_val_type_str(key, value):
	"""
	Creates a string representing a dictionary item. The string fits this
	format: "<key>: <value> <type(value)>".

	Args:
		key: the key from the dictionary item
		value: the value from the dictionary item

	Returns:
		str: a string representing the dictionary item
	"""
	return _dict_key_val_str(key, value) + " " + str(type(value))


def _error_for_unexpected_value(key, value):
	raise ValueError("Unexpected value for " + str(key) + ": " + str(value))


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


def get_yaml_content(field_setting_path, allow_nones=False):
	"""
	Reads a YAML file and returns its content in in a dictionary.

	Args:
		field_setting_path (pathlib.Path): the path to the YAML file
		allow_nones (bool): if False, the returned content does not contain
			None values. Defaults to False.

	Returns:
		dict: the YAML file's content

	Raises:
		ValueError: if the extension of field_setting_path is not "yaml" or
		"yml"
	"""
	if field_setting_path.suffixes not in ([".yaml"], [".yml"]):
		raise ValueError("The file extension must be \".yaml\" or \".yml\".")

	yaml_content = None
	with field_setting_path.open(encoding="utf8") as field_setting_stream:
		yaml_content = load(field_setting_stream, FullLoader)

		if not allow_nones:
			yaml_content = filter_values_from_dict(yaml_content, (None,))

	return yaml_content


def parse_yaml_content(yaml_content):
	field_values = dict()

	for key, value in yaml_content.items():
		if key == "RaisonVoyage":
			field_values.update(_parse_travel_reasons(value))
		elif key == "Dépenses":
			field_values.update(_parse_expanse_list(value))
		elif key == "Codes comptables":
			field_values.update(_parse_codes_comptables(value))
		elif key == "RaisonDépenses":
			if value.lower() == "voyage":
				field_values["Group1"] = _CHOICE1
			elif value.lower() == "autre":
				field_values["Group1"] = _CHOICE2
			else:
				_error_for_unexpected_value(key, value)
		elif key == "Étudiant(e) ou employé(e)":
			if value.lower() == "employé(e)":
				field_values["Group2"] = _CHOICE1
			elif value.lower() == "étudiant(e)":
				field_values["Group2"] = _CHOICE2
			else:
				_error_for_unexpected_value(key, value)
		elif key == "Chèque ou dépôt":
			if value.lower() == "dépôt":
				field_values["Group4"] = "/D#E9p#F4t"
			elif value.lower() == "chèque":
				field_values["Group4"] = "/Ch#E8que"
			else:
				_error_for_unexpected_value(key, value)
		elif key == "Distance":
			field_values["KM"] = value
		else:
			field_values[key] = value

	return field_values


def _parse_codes_comptables(codes_comptables):
	fields = dict()

	for i in range(len(codes_comptables)):
		cc = codes_comptables[i]
		ubr = cc["UBR"]
		account = cc["Compte"]
		df = cc["DemFin"]
		cbs = cc["CBS"]
		amount = cc["Montant"]

		fields["UBR" + str(i+1)] = ubr
		fields["CC" + str(i+1)] = account
		fields["DF" + str(i+1)] = df
		fields["CBS" + str(i+1)] = cbs
		fields["ccMontant$" + str(i+1)] = amount

	return fields


def _parse_expanse_list(expanse_list):
	fields = dict()

	for i in range(len(expanse_list)):
		expanse = expanse_list[i]
		description = expanse["Description"]
		amount = expanse["Montant"]

		fields["Détails" + str(i+1)] = description
		fields["Montant$" + str(i+1)] = amount

	return fields


def _parse_travel_reasons(travel_reason_dict):
	fields = dict()

	presentation = travel_reason_dict["Présentation"]
	if presentation[_KEY_CHECKED]:
		fields["Boite1"] = _CHECKBOX_YES
	fields["Présentation"] = presentation["Sujet"]

	conference = travel_reason_dict["Conférence"]
	if conference[_KEY_CHECKED]:
		fields["Boite2"] = _CHECKBOX_YES
	fields["Conférence"] = conference["Nom"]

	if travel_reason_dict["Sabbatique"]:
		fields["Boite3"] = _CHECKBOX_YES

	others = travel_reason_dict["Autres"]
	if others[_KEY_CHECKED]:
		fields["Boite4"] = _CHECKBOX_YES
	fields["Autres"] = others["Précision"]

	return fields


def print_dictionary(a_dict, print_val_type):
	"""
	Prints a dictionary's items in the console in the following format:
	"<key>: <value>".

	Args:
		a_dict (dict): any dictionary
		print_val_type (bool): if True, the type of each value is also printed.
	"""
	item_to_str_fnc = _dict_key_val_type_str if print_val_type\
		else _dict_key_val_str

	for key, value in a_dict.items():
		print(item_to_str_fnc(key, value))


def str_to_bool(bool_str):
	"""
	Converts a string to a Boolean value.

	False: "0", "f", "false", "n" or "no"

	True: "1", "t", "true", "y" or "yes"

	Args:
		bool_str (str): a string corresponding to a Boolean value

	Returns:
		bool: the Boolean value matching bool_str

	Raises:
		ValueError: if bool_str does not match a boolean value
	"""
	if bool_str.lower() in ("0", "f", "false", "n", "no"):
		return False
	if bool_str.lower() in ("1", "t", "true", "y", "yes"):
		return True
	raise ValueError("\"" + str(bool_str)
		+ "\" does not match a boolean value.")


if __name__ == "__main__":
	try:
		field_setting_path = Path(argv[1])
	except IndexError:
		print("The path to a field setting file must be provided as an argument.")
		exit()

	try:
		print_val_type = str_to_bool(argv[2])
	except IndexError:
		print_val_type = False
	except ValueError as ve:
		print(ve)
		exit()

	yaml_content = get_yaml_content(field_setting_path)
	field_values = parse_yaml_content(yaml_content)
	print_dictionary(field_values, print_val_type)
