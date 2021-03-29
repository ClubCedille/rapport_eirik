"""
This module allows to write a PDF object structure in a file stream. An object
structure consists of containers (dictionaries, lists, sets and tuples)
embedded in one another and other objects.
"""


from PyPDF2.generic import PdfObject


_DLST = (dict, list, set, tuple)


_STREAM_WRITING_MODES = ("a", "a+", "r+", "w", "w+")


def _make_tabs(n):
	return "\t" * n


def _obj_and_type_to_str(obj):
	return str(obj) + " " + str(type(obj))


def obj_is_a_dlst(obj):
	"""
	Indicates whether the given object is a dictionary, a list, a set or a
	tuple.

	Args:
		obj: any object

	Returns:
		bool: True if the object's type is dict, list, set or tuple, False
			otherwise.
	"""
	return isinstance(obj, _DLST)


def write_pdf_obj_struct(struct, w_stream, write_types=False):
	"""
	Writes a PDF object structure in a file stream. Lines of same indentation
	represent objects in the same container. The stream's mode must be "a",
	"a+", "r+", "w" or "w+". It the object struct is not a dictionary, a list,
	a set or a tuple, this method will only write one line representing that
	object.

	Args:
		struct: any object. Can be a container or not.
		w_stream (TextIOWrapper): the file stream that will contain the
			structure's representation
		write_types (bool): If True, this method will write the contained
			objects' type in the stream. Defaults to False.

	Raises:
		ValueError: if the stream's mode in incorrect
	"""
	if w_stream.mode not in _STREAM_WRITING_MODES:
		raise ValueError("The stream's mode must be "
			+ "\"a\", \"a+\", \"r+\", \"w\" or \"w+\".")

	obj_str_fnc = _obj_and_type_to_str if write_types else str

	if obj_is_a_dlst(struct):
		w_stream.write(str(type(struct)) + "\n")
		indent = 1

	else:
		indent = 0

	_write_pdf_obj_struct_rec(struct, w_stream, indent, obj_str_fnc)


def _write_pdf_obj_struct_rec(obj_to_write, w_stream, indent, obj_str_fnc):
	tabs = _make_tabs(indent)
	indent += 1

	if isinstance(obj_to_write, PdfObject):
		obj_to_write = obj_to_write.getObject()

	if isinstance(obj_to_write, (list, tuple)):
		length = len(obj_to_write)

		for i in range(length):
			item = obj_to_write[i]
			line = tabs + "[" + str(i) + "]: "

			if obj_is_a_dlst(item):
				line += str(type(item))
				w_stream.write(line + "\n")
				_write_pdf_obj_struct_rec(item, w_stream, indent, obj_str_fnc)

			else:
				line += obj_str_fnc(item)
				w_stream.write(line + "\n")

	elif isinstance(obj_to_write, dict):
		for key, value in obj_to_write.items():
			line = tabs + str(key) + ": "

			if obj_is_a_dlst(value):
				line += str(type(value))
				w_stream.write(line + "\n")
				_write_pdf_obj_struct_rec(value, w_stream, indent, obj_str_fnc)

			else:
				line += obj_str_fnc(value)
				w_stream.write(line + "\n")

	elif isinstance(obj_to_write, set):
		for item in obj_to_write:
			line = tabs

			if obj_is_a_dlst(item):
				line += str(type(item))
				w_stream.write(line + "\n")
				_write_pdf_obj_struct_rec(item, w_stream, indent, obj_str_fnc)

			else:
				line += obj_str_fnc(item)
				w_stream.write(line + "\n")

	else:
		line = tabs + obj_str_fnc(obj_to_write)
		w_stream.write(line + "\n")
