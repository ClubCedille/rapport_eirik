from PyPDF2 import PdfFileWriter
from PyPDF2.generic import BooleanObject, IndirectObject, NameObject


def make_writer_from_reader(pdf_reader, editable):
	pdf_writer = PdfFileWriter()

	if editable:
		for page in pdf_reader.pages:
			pdf_writer.addPage(page)
	else:
		pdf_writer.cloneDocumentFromReader(pdf_reader)

	return pdf_writer


def set_need_appearances(pdf_writer, bool_val):
	# https://stackoverflow.com/questions/47288578/pdf-form-filled-with-pypdf2-does-not-show-in-print
	catalog = pdf_writer._root_object
	# Get the AcroForm tree and add "/NeedAppearances attribute
	if "/AcroForm" not in catalog:
		pdf_writer._root_object.update({
			NameObject("/AcroForm"): IndirectObject(len(pdf_writer._objects), 0, pdf_writer)})

	need_appearances = NameObject("/NeedAppearances")
	pdf_writer._root_object["/AcroForm"][need_appearances] = BooleanObject(bool_val)


def update_checkboxes(page, fields):
	# https://stackoverflow.com/questions/35538851/how-to-check-uncheck-checkboxes-in-a-pdf-with-python-preferably-pypdf2
	for j in range(0, len(page["/Annots"])):
		writer_annot = page["/Annots"][j].getObject()
		for field in fields:
			if writer_annot.get("/T") == field:
				writer_annot.update({
					NameObject("/V"): NameObject(fields[field]),
					NameObject("/AS"): NameObject(fields[field])
				})
