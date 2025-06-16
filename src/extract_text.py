import fitz


def extract_text_from_pdf(path):
    """
    Extracts all text content from a PDF file using PyMuPDF.

    Parameters
    ----------
    path : str
        The full path to the PDF file.

    Returns
    -------
    str
        The concatenated text from all pages in the PDF.

    """

    doc = fitz.open(path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


def split_text_into_chunks(text, chunk_size=500, overlap=50):
    """
    Splits a long text into overlapping chunks.

    Parameters
    ----------
    text : str
        The full text to split.
    chunk_size : int, optional
        The size of each chunk in characters (default is 500).
    overlap : int, optional
        The number of characters to overlap between chunks (default is 50).

    Returns
    -------
    list of str
        A list of text chunks.

    """

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks
