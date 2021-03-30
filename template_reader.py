from container_util import print_container
from PyPDF2 import PdfFileReader
from pypdf2_util import make_writer_from_reader, set_need_appearances

input_stream = open("rapport_depenses.pdf", "rb")
reader = PdfFileReader(input_stream)

template_info = reader.getDocumentInfo()
print_container(template_info, "Template document info")

writer = make_writer_from_reader(reader, False)

field_update = {"Date": "2021-03-01",
				"Nom": "Dupré",
				"Prenom": "Raphaëlle",
				"Group2": "/Choix2",
				"CodePermanent": "DUPR01060901",
				"Group4": "/Ch#E8que", # Values "/Ch#E8que" and "/Chèque" do not work.
				#"Boite1": "/Oui", # Causes updatePageFormFieldValues to fail.
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
