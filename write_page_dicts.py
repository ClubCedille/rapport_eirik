from pathlib import Path
from PyPDF2 import PdfFileReader
from PyPDF2.generic import PdfObject
from sys import argv


def _make_tabs(n):
	return "\t" * n


def _obj_and_type_to_str(obj):
	return str(obj) + " " + str(type(obj))


def _write_page_objs_rec(w_stream, obj_to_write, indent=0):
	tabs = _make_tabs(indent)
	indent += 1

	if isinstance(obj_to_write, PdfObject):
		obj_to_write = obj_to_write.getObject()

	if isinstance(obj_to_write, (list, tuple)):
		length = len(obj_to_write)

		for i in range(length):
			item = obj_to_write[i]

			if isinstance(item, (dict, list, set, tuple)):
				_write_page_objs_rec(w_stream, item, indent)
			else:
				w_stream.write(tabs + "[" + str(i) + "]: " + _obj_and_type_to_str(item) + "\n")

	elif isinstance(obj_to_write, dict):
		for key, value in obj_to_write.items():
			line = tabs + str(key) + ":"

			if isinstance(value, dict):
				_write_page_objs_rec(w_stream, value, indent)
			else:
				line += _obj_and_type_to_str(value)

			w_stream.write(line + "\n")

	elif isinstance(obj_to_write, set):
		for item in obj_to_write:
			if isinstance(item, (dict, list, set, tuple)):
				_write_page_objs_rec(w_stream, item, indent)
			else:
				w_stream.write(tabs + _obj_and_type_to_str(item) + "\n")

	w_stream.write(tabs + str(obj_to_write) + "\n")


try:
	input_path = Path(argv[1])
except IndexError:
	print("The path to a PDF file must be provided as an argument.")
	exit()

try:
	output_path = Path(argv[2])
except IndexError:
	output_path = input_path.parents[0]/(input_path.stem + ".txt")

reader = PdfFileReader(input_path.open("rb"))
pages = reader.pages

with output_path.open("w") as output_stream:
	output_stream.write("Content of " + str(input_path) + "\n")

	for i in range(len(pages)):
		page = pages[i]
		output_stream.write("\nPage " + str(i) + "\n")
		_write_page_objs_rec(output_stream, page)
