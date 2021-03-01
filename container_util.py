_STREAM_WRITING_MODES = ("r+", "w", "w+", "a", "a+")


def dict_to_lines(a_dict):
	key_val_lines = list()

	for key, value in a_dict.items():
		key_val_lines.append(str(key) + ": " + str(value))

	return key_val_lines


def _container_to_lines_fnc(a_container):
	if isinstance(a_container, dict):
		return dict_to_lines
	elif isinstance(a_container, (list, tuple)):
		return list_or_tuple_to_lines
	else:
		raise TypeError("The argument must be of type dict, list or tuple.")


def list_or_tuple_to_lines(a_tuplist):
	index_item_lines = list()
	for i in range(len(a_tuplist)):
		line = "[" + str(i) + "]: " + str(a_tuplist[i])
		index_item_lines.append(line)

	return index_item_lines


def print_container(a_container, title=None):
	container_to_lines_fnc = _container_to_lines_fnc(a_container)

	if title is not None:
		print(title)

	lines = container_to_lines_fnc(a_container)
	for line in lines:
		print(line)


def write_dict_in_stream(a_dict, w_stream, before_line=None, after_line=None):
	assert(w_stream.mode in _STREAM_WRITING_MODES)

	key_val_lines = dict_to_lines(a_dict)
	for line in key_val_lines:
		if before_line is not None:
			line = before_line + line

		if after_line is not None:
			line += after_line

		w_stream.write(line)
