from PyPDF2 import PdfFileReader, PdfFileWriter
#from PyPDF2 import BooleanObject, NameObject, PdfFileReader, PdfFileWriter

#def make_field_content_visible(pdf_reader):
	#https://github.com/mstamy2/PyPDF2/issues/355#issuecomment-353217311
#	if "/AcroForm" in pdf_reader.trailer["/Root"]:
#		pdf_reader.trailer["/Root"]["/AcroForm"].update(
#			{NameObject("/NeedAppearances"): BooleanObject(True)})


def print_dictionary(d):
	for key, value in d.items():
		print(str(key) + ": " + str(value))


input_stream = open("rapport_depenses.pdf", "rb")
template = PdfFileReader(input_stream)
writer = PdfFileWriter()
#make_field_content_visible(template)

template_info = template.getDocumentInfo()
print("Template document info")
print_dictionary(template_info)

#writer.cloneDocumentFromReader(template)
#make_field_content_visible(writer)

#page = writer.getPage(0)
page = template.getPage(0)
writer.addPage(page)
field_update = {"Nom": "Dupré",
				"Prenom": "Jeanne",
				"Group2": "\Choix2",
				"CodePermanent": "DUPJ01060901"}
writer.updatePageFormFieldValues(page, field_update)

output_stream = open("rapport_depenses_essai.pdf", "wb")
writer.write(output_stream)

input_stream.close()
output_stream.close()