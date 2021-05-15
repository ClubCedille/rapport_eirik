"""
This module allows to make simplified representations of a PDF file's fields.
If it is executed in command line, it writes them in a .txt file.

Args:
	1: path to a PDF file
	2: (optional) path to the output .txt file
"""


from pathlib import Path
from PyPDF2 import PdfFileReader
from sys import argv, exit


_INPUT_EXTENSION = ".pdf"
_INPUT_EXTENSION_IN_LIST = [_INPUT_EXTENSION]
_OUTPUT_EXTENSION = ".txt"
_OUTPUT_EXTENSION_IN_LIST = [_OUTPUT_EXTENSION]


class PdfField:
	"""
	This class is a simplified representation of a PDF file field. It contains
	the field's name, type and value. The string representation matches the
	format "<name> (<type>): <value>".
	"""

	def __init__(self, name, type, value):
		"""
		The constructor needs the field's name, type and value. name and type
		can be instances of str or one of its subclasses. value can be an
		instance of any class.

		Args:
			name (str): the field's name
			type (str): the field's type
			value: the field's value
		"""
		self.name = name
		self.type = type
		self.value = value

	def __str__(self):
		return self.name + " (" + self.type + "): " + str(self.value)


def get_pdf_field_list(pdf_reader):
	"""
	Makes representations of a PDF file's fields.

	Args:
		pdf_reader (PyPDF2.PdfFileReader): a reader that contains a PDF file's
			representation

	Returns:
		list: contains PdfField instances that represent the fields from the
			file read by pdf_reader
		None: if the file does not have fields
	"""
	pdf_fields = pdf_reader.getFields()
	if pdf_fields is None:
		return None

	field_list = list()
	for mapping_name, field in pdf_fields.items():
		field_list.append(PdfField(mapping_name, field.fieldType, field.value))

	return field_list


def _make_default_output_file_name(input_path):
	return _make_default_output_file_stem(input_path) + _OUTPUT_EXTENSION


def _make_default_output_file_stem(input_path):
	return input_path.stem + "_field_values"


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

	# Output path checks
	try:
		output_path = Path(argv[2])

		if output_path.is_dir():
			output_path = output_path/_make_default_output_file_name(input_path)

		elif output_path.suffixes != _OUTPUT_EXTENSION_IN_LIST:
			output_path = output_path.with_suffix(_OUTPUT_EXTENSION)

	except IndexError:
		output_path = input_path.with_name(
			_make_default_output_file_name(input_path))

	# Real work
	reader = PdfFileReader(input_path.open(mode="rb"))
	field_list = get_pdf_field_list(reader)

	if field_list is None:
		print(str(input_path) + " does not contain fields.")
		exit()

	field_str = "\n".join(map(str, field_list))

	header = "Fields in file " + str(input_path) + "\n\n"
	output_path.write_text(header + field_str)
