# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Expense Tracker is a Python application that processes Desjardins credit card PDF statements, categorizes transactions using pattern matching with interactive learning, and uploads expenses to Notion databases.

## Commands

```bash
# Run the application
python -m src.main

# Run tests
pytest tests/

# Install dependencies
pip install -r requirements.txt
```

## Architecture

The application follows a 7-step pipeline defined in `src/main.py`:

1. Load configuration from `.env`
2. Find transaction directory
3. Connect to Notion API
4. Select PDF input files
5. Extract tables from PDFs (pdfplumber)
6. Parse transactions (Desjardins-specific format)
7. Categorize and upload to Notion

### Module Structure

- **src/ocr/extraction.py** - PDF table extraction using pdfplumber (`extract_table_transactions`)
- **src/parsing/desjardins.py** - Desjardins statement parsing, date/amount cleaning, returns pandas DataFrame
- **src/categorization/categories.py** - Pattern-based categorization with interactive learning for unknown merchants
- **src/notion_api/client.py** - Notion database operations (`process` function creates expense records)
- **src/utils/config.py** - Environment variable management (must call `init_config()` at startup)
- **src/utils/file_handler.py** - File I/O, JSON persistence, PDF discovery

### Data Flow

PDF files → pdfplumber extraction → Desjardins parser (DataFrame) → categorization → Notion API upload

### Key Data Files

- `data/categories/Database.json` - Category definitions with Notion page IDs and learned merchant patterns
- `data/pdf/` - Input PDF files location

## Configuration

Required environment variables in `.env`:
- `NOTION_API_TOKEN` - Notion API authentication
- `EXPENSE_DATABASE_ID` - Target Notion database for expenses
- `ACCOUNT_LINKING_ID` - Notion page ID for account relations
- `TRANSACTION_DIRS` - Comma-separated paths to check for transaction files

## Technical Notes

- Recent migration from Tesseract OCR to pdfplumber for PDF processing (commit 8994dbd)
- Categories store Notion page IDs for database relations
- Date parsing handles "DD MM" format from credit statements with smart year inference
- Amount parsing handles "CR" markers for credits/income
- Interactive CLI uses questionary for user prompts
- Supports Excel editing of extracted transactions before upload
