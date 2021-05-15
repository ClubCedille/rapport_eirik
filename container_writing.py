_STREAM_WRITING_MODES = ("a", "a+", "r+", "w", "w+")


def _container_to_lines_fnc(a_container):
	if isinstance(a_container, dict):
		return dict_to_lines

	elif isinstance(a_container, (list, tuple)):
		return list_or_tuple_to_lines

	elif isinstance(a_container, set):
		return set_to_lines

	else:
		raise TypeError(
			"The argument must be of type dict, list, set or tuple.")


def dict_to_lines(a_dict):
	key_val_lines = list()

	for key, value in a_dict.items():
		key_val_lines.append(str(key) + ": " + str(value))

	return key_val_lines


def list_or_tuple_to_lines(a_tuplist):
	index_item_lines = list()

	for i, item in enumerate(a_tuplist):
		line = "[" + str(i) + "]: " + str(item)
		index_item_lines.append(line)

	return index_item_lines


def print_container(a_container, title=None):
	container_to_lines_fnc = _container_to_lines_fnc(a_container)

	if title is not None:
		print(title)

	lines = container_to_lines_fnc(a_container)
	for line in lines:
		print(line)


def set_to_lines(a_set):
	item_lines = list()

	for item in a_set:
		item_lines.append(str(item))

	return item_lines


def write_container_in_stream(a_container, w_stream,
		before_item=None, after_item=None):
	if w_stream.mode not in _STREAM_WRITING_MODES:
		raise ValueError("The stream's mode must be "
			+ "\"a\", \"a+\", \"r+\", \"w\" or \"w+\".")

	container_to_lines_fnc = _container_to_lines_fnc(a_container)

	lines = container_to_lines_fnc(a_container)
	for line in lines:
		if before_item is not None:
			line = before_item + line

		if after_item is not None:
			line += after_item

		w_stream.write(line)
