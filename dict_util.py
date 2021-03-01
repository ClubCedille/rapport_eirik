_STREAM_WRITING_MODES = ("r+", "w", "w+", "a", "a+")


def dict_to_lines(a_dict):
	key_val_lines = list()

	for key, value in a_dict.items():
		key_val_lines.append(str(key) + ": " + str(value))

	return key_val_lines


def print_dict(a_dict, title=None):
	if title is not None:
		print(title)

	key_val_lines = dict_to_lines(a_dict)
	for line in key_val_lines:
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
