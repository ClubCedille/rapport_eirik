from pathlib import Path
from PyPDF2 import PdfFileReader
from sys import argv, exit

INPUT_EXTENSION = ".pdf"

try:
	input_path = Path(argv[1])
except IndexError:
	print("ERROR! Need the input file as the first argument.")
	exit()

if not input_path.exists():
	print("ERROR! " + str(input_path) + " does not exist.")
	exit()

if not input_path.suffix == INPUT_EXTENSION:
	print("ERROR! The input file must have the extension " + INPUT_EXTENSION + ".")
	exit()

reader = PdfFileReader(input_path.open(mode="rb"))
field_values = reader.getFormTextFields()

field_str = str()
for field, value in field_values.items():
	field_str += str(field) + ": " + str(value) + "\n"

output_path = Path("field_values.txt")
output_path.write_text(field_str)
