from PyPDF2 import PdfFileReader
from PyPDF2.generic import BooleanObject, IndirectObject, NameObject
from pypdf2_util import make_writer_from_reader, set_need_appearances


def print_dictionary(d):
	for key, value in d.items():
		print(str(key) + ": " + str(value))


input_stream = open("rapport_depenses.pdf", "rb")
template = PdfFileReader(input_stream)

template_info = template.getDocumentInfo()
print("Template document info")
print_dictionary(template_info)

writer = make_writer_from_reader(template, False)

field_update = {"Nom": "Dupré",
				"Prenom": "Raphaëlle",
				"Group2": "\Choix2",
				"CodePermanent": "DUPR01060901",
				"Détails1": "Hôtel",
				"UBR1": "UBR1"}
page = writer.getPage(0)
writer.updatePageFormFieldValues(page, field_update)
set_need_appearances(writer, True) # To make field values visible

output_stream = open("rapport_depenses_essai.pdf", "wb")
writer.write(output_stream)

input_stream.close()
output_stream.close()
