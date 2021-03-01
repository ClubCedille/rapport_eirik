# Explores recursively the objects in a PDF file's pages and records their
# hierachy in a .txt file.
# argv[1]: path to the PDF file to explore
# argv[2]: (optional) path to the .txt output file


from pathlib import Path
from PyPDF2 import PdfFileReader
from PyPDF2.generic import PdfObject
from sys import argv


_DLST = (dict, list, set, tuple)

_INPUT_EXTENSION = ".pdf"

_INPUT_EXTENSION_LIST = [_INPUT_EXTENSION]

_OUTPUT_EXTENSION = ".txt"

_OUTPUT_EXTENSION_LIST = [_OUTPUT_EXTENSION]


def _make_default_output_file_name(input_path):
	return input_path.stem + "_object_hierarchy" + _OUTPUT_EXTENSION


def _make_tabs(n):
	return "\t" * n


def _obj_and_type_to_str(obj):
	return str(obj) + " " + str(type(obj))


def _obj_is_a_dlst(obj):
	return isinstance(obj, _DLST)


def _replace_extension(a_path, extension):
	return a_path.parents[0]/(a_path.stem + extension)


def _write_page_objects_rec(w_stream, obj_to_write, indent=0):
	tabs = _make_tabs(indent)
	indent += 1

	if isinstance(obj_to_write, PdfObject):
		obj_to_write = obj_to_write.getObject()

	if isinstance(obj_to_write, (list, tuple)):
		length = len(obj_to_write)

		for i in range(length):
			item = obj_to_write[i]

			if _obj_is_a_dlst(item):
				_write_page_objects_rec(w_stream, item, indent)
			else:
				line = tabs + "[" + str(i) + "]: "\
					+ _obj_and_type_to_str(item)
				w_stream.write(line + "\n")

	elif isinstance(obj_to_write, dict):
		for key, value in obj_to_write.items():
			line = tabs + str(key) + ":"

			if _obj_is_a_dlst(value):
				_write_page_objects_rec(w_stream, value, indent)
			else:
				line += " " + _obj_and_type_to_str(value)

			w_stream.write(line + "\n")

	elif isinstance(obj_to_write, set):
		for item in obj_to_write:
			if _obj_is_a_dlst(item):
				_write_page_objects_rec(w_stream, item, indent)
			else:
				line = tabs + _obj_and_type_to_str(item)
				w_stream.write(line + "\n")

	else:
		line = tabs + str(obj_to_write)
		w_stream.write(line + "\n")


try:
	input_path = Path(argv[1])
except IndexError:
	print("ERROR! The path to a " + _INPUT_EXTENSION
		+ " file must be provided as the first argument.")
	exit()

if not input_path.exists():
	print("ERROR! Path " + str(input_path) + " does not exist.")
	exit()
elif input_path.suffixes != _INPUT_EXTENSION_LIST:
	print("ERROR! The first argument must be the path to a "
		+ _INPUT_EXTENSION + " file.")
	exit()

try:
	output_path = Path(argv[2])
	if output_path.is_dir():
		output_path = output_path/_make_default_output_file_name(input_path)
	elif output_path.suffixes != _OUTPUT_EXTENSION_LIST:
		output_path = _replace_extension(output_path, _OUTPUT_EXTENSION)
except IndexError:
	output_path = input_path.parents[0]/_make_default_output_file_name(input_path)

reader = PdfFileReader(input_path.open("rb"))
pages = reader.pages

with output_path.open("w") as output_stream:
	output_stream.write("Object hierachy of " + str(input_path) + "\n")

	for i in range(len(pages)):
		page = pages[i]
		output_stream.write("\n\nPAGE " + str(i) + "\n")
		_write_page_objects_rec(output_stream, page)
