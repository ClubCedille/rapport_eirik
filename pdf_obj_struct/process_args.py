from argparse import ArgumentParser
from pathlib import Path
from pdf_obj_struct import write_pdf_obj_struct
from PyPDF2 import PdfFileReader


_INPUT_EXTENSION = ".pdf"
_INPUT_EXTENSION_IN_LIST = [_INPUT_EXTENSION]
_OUTPUT_EXTENSION = ".txt"
_OUTPUT_EXTENSION_IN_LIST = [_OUTPUT_EXTENSION]


def _make_default_output_file_name(input_path, after_stem):
	return _make_default_output_file_stem(input_path, after_stem)\
		+ _OUTPUT_EXTENSION


def _make_default_output_file_stem(input_path, after_stem):
	return input_path.stem + after_stem


def make_parser(struct_type):
	"""
	Creates an argparse.ArgumentParser for scripts write_field_objects.py and
	write_page_objects.py.

	Args:
		struct_type (int): 0 for fields, 1 for pages

	Returns:
		argparse.ArgumentParser: a parser designed specifically for these
			scripts

	Raises:
		ValueError: if argument struct_type is incorrect
	"""
	if struct_type == 0:
		struct_word = "fields"

	elif struct_type == 1:
		struct_word = "pages"

	else:
		raise ValueError(str(struct_type) + " is not a structure type.")

	parser = ArgumentParser(description=
		"This script explores recursively the object structure in a PDF\
		file's " + struct_word + " and records it in a .txt file.")

	parser.add_argument("-f", "--file", type=Path, required=True,
		help="Path to the PDF file to explore")

	parser.add_argument("-d", "--depth", type=int, default=0,
		help="Limit of the recursion depth that the algorithm can reach. If 0\
		or less, no limit is set, and PyPDF2's indirect objects will not be\
		resolved. Defaults to 0.")

	parser.add_argument("-o", "--output", type=Path,
		help="Path to the .txt output file. If set to \"console\", the object\
		structure will be written in the console. If not specified, an output\
		path is generated automatically.")

	return parser


def process_arguments(args, struct_type):
	"""
	Performs various checks on the arguments from the parser returned by
	make_parser and changes their value if necessary. The arguments are
	the path to the file to explore, the recusion depth limit and the path to
	the output file in this precise order. If the latter is None, the object
	structure must be written in the console.

	Args:
		args (argparse.Namespace): the object returned when parse_args is
			called on the parser instantiated by make_parser
		struct_type (int): 0 for fields, 1 for pages

	Returns:
		tuple: It contains the path to the file to explore [0], the recusion
			depth limit [1] and the path to the output file [2].

	Raises:
		ValueError: if the path to the file to explore or struct_type is
			incorrect
	"""
	if struct_type == 0: # Fields
		input_path_suffix = "_field_objects"

	elif struct_type == 1: # Pages
		input_path_suffix = "_page_objects"

	else:
		raise ValueError(str(struct_type) + " is not a structure type.")

	# Input path checks
	input_path = args.file

	if not input_path.exists():
		raise ValueError("ERROR! " + str(input_path) + " does not exist.")

	elif input_path.suffixes != _INPUT_EXTENSION_IN_LIST:
		# False if not a file
		raise ValueError("ERROR! The first argument must be the path to a "
			+ _INPUT_EXTENSION + " file.")

	# Recursion depth limit
	depth_limit = args.depth
	
	# Output path checks
	output_path = args.output

	if output_path is None:
		output_path = input_path.with_name(
			_make_default_output_file_name(input_path, input_path_suffix))

	elif str(output_path).lower() == "console":
			output_path = None

	elif output_path.is_dir():
		output_path = output_path/\
			_make_default_output_file_name(input_path, input_path_suffix)

	elif output_path.suffixes != _OUTPUT_EXTENSION_IN_LIST:
		output_path = output_path.with_suffix(_OUTPUT_EXTENSION)

	return input_path, depth_limit, output_path
