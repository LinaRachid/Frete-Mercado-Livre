# Mercado Livre Shipping Cost Extractor

![Python](https://img.shields.io/badge/Language-Python-blue) ![Mercado Livre](https://img.shields.io/badge/Platform-Mercado_Livre-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

## Description
A Python GUI tool to extract shipping costs from Mercado Livre listings using the API endpoint `https://api.mercadolibre.com/items/{ad_id}/shipping_options?zip_code={zip_code}`. Features asynchronous batch processing based on the sender's ZIP code, with a custom icon for the executable.

## Why This Matters for Data Analysts
For data analysts working with e-commerce data, obtaining accurate shipping costs from Mercado Livre listings is often a critical step in pricing analysis, cost optimization, and market research. Traditionally, this required time-consuming methods like web scraping, which are prone to errors due to website changes and rate-limiting issues. This tool solves that problem by:

- **Direct API Access**: Uses the official Mercado Livre API for reliable and accurate data extraction.
- **Batch Processing**: Processes multiple ad IDs asynchronously, saving hours of manual work.
- **Error Handling**: Provides clear feedback on failures, ensuring data quality.
- **No Web Scraping Hassles**: Unlike web scraping, this tool avoids the need for fragile HTML parsing, offering a more robust and maintainable solution.

## Important Notice
⚠️ **This tool extracts shipping costs only for Mercado Livre listings, not Mercado Shops.** Shipping costs on Mercado Shops may differ from Mercado Livre. Note that Mercado Shops will be discontinued by Mercado Livre on 31/12/2025. Until then, ensure the ad ID you provide belongs to a Mercado Livre listing to avoid confusion with shipping cost values.

## Features
- Flexible ad ID input (e.g., `MLB1234567891`, `1234567891`, or one per line).
- Flexible ZIP code input (e.g., `01001000`, `01.001-000`).
- Fast batch processing with asynchronous requests, preserving input order.
- Simple Tkinter GUI with custom icon.
- Detailed error handling with user-friendly messages.

## Requirements
- **Python 3.6+**: Must include `tkinter` (typically pre-installed with Python).
- **`aiohttp`**: Install via `pip install aiohttp` for asynchronous HTTP requests.

## Installation and Usage

### Executable
1. Download `MercadoLivreShipping.exe` from the repository root.
2. Ensure an active internet connection.
3. Run: `MercadoLivreShipping.exe`

### Source Code
1. Clone the repository:
   ```bash
   git clone https://github.com/LinaRachid/frete-mercado-livre.git

## Contact
For bugs, errors, issues, suggestions, ideas, or inquiries, feel free to contact me:

**Lina Rachid**  
[GitHub](https://github.com/LinaRachid) | Email: linarachid.ti@gmail.com

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
