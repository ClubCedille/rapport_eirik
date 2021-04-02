"""
Explores recursively the object structure in a PDF file's pages and records
their structure in a .txt file.

Args:
	1: (str) the path to the PDF file to explore
	2: (int, optional) the limit to the recursion depth that the algorithm
		can reach. If 0 or less, no limit is set, and PyPDF2's indirect
		objects will not be resolved. Defaults to 0.
	3: (str, optional) the path to the .txt output file. If set to "console",
		the object structure will be written in the console.
"""


from pathlib import Path
from pdf_obj_struct import write_pdf_obj_struct
from PyPDF2 import PdfFileReader
from sys import argv


_INPUT_EXTENSION = ".pdf"
_INPUT_EXTENSION_IN_LIST = [_INPUT_EXTENSION]
_OUTPUT_EXTENSION = ".txt"
_OUTPUT_EXTENSION_IN_LIST = [_OUTPUT_EXTENSION]


def _make_default_output_file_name(input_path):
	return _make_default_output_file_stem(input_path) + _OUTPUT_EXTENSION


def _make_default_output_file_stem(input_path):
	return input_path.stem + "_page_objects"


def _write_page_objs_in_console(pdf_path, pages, w_stream, depth_limit):
	w_stream.write("Objects in the pages of " + str(pdf_path) + "\n")

	for i in range(len(pages)):
		page = pages[i]
		w_stream.write("\n\nPAGE " + str(i) + "\n")
		write_pdf_obj_struct(page, w_stream, True, depth_limit>0, depth_limit)


if __name__ == "__main__":

	# Input path checks
	try:
		input_path = Path(argv[1])
	except IndexError:
		print("ERROR! The path to a " + _INPUT_EXTENSION
			+ " file must be provided as the first argument.")
		exit()

	if not input_path.exists():
		print("ERROR! " + str(input_path) + " does not exist.")
		exit()

	elif input_path.suffixes != _INPUT_EXTENSION_IN_LIST:
		# False if not a file
		print("ERROR! The first argument must be the path to a "
			+ _INPUT_EXTENSION + " file.")
		exit()

	# Recursion depth limit check
	try:
		depth_limit = int(argv[2])

	except IndexError:
		depth_limit = 0

	except ValueError as ve:
		print("Argument 2: " + str(ve))
		exit()

	# Output path checks
	try:
		output_path = argv[3]

		if output_path.lower() == "console":
			output_path = None

		else:
			output_path = Path(output_path)

			if output_path.is_dir():
				output_path =\
					output_path/_make_default_output_file_name(input_path)

			elif output_path.suffixes != _OUTPUT_EXTENSION_IN_LIST:
				output_path = output_path.with_suffix(_OUTPUT_EXTENSION)

	except IndexError:
		output_path = input_path.with_name(
			_make_default_output_file_name(input_path))

	# Real work
	reader = PdfFileReader(input_path.open(mode="rb"))
	pages = reader.pages

	if output_path is None:
		from sys import stdout
		_write_page_objs_in_console(input_path, pages, stdout, depth_limit)

	else:
		with output_path.open(mode="w", encoding="utf8") as output_stream:
			_write_page_objs_in_console(input_path, pages,
				output_stream, depth_limit)
