# Data Directory

This directory contains application data and input files.

## Structure

### categories/
Contains JSON files for expense categorization:
- `Database.json` - List of all category names
- `id.json` - Corresponding Notion page IDs for each category
- `{CategoryName}.json` - Pattern files for each category containing merchant names/descriptions

### screenshots/
Place your bank statement images (.jpeg files) here for processing.

## Example categories/Database.json

```json
[
  "Grocery",
  "Restaurant",
  "Transport",
  "Entertainment",
  "Utilities"
]
```

## Example categories/id.json

```json
[
  "notion-page-id-1",
  "notion-page-id-2",
  "notion-page-id-3",
  "notion-page-id-4",
  "notion-page-id-5"
]
```

## Example categories/Grocery.json

```json
[
  "maxi",
  "dollarama",
  "walmart"
]
```
