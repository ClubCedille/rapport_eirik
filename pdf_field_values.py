from PyPDF2 import PdfFileReader
from pathlib import Path

reader = PdfFileReader(open("rapport_depenses.pdf", "rb"))
field_values = reader.getFormTextFields()

field_str = str()
for field, value in field_values.items():
	field_str += str(field) + ": " + str(value) + "\n"

output_path = Path("field_values.txt")
output_path.write_text(field_str)
