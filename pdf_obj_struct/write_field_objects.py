"""
Explores recursively the objects in a PDF file's fields and records their
structure in a .txt file.

Args:
	1: (str) the path to the PDF file to explore
	2: (int, optional) the limit to the recursion depth that the algorithm
		can reach. If 0 or less, no limit is set, and PyPDF2's indirect
		objects will not be resolved. Defaults to 0.
	3: (str, optional) the path to the .txt output file
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
	return input_path.stem + "_field_objects"


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

	if input_path.suffixes != _INPUT_EXTENSION_IN_LIST: # False if not a file
		print("ERROR! The first argument must be the path to a "
			+ _INPUT_EXTENSION + " file.")
		exit()

	# Recursion depth limit check
	try:
		depth_limit = int(argv[2])

	except IndexError:
		depth_limit = 0

	# Output path checks
	try:
		output_path = Path(argv[3])

		if output_path.is_dir():
			output_path = output_path/_make_default_output_file_name(input_path)

		elif output_path.suffixes != _OUTPUT_EXTENSION_IN_LIST:
			output_path = output_path.with_suffix(_OUTPUT_EXTENSION)

	except IndexError:
		output_path = input_path.with_name(
			_make_default_output_file_name(input_path))

	# Real work
	reader = PdfFileReader(input_path.open(mode="rb"))

	with output_path.open(mode="w") as output_stream:
		output_stream.write("Objects in the fields of "
			+ str(input_path) + "\n")

		for mapping_name, field in reader.getFields().items():
			output_stream.write("\n" + mapping_name + "\n")
			write_pdf_obj_struct(field, output_stream,
				True, depth_limit>0, depth_limit)
