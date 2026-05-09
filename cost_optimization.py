# cost_optimization.py

import pandas as pd
import os


# Paths
INVOICE_CSV = "output_csv/parsed_invoice.csv"

COMPONENT_FOLDER = "component_costs"

OUTPUT_FOLDER = "output_csv/optimized_parts"


def normalize_columns(df):
    """
    Cleans column names.
    """

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    return df


def load_invoice():
    """
    Loads parsed invoice CSV.
    """

    if not os.path.exists(INVOICE_CSV):
        raise FileNotFoundError(
            f"Invoice CSV not found: {INVOICE_CSV}"
        )

    df = pd.read_csv(INVOICE_CSV)

    return df


def load_component_csv(part_number):
    """
    Loads component pricing CSV
    corresponding to the part number.
    """

    csv_path = os.path.join(
        COMPONENT_FOLDER,
        f"{part_number}.csv"
    )

    if not os.path.exists(csv_path):
        return None

    df = pd.read_csv(csv_path)

    df = normalize_columns(df)

    required_columns = [
        "quantity",
        "unit price",
        "ext price"
    ]

    for column in required_columns:

        if column not in df.columns:
            raise ValueError(
                f"Missing column '{column}' "
                f"in {csv_path}"
            )

    return df


def optimize_part(
    part_number,
    ordered_quantity,
    original_total,
    component_df
):
    """
    Finds best pricing tier
    for one component.
    """

    best_row = None

    lowest_total = None

    for _, row in component_df.iterrows():

        try:

            quantity = int(row["quantity"])

            unit_price = float(
                str(row["unit price"]).replace(",", "")
            )

            ext_price = float(
                str(row["ext price"]).replace(",", "")
            )

        except:
            continue

        # Ignore tiers below required quantity
        if quantity < ordered_quantity:
            continue

        # Find lowest total price
        if (
            lowest_total is None or
            ext_price < lowest_total
        ):
            lowest_total = ext_price
            best_row = row

    # Fallback if no bulk tier exists
    if best_row is None:

        best_row = component_df.iloc[-1]

        quantity = ordered_quantity

        unit_price = float(
            str(best_row["unit price"]).replace(",", "")
        )

        ext_price = (
            quantity * unit_price
        )

    else:

        quantity = int(best_row["quantity"])

        unit_price = float(
            str(best_row["unit price"]).replace(",", "")
        )

        ext_price = float(
            str(best_row["ext price"]).replace(",", "")
        )

    savings = (
        original_total - ext_price
    )

    return {

        "Part Number":
            part_number,

        "Original Quantity":
            ordered_quantity,

        "Suggested Quantity":
            quantity,

        "Original Total CAD":
            round(original_total, 2),

        "Optimized Unit Price CAD":
            round(unit_price, 4),

        "Optimized Total CAD":
            round(ext_price, 2),

        "Savings CAD":
            round(savings, 2)
    }


def save_part_csv(part_number, optimized_data):
    """
    Saves optimized result
    for a single part.
    """

    os.makedirs(
        OUTPUT_FOLDER,
        exist_ok=True
    )

    output_path = os.path.join(
        OUTPUT_FOLDER,
        f"{part_number}_optimized.csv"
    )

    df = pd.DataFrame([optimized_data])

    df.to_csv(
        output_path,
        index=False
    )


def optimize_all_parts():
    """
    Main optimization pipeline.
    """

    invoice_df = load_invoice()

    summary_rows = []

    for _, row in invoice_df.iterrows():

        part_number = row["Part Number"]

        ordered_quantity = int(
            row["Ordered"]
        )

        original_total = float(
            row["Amount CAD"]
        )

        print(
            f"[INFO] Optimizing {part_number}..."
        )

        component_df = load_component_csv(
            part_number
        )

        if component_df is None:

            print(
                f"[WARNING] No pricing CSV found "
                f"for {part_number}"
            )

            continue

        optimized_data = optimize_part(
            part_number,
            ordered_quantity,
            original_total,
            component_df
        )

        save_part_csv(
            part_number,
            optimized_data
        )

        summary_rows.append(
            optimized_data
        )

    # Save master summary CSV
    if summary_rows:

        summary_df = pd.DataFrame(
            summary_rows
        )

        summary_output = os.path.join(
            OUTPUT_FOLDER,
            "optimization_summary.csv"
        )

        summary_df.to_csv(
            summary_output,
            index=False
        )

        print("\n[SUCCESS] Optimization complete.")
        print(
            f"[SUCCESS] Summary saved:"
        )
        print(summary_output)
