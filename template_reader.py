from PyPDF2 import PdfFileReader

template = PdfFileReader(open("rapport_depenses.pdf", "rb"))

template_info = template.getDocumentInfo()
print("Template document info")
for key in template_info:
    print(key, ": ", template_info[key])