

											*** DigiKey Invoice Optimizer ***

-------------------------------------------------------------------------------------------------------

* Overview:

This project is a Python-based procurement and pricing optimization tool designed specifically for DigiKey invoices.

The program:
- Reads and parses DigiKey PDF invoices
Extracts:
- Ordered quantity
- Shipped quantity
- Part number
- Description
- Unit price
- Total amount
- Converts invoice data into structured CSV files
- Matches invoice part numbers to individual component pricing CSVs
- Analyzes bulk pricing tiers
- Calculates more cost-efficient purchasing quantities
- Generates optimized CSV reports

The system is modular and designed for future expansion, including:
- DigiKey API integration
- GUI support
- Multi-vendor compatibility
- Inventory tracking
- Live pricing analysis

-------------------------------------------------------------------------------------------------------

* Features:
- PDF Invoice Parsing
- Parses DigiKey PDF invoices
- Extracts component line items automatically

* Detects:
- Part numbers
- Descriptions
- Quantities
- Pricing
- Converts invoice data into structured CSV format
- Bulk Pricing Optimization

* For every component found in the invoice:
- Searches for a matching CSV file inside component_costs/
- Loads quantity pricing tiers
- Finds the most cost-efficient pricing option
- Detects cases where ordering more parts reduces total cost
- Generates optimized reports

-------------------------------------------------------------------------------------------------------

* Current Limitations:
- DigiKey invoices only
- Assumes text-based PDFs
- No OCR support yet
- No API integration yet
- CSV formatting must remain consistent

* Planned Features:
- DigiKey API integration
- GUI interface
- Drag-and-drop PDF support
- Live pricing updates
- Multi-vendor support
- Inventory awareness
- Constraint-based procurement optimization
- Historical pricing analysis

-------------------------------------------------------------------------------------------------------

* Technologies Used:
- Python
- pdfplumber
- pandas
- Regular Expressions (re)

