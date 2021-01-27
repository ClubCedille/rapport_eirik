from PyPDF2 import PdfFileReader

def print_dictionary(d):
	for key, value in d.items():
		print(str(key) + ": " + str(value))

template = PdfFileReader(open("rapport_depenses.pdf", "rb"))

template_info = template.getDocumentInfo()
print("Template document info")
print_dictionary(template_info)

template_fields = template.getFields()
print("\nTemplate document fields")
if template_fields is None:
	print("No fields")
else:
	print_dictionary(template_fields)

template_field_values = template.getFormTextFields()
print("\nTemplate document field values")
if template_field_values is None:
	print("No fields")
else:
	print_dictionary(template_field_values)
