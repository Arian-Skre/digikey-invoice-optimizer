import os
import pandas as pd

from pdf_to_csv_handler import (
    extract_invoice_data,
    save_invoice_csv
)

from cost_optimization import (
    optimize_all_parts
)

def main():
    print("=" * 50)
    print(" DigiKey Invoice Optimization Tool ")
    print("=" * 50)

    # Ask user for PDF filename
    pdf_name = input("\nEnter DigiKey PDF filename: ").strip()

    # Build full path
    pdf_path = pdf_name

    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"\n[ERROR] File not found: {pdf_path}")
        return

    print("\n[INFO] Loading PDF...")

    try:
        # Extract invoice data from PDF
        invoice_df = extract_invoice_data(pdf_path)

        # Check if extraction succeeded
        if invoice_df.empty:
            print("[ERROR] No invoice data extracted.")
            return

        print("[SUCCESS] PDF parsed successfully.")

        # Save parsed CSV
        parsed_csv_path = os.path.join(
            "output_csv",
            "parsed_invoice.csv"
        )

        save_invoice_csv(invoice_df, parsed_csv_path)

        print(f"[SUCCESS] Parsed CSV saved:")
        print(f"          {parsed_csv_path}")

        # Run optimization
        print("\n[INFO] Running cost optimization...")

        optimize_all_parts()

    except Exception as e:
        print(f"\n[ERROR] Program failed:")
        print(str(e))


if __name__ == "__main__":
    main()
