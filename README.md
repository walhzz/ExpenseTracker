# Expense Tracker

Automated expense processing from bank statements using OCR, pattern matching, and Notion API integration.

## Features

- 📸 **OCR Processing**: Extract text from bank statement images using Tesseract
- 🏦 **Desjardins Parser**: Parse and clean Desjardins bank transaction data
- 🏷️ **Smart Categorization**: Pattern matching with interactive learning
- 📊 **Notion Integration**: Automatic upload to Notion databases
- 🔐 **Secure Configuration**: Environment variables for sensitive data

## Project Structure

```
expense-tracker/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Entry point CLI
│   ├── ocr/
│   │   ├── __init__.py
│   │   └── extraction.py       # Tesseract + image processing
│   ├── parsing/
│   │   ├── __init__.py
│   │   └── desjardins.py       # Transaction parsing & data transformation
│   ├── categorization/
│   │   ├── __init__.py
│   │   └── categories.py       # Category management logic
│   ├── notion_api/
│   │   ├── __init__.py
│   │   └── client.py           # Notion database operations
│   └── utils/
│       ├── __init__.py
│       ├── config.py           # Environment configuration
│       └── file_handler.py     # JSON loading/saving
├── data/
│   ├── categories/
│   │   ├── Database.json       # List of category names
│   │   ├── id.json             # Notion page IDs
│   │   └── {Category}.json     # Pattern files for each category
│   └── screenshots/            # Input images go here
├── tests/
│   ├── __init__.py
│   ├── test_ocr.py
│   ├── test_parsing.py
│   ├── test_categorization.py
│   └── test_integration.py
├── .env                        # Your credentials (not in git)
├── .env.example                # Template for .env
├── .gitignore
├── requirements.txt
├── README.md
├── script4_legacy.py           # Original monolithic script (backup)
└── script4.py                  # Backward compatibility wrapper
```

## Installation

### Prerequisites

- Python 3.10+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed
- Notion account with API access

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/walhzz/ExpenseTracker.git
cd ExpenseTracker
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. **Set up data directory**
   - Place your bank statement images in `data/screenshots/`
   - Configure categories in `data/categories/Database.json`
   - Add Notion page IDs in `data/categories/id.json`

## Usage

### Run the application

```bash
python -m src.main
```

Or using the legacy interface:

```bash
python script4.py
```

### Workflow

1. **Image Processing**: Place .jpeg bank statement images in `data/screenshots/` or configure `TRANSACTION_DIRS` in `.env`
2. **OCR Extraction**: Application reads all images and extracts text
3. **Transaction Parsing**: Parses Desjardins-specific format (dates, amounts, descriptions)
4. **Interactive Editing**: Optional Excel editing for corrections
5. **Categorization**: Automatic categorization with manual override for unknowns
6. **Notion Upload**: Creates expense/income records in your Notion databases

## Configuration

### Environment Variables (.env)

```env
# Notion API
NOTION_API_TOKEN=your_notion_api_token
EXPENSE_DATABASE_ID=your_expense_database_id
INCOME_DATABASE_ID=your_income_database_id
ACCOUNT_LINKING_ID=your_account_linking_id

# Tesseract OCR
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe

# Transaction Directories (comma-separated)
TRANSACTION_DIRS=C:\Users\YourName\iCloudDrive\Transaction
```

### Category Setup

**data/categories/Database.json**
```json
[
  "Grocery",
  "Restaurant",
  "Transport",
  "Entertainment"
]
```

**data/categories/Grocery.json**
```json
[
  "maxi",
  "dollarama",
  "walmart"
]
```

## Development

### Run tests

```bash
pytest tests/
```

### Project Architecture

- **src/ocr**: Image processing and OCR text extraction
- **src/parsing**: Bank statement parsing and data transformation
- **src/categorization**: Pattern-based expense categorization
- **src/notion_api**: Notion database API integration
- **src/utils**: Configuration management and file I/O

## Version History

### v2.0.0 (Current)
- ✅ Modular architecture with src/, data/, tests/
- ✅ Improved code organization and maintainability
- ✅ Environment variable configuration
- ✅ Comprehensive test suite
- ✅ Better separation of concerns

### v1.0.0 (Legacy)
- Single monolithic script (script4_legacy.py)
- Basic OCR and Notion integration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is private and for personal use.

## Author

**Walid**

## Acknowledgments

- Built with [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- Uses [Notion API](https://developers.notion.com/)
- Powered by Python 🐍
