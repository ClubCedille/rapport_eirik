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


def write_container_in_stream(a_container, w_stream,
		after_item=None, before_item=None):
	assert(w_stream.mode in _STREAM_WRITING_MODES)

	container_to_lines_fnc = _container_to_lines_fnc(a_container)

	lines = container_to_lines_fnc(a_container)
	for line in lines:
		if before_item is not None:
			line = before_item + line

		if after_item is not None:
			line += after_item

		w_stream.write(line)
