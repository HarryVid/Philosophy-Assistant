from pymupdf4llm import to_markdown
from pathlib import Path
from tqdm import tqdm


def pdf_to_md():
	PDF_PATH = "./data/TextBooksPDF/"
	MD_PATH = "./data/TextBooksMD/"
	if not list(Path(MD_PATH).glob('*.md')):
		PDFbooks = list(Path(PDF_PATH).glob('*.pdf'))
		for book in tqdm(PDFbooks):
			pdf_source = str(book).split('/')[2].split('.')[0]
			md_text = to_markdown(book)
			Path(f"{MD_PATH}{pdf_source}.md").write_bytes(md_text.encode())
		print("Finished Converting PDF to MD!")
	else:
		print("Markdown Documents Already Exist!")


pdf_to_md()
