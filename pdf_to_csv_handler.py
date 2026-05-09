# pdf_to_csv_handler.py

import pdfplumber
import pandas as pd
import re
import os

def extract_invoice_data(pdf_path):
    """
    Extracts DigiKey invoice item data
    from PDF text.
    """

    extracted_rows = []

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if not text:
                continue

            lines = text.split("\n")

            for line in lines:

                line = line.strip()

                # Only process lines containing part data
                if "PART:" not in line:
                    continue

                try:

                    # Example line:
                    # 1 1 0 1 PART: HM2740-ND DESC: CHASSIS ... 71.48000 71.48 T

                    # Extract leading numbers
                    leading_match = re.match(
                        r"^(\d+)\s+(\d+)\s+(\d+)\s+(\d+)",
                        line
                    )

                    if not leading_match:
                        continue

                    line_item = int(
                        leading_match.group(1)
                    )

                    ordered = int(
                        leading_match.group(2)
                    )

                    cancelled = int(
                        leading_match.group(3)
                    )

                    shipped = int(
                        leading_match.group(4)
                    )

                    # Extract part number
                    part_match = re.search(
                        r"PART:\s*([A-Z0-9\-\+]+)",
                        line
                    )

                    if not part_match:
                        continue

                    part_number = part_match.group(1)

                    # Extract description
                    desc_match = re.search(
                        r"DESC:\s*(.*?)\s+([\d\.]+)\s+([\d\.]+)\s+T?$",
                        line
                    )

                    if not desc_match:
                        continue

                    description = desc_match.group(1)

                    unit_price = float(
                        desc_match.group(2)
                    )

                    amount = float(
                        desc_match.group(3)
                    )

                    extracted_rows.append({

                        "Line Item":
                            line_item,

                        "Ordered":
                            ordered,

                        "Cancelled":
                            cancelled,

                        "Shipped":
                            shipped,

                        "Part Number":
                            part_number,

                        "Description":
                            description,

                        "Unit Price CAD":
                            unit_price,

                        "Amount CAD":
                            amount
                    })

                except Exception as e:

                    print(
                        f"[WARNING] Failed to parse line:\n{line}"
                    )

                    print(e)

    df = pd.DataFrame(extracted_rows)

    return df

def save_invoice_csv(df, output_path):
    """
    Saves extracted invoice data to CSV.
    """

    import os

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    df.to_csv(
        output_path,
        index=False
    )
