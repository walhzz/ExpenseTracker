# Expense Tracker

![Desjardins Logo](data/images/desjardinLogo.png)

## Why I Built This

I wanted one simple thing: to know exactly where my money goes each month. Sounds basic, right? But as a Desjardins customer, this turned out to be surprisingly difficult.

### The Problem

Like many people, I use Desjardins for my banking. When I decided to get serious about tracking my expenses, I quickly ran into walls:

**No API Access** - Unlike some banks that offer developer APIs, getting programmatic access to Desjardins data is essentially impossible for regular customers. There's no official API, and the unofficial routes are complex and unreliable.

**No Compatible Apps** - I tried finding expense tracking apps that could connect to Desjardins. Most popular budgeting apps either don't support Canadian banks at all, or specifically don't work with Desjardins. The ones that claim to support it often have connection issues or missing features.

**AccèsD's Built-in Tracking Falls Short** - Desjardins does have some expense tracking features in AccèsD, but I found them inaccurate. The auto-categorization frequently misclassifies transactions, and there's no easy way to export the data or integrate it with my personal finance workflow in Notion.

### What I Actually Wanted

I needed a system that would:

- Extract my transaction data accurately from Desjardins statements
- Let me categorize expenses my way, not some algorithm's best guess
- Learn my spending patterns over time
- Sync everything to Notion where I manage my finances

Since no existing solution did this, I built my own.

---

## The Solution

This project processes Desjardins credit card PDF statements, extracts every transaction, and uploads them to my Notion expense database. It handles the quirky formatting of Desjardins statements and learns to categorize recurring merchants automatically.

### Key Features

- **PDF Table Extraction** - Uses pdfplumber to accurately extract transaction tables from Desjardins credit card statements
- **Desjardins-Specific Parsing** - Handles the particular date formats, amount displays, and table structures used by Desjardins
- **Smart Categorization** - Pattern matching that learns from your categorization choices and remembers them for future transactions
- **Notion Integration** - Direct upload to Notion databases with proper relations and properties
- **Interactive Workflow** - Review and edit transactions before uploading, with optional Excel editing for corrections

---

## Technical Documentation

### Architecture

The application follows a pipeline workflow:

1. **PDF Processing** - Extract tables from Desjardins PDF statements using pdfplumber
2. **Transaction Parsing** - Parse dates, amounts, and descriptions into structured data
3. **Categorization** - Match merchants to categories using learned patterns
4. **Notion Upload** - Create expense records in your Notion database

### Project Structure

```
expense-tracker/
├── src/
│   ├── categorization/
│   │   └── categories.py       # Category management & pattern matching
│   ├── notion_api/
│   │   └── client.py           # Notion database operations
│   ├── ocr/
│   │   └── extraction.py       # PDF table extraction (pdfplumber)
│   ├── parsing/
│   │   └── desjardins.py       # Transaction parsing & data transformation
│   └── utils/
│       ├── config.py           # Environment configuration
│       └── file_handler.py     # File I/O utilities
├── data/
│   ├── categories/
│   │   ├── Database.json       # Category definitions with Notion IDs & patterns
│   │   └── id.json             # Legacy ID mapping
│   ├── images/                 # Static assets
│   └── pdf/                    # Input PDF statements
├── tests/
│   └── notion_api/
│       └── test_client.py      # Notion API unit tests
├── main.py                     # Application entry point
├── .env                        # Your credentials (not in git)
├── .env.example                # Template for .env
└── requirements.txt
```

### Installation

#### Prerequisites

- Python 3.10+
- Notion account with API access

#### Setup

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
   - Place your Desjardins PDF statements in `data/pdf/`
   - Configure categories in `data/categories/Database.json`

### Configuration

#### Environment Variables (.env)

```env
# Notion API
NOTION_API_TOKEN=your_notion_api_token
EXPENSE_DATABASE_ID=your_expense_database_id
INCOME_DATABASE_ID=your_income_database_id
ACCOUNT_LINKING_ID=your_account_linking_id

# Transaction Directories (comma-separated)
TRANSACTION_DIRS=C:\Users\YourName\iCloudDrive\Transaction
```

#### Category Database (data/categories/Database.json)

This file defines your expense categories and links them to your Notion database. Location: `data/categories/Database.json`

```json
[
  {
    "id": "your_notion_page_id_for_groceries",
    "name": "Groceries",
    "expenses": ["Costco", "Metro", "Loblaws"]
  },
  {
    "id": "your_notion_page_id_for_restaurants",
    "name": "Restaurants",
    "expenses": ["McDonald's", "Pizza Hut"]
  }
]
```

**Field descriptions:**

| Field      | Description                                                                                                                                                     |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`       | The Notion page ID for this category. Found in your Notion database URL when viewing the category page.                                                         |
| `name`     | Display name for the category. Must match exactly with your Notion database category names.                                                                     |
| `expenses` | Array of merchant name patterns. When a transaction description contains any of these strings (case-insensitive), it's automatically assigned to this category. |

**Important notes:**

- The `id` must be a valid Notion page ID from your expense categories database
- New merchant patterns are automatically added to `expenses` when you categorize unknown transactions
- Pattern matching is case-insensitive and uses substring matching (e.g., "Metro" matches "METRO PLUS MONTREAL QC")

### Usage

```bash
python -m src.main
```

The interactive CLI will guide you through:

1. Selecting PDF files to process
2. Reviewing extracted transactions (with optional Excel editing)
3. Categorizing any unknown merchants
4. Uploading to Notion

### Running Tests

```bash
pytest tests/
```

---

## Version History

### v2.0.0 (Current)

- Migrated from OCR/image processing to direct PDF table extraction
- Modular architecture with clear separation of concerns
- Environment variable configuration
- Interactive CLI workflow

### v1.0.0 (Legacy)

- Single monolithic script
- Tesseract OCR-based image processing

---

## Author

**Walid**

## License

This project is private and for personal use.
