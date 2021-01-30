from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import BooleanObject, IndirectObject, NameObject


def print_dictionary(d):
	for key, value in d.items():
		print(str(key) + ": " + str(value))


def set_need_appearances(pdf_writer, bool_val):
	# https://stackoverflow.com/questions/47288578/pdf-form-filled-with-pypdf2-does-not-show-in-print
	catalog = pdf_writer._root_object
	# Get the AcroForm tree and add "/NeedAppearances attribute
	if "/AcroForm" not in catalog:
		pdf_writer._root_object.update({
			NameObject("/AcroForm"): IndirectObject(len(pdf_writer._objects), 0, pdf_writer)})

	need_appearances = NameObject("/NeedAppearances")
	pdf_writer._root_object["/AcroForm"][need_appearances] = BooleanObject(bool_val)


input_stream = open("rapport_depenses.pdf", "rb")
template = PdfFileReader(input_stream)

template_info = template.getDocumentInfo()
print("Template document info")
print_dictionary(template_info)

writer = PdfFileWriter()
# Editable output file
#page = template.getPage(0)
#writer.addPage(page)

# Non editable output file
writer.cloneDocumentFromReader(template)
page = writer.getPage(0)

field_update = {"Nom": "Dupré",
				"Prenom": "Raphaëlle",
				"Group2": "\Choix2",
				"CodePermanent": "DUPR01060901"}
writer.updatePageFormFieldValues(page, field_update)
set_need_appearances(writer, True) # To make field values visible

output_stream = open("rapport_depenses_essai.pdf", "wb")
writer.write(output_stream)

input_stream.close()
output_stream.close()