"""
This module allows to make simplified representations of a PDF file's fields.
If it is executed in command line, it writes them in a .txt file.

Args:
	1: path to a PDF file
	2: (optional) path to the output .txt file
"""


from jazal import\
	MissingPathArgWarner,\
	make_altered_name,\
	make_altered_path
from pathlib import Path
from PyPDF2 import PdfFileReader
from sys import argv, exit


DFLT_OUTPUT_TERMINATION = "_field_values"
ERROR_INTRO = "ERROR! "


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


if __name__ == "__main__":
	# Input path checks
	missing_input_warner = MissingPathArgWarner("Input file", (".pdf",))
	try:
		input_path = Path(argv[1])
		input_path_checker =\
			missing_input_warner.make_reactive_path_checker(input_path)
		input_path_checker.check_path_exists()
		input_path_checker.check_extension_correct()

	except IndexError:
		print(ERROR_INTRO + missing_input_warner.make_missing_arg_msg())
		exit()

	except Exception as e:
		print(ERROR_INTRO + str(e))
		exit()

	# Output path checks
	missing_output_warner = MissingPathArgWarner("Output file", (".txt",))
	try:
		output_path = Path(argv[2])

		output_path_checker =\
			missing_output_warner.make_reactive_path_checker(output_path)

		if output_path_checker.path_is_dir():
			output_path = output_path/make_altered_name(
				input_path, after_stem=DFLT_OUTPUT_TERMINATION,
				extension=output_path_checker.extension_to_str())
		else:
			output_path_checker.check_extension_correct()

	except IndexError:
		output_path = make_altered_path(
		input_path,
		after_stem=DFLT_OUTPUT_TERMINATION,
		extension=missing_output_warner.extension_to_str())

	except Exception as e:
		print(ERROR_INTRO + str(e))
		exit()

	# Real work
	reader = PdfFileReader(input_path.open(mode="rb"))
	field_list = get_pdf_field_list(reader)

	if field_list is None:
		print(str(input_path) + " does not contain fields.")
		exit()

	field_str = "\n".join(map(str, field_list))

	header = "Fields in file " + str(input_path) + "\n\n"
	output_path.write_text(header + field_str)
