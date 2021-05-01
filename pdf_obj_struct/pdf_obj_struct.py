"""
This module allows to write a PDF object structure in a file stream. An object
structure consists of containers (dictionaries, lists, sets and tuples)
embedded in one another and other objects. This module also works on
structures that do not contain PDF objects.
"""


from PyPDF2.generic import BooleanObject, DictionaryObject, IndirectObject


_DLST = (dict, list, set, tuple)
_LT = (list, tuple)

_PAGE_KEYS = ("/Annots", "/Contents", "/CropBox", "/MediaBox",
	"/Parent", "/Resources", "/Rotate", "/Tabs", "/Type")

_STREAM_WRITING_MODES = ("a", "a+", "r+", "w", "w+")

_CLOSING_BRACKET_COLON_SPACE = "]: "
_COLON_SPACE = ": "
_NEW_LINE = "\n"
_OPENING_BRACKET = "["
_PAGE_REF = "\tReference to a page\n"
_SPACE = " "
_TAB = "\t"
_UNEXPLORED_OBJS = "\t[...]\n"


def _index_between_brackets(index):
	return _OPENING_BRACKET + str(index) + _CLOSING_BRACKET_COLON_SPACE


def _make_tabs(n):
	return _TAB * n


def _obj_and_type_to_str(obj):
	if isinstance(obj, BooleanObject):
		return str(obj.value) + _SPACE + str(type(obj))

	else:
		return str(obj) + _SPACE + str(type(obj))


def obj_is_a_dlst(obj):
	"""
	Indicates whether the given object is a dictionary, a list, a set or a
	tuple.

	Args:
		obj: any object

	Returns:
		bool: True if the object's type is dict, list, set or tuple, False
			otherwise
	"""
	return isinstance(obj, _DLST)


def _obj_is_a_page(obj):
	"""
	Indicates whether the given object is a dictionary that represents a page
	of a PDF file.

	Args:
		obj: any object

	Returns:
		bool: True if the object represents a PDF page, False otherwise.
	"""
	if isinstance(obj, DictionaryObject):
		return tuple(obj.keys()) == _PAGE_KEYS

	else:
		return False


def _rslv_pdf_ind_object(obj):
	if isinstance(obj, IndirectObject):
		return obj.getObject()

	else:
		return obj


def _return_arg(obj):
	return obj


def write_pdf_obj_struct(struct, w_stream, write_types=False,
		rslv_ind_objs=False, depth_limit=0):
	"""
	Writes a PDF object structure in a file stream. The indentation indicates
	which objects are contained in others. The stream's mode must be "a",
	"a+", "r+", "w" or "w+". It the object struct is not a dictionary, a list,
	a set or a tuple, this method will only write one line representing that
	object.

	Args:
		struct: any object. Can be a container or not.
		w_stream (TextIOWrapper): the file stream that will contain the
			structure's representation
		write_types (bool): If True, this method will write the contained
			objects' type in the stream. Defaults to False.
		rslv_ind_objs (bool): If True, the indirect objects found in the
			structure will be resolved. Defaults to False. WARNING! Setting
			this parameter to True can make the function exceed the maximum
			recursion depth.
		depth_limit (int): a limit to the recursion depth. If it is set to 0
			or less, no limit is enforced. Defaults to 0.

	Raises:
		RecursionError: if this function exceeds the maximum recursion depth
		ValueError: if the stream's mode in incorrect
	"""
	if w_stream.mode not in _STREAM_WRITING_MODES:
		raise ValueError("The stream's mode must be "
			+ "\"a\", \"a+\", \"r+\", \"w\" or \"w+\".")

	obj_str_fnc = _obj_and_type_to_str if write_types else str
	ind_obj_fnc = _rslv_pdf_ind_object if rslv_ind_objs else _return_arg

	if obj_is_a_dlst(struct):
		w_stream.write(str(type(struct)) + _NEW_LINE)
		rec_depth = 1

	else:
		rec_depth = 0

	_write_pdf_obj_struct_rec(struct, w_stream, rec_depth,
		depth_limit, obj_str_fnc, ind_obj_fnc)


def _write_pdf_obj_struct_rec(obj_to_write, w_stream, rec_depth,
		depth_limit, obj_str_fnc, ind_obj_fnc):
	tabs = _make_tabs(rec_depth)
	rec_depth += 1

	if isinstance(obj_to_write, _LT):
		length = len(obj_to_write)

		for i in range(length):
			item = ind_obj_fnc(obj_to_write[i])
			line = tabs + _index_between_brackets(i)

			if obj_is_a_dlst(item):
				line += str(type(item))
				w_stream.write(line + _NEW_LINE)

				if _obj_is_a_page(item):
					line = tabs + _PAGE_REF
					w_stream.write(line)

				elif depth_limit<=0 or rec_depth<=depth_limit:
					_write_pdf_obj_struct_rec(item, w_stream, rec_depth,
						depth_limit, obj_str_fnc, ind_obj_fnc)

				else:
					w_stream.write(tabs + _UNEXPLORED_OBJS)

			else:
				line += obj_str_fnc(item)
				w_stream.write(line + _NEW_LINE)

	elif isinstance(obj_to_write, dict):
		for key, value in obj_to_write.items():
			value = ind_obj_fnc(value)
			line = tabs + str(key) + _COLON_SPACE

			if obj_is_a_dlst(value):
				line += str(type(value))
				w_stream.write(line + _NEW_LINE)

				if _obj_is_a_page(value):
					line = tabs + _PAGE_REF
					w_stream.write(line)

				elif depth_limit<=0 or rec_depth<=depth_limit:
					_write_pdf_obj_struct_rec(value, w_stream, rec_depth,
						depth_limit, obj_str_fnc, ind_obj_fnc)

				else:
					w_stream.write(tabs + _UNEXPLORED_OBJS)

			else:
				line += obj_str_fnc(value)
				w_stream.write(line + _NEW_LINE)

	elif isinstance(obj_to_write, set):
		for item in obj_to_write:
			item = ind_obj_fnc(item)
			line = tabs

			if obj_is_a_dlst(item):
				line += str(type(item))
				w_stream.write(line + _NEW_LINE)

				if _obj_is_a_page(item):
					line = tabs + _PAGE_REF
					w_stream.write(line)

				elif depth_limit<=0 or rec_depth<=depth_limit:
					_write_pdf_obj_struct_rec(item, w_stream, rec_depth,
						depth_limit, obj_str_fnc, ind_obj_fnc)

				else:
					w_stream.write(tabs + _UNEXPLORED_OBJS)

			else:
				line += obj_str_fnc(item)
				w_stream.write(line + _NEW_LINE)

	else:
		line = tabs + obj_str_fnc(obj_to_write)
		w_stream.write(line + _NEW_LINE)
