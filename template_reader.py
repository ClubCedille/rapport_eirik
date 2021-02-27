from dict_util import print_dict
from PyPDF2 import PdfFileReader
from PyPDF2.generic import BooleanObject, IndirectObject, NameObject
from pypdf2_util import make_writer_from_reader, set_need_appearances

input_stream = open("rapport_depenses.pdf", "rb")
template = PdfFileReader(input_stream)

template_info = template.getDocumentInfo()
print_dict(template_info, "Template document info")

writer = make_writer_from_reader(template, False)

field_update = {"Nom": "Dupré",
				"Prenom": "Raphaëlle",
				"Group2": "/Choix2",
				"CodePermanent": "DUPR01060901",
				"Détails1": "Hôtel",
				"Montant$1": 999.99,
				"KM": 42,
				"UBR1": "UBR1"}
page = writer.getPage(0)
writer.updatePageFormFieldValues(page, field_update)
set_need_appearances(writer, True) # To make field values visible

output_stream = open("rapport_depenses_essai.pdf", "wb")
writer.write(output_stream)

input_stream.close()
output_stream.close()
