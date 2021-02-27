def dict_to_lines(a_dict):
	key_val_lines = list()

	for key, value in a_dict.items():
		print(str(key) + ": " + str(value))

	return key_val_lines


def print_dictionary(a_dict, title=None):
	if title:
		print(title)

	key_val_lines = dict_to_lines(a_dict)
	for line in key_val_lines:
		print(line)
