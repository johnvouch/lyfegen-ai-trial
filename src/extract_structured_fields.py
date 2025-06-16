import re


def extract_structured_fields(text: str) -> dict:
    """
        Extracts structured fields using simple pattern matching.

        Parameters
        ----------
        text : str
            The text to extract structured fields from.

        Returns
        -------
        dict
            The derived structured fields.

        """

    data = {}

    try:
        match = re.search(r"Parties?: (.+?)\n", text, re.IGNORECASE)
        data["parties"] = match.group(1) if match else None
    except Exception as ex:
        print(ex)
        data["parties"] = None

    try:
        match = re.search(r"Country: (.+?)\n", text, re.IGNORECASE)
        data["country"] = match.group(1) if match else None
    except Exception as ex:
        print(ex)
        data["country"] = None

    try:
        match = re.search(r"Disease Area: (.+?)\n", text, re.IGNORECASE)
        data["disease_area"] = match.group(1) if match else None
    except Exception as ex:
        print(ex)
        data["disease_area"] = None

    try:
        match = re.search(r"£[\d,]+", text)
        data["estimated_cost"] = match.group(0) if match else None
    except Exception as ex:
        print(ex)
        data["estimated_cost"] = None

    return data
