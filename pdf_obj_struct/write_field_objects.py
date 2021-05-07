from argparse import ArgumentParser
from pathlib import Path
from pdf_obj_struct import write_pdf_obj_struct
from PyPDF2 import PdfFileReader
from sys import argv


parser = ArgumentParser(description=
	"This script explores recursively the object structure in a PDF file's\
	fields and records it in a .txt file.")

parser.add_argument("-f", "--file", type=Path, required=True,
	help="Path to the PDF file to explore")

parser.add_argument("-d", "--depth", type=int, default=0,
	help="Limit of the recursion depth that the algorithm can reach. If 0 or\
	less, no limit is set, and PyPDF2's indirect objects will not be\
	resolved. Defaults to 0.")

parser.add_argument("-o", "--output", type=Path,
	help="Path to the .txt output file. If set to \"console\", the object\
	structure will be written in the console. If not specified, an output\
	path is generated automatically.")

args = parser.parse_args()


_INPUT_EXTENSION = ".pdf"
_INPUT_EXTENSION_IN_LIST = [_INPUT_EXTENSION]
_OUTPUT_EXTENSION = ".txt"
_OUTPUT_EXTENSION_IN_LIST = [_OUTPUT_EXTENSION]


def _make_default_output_file_name(input_path):
	return _make_default_output_file_stem(input_path) + _OUTPUT_EXTENSION


def _make_default_output_file_stem(input_path):
	return input_path.stem + "_field_objects"


def _write_field_objs_in_stream(pdf_path, field_dict, w_stream, depth_limit):
	w_stream.write("Objects in the fields of " + str(pdf_path) + "\n")

	for mapping_name, field in field_dict.items():
		w_stream.write("\n" + mapping_name + "\n")
		write_pdf_obj_struct(field, w_stream,
			True, depth_limit>0, depth_limit)


if __name__ == "__main__":

	# Input path checks
	input_path = args.file

	if not input_path.exists():
		print("ERROR! " + str(input_path) + " does not exist.")
		exit()

	elif input_path.suffixes != _INPUT_EXTENSION_IN_LIST:
		# False if not a file
		print("ERROR! The first argument must be the path to a "
			+ _INPUT_EXTENSION + " file.")
		exit()

	# Recursion depth limit
	depth_limit = args.depth

	# Output path checks
	output_path = args.output

	if output_path is None:
		output_path = input_path.with_name(
			_make_default_output_file_name(input_path))

	elif str(output_path).lower() == "console":
			output_path = None

	elif output_path.is_dir():
		output_path = output_path/_make_default_output_file_name(input_path)

	elif output_path.suffixes != _OUTPUT_EXTENSION_IN_LIST:
		output_path = output_path.with_suffix(_OUTPUT_EXTENSION)

	# Real work
	reader = PdfFileReader(input_path.open(mode="rb"), strict=False)
	fields = reader.getFields()

	if output_path is None:
		from sys import stdout
		_write_field_objs_in_console(input_path, fields, stdout, depth_limit)

	else:
		with output_path.open(mode="w", encoding="utf8") as output_stream:
			_write_field_objs_in_stream(input_path, fields,
				output_stream, depth_limit)
