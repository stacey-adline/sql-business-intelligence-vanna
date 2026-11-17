# SQL Business Intelligence with Vanna AI

A starter project for asking business-data questions in plain English and converting them into SQL with Vanna AI.

## Features
- SQLite business database with sample Superstore-style orders
- Vanna AI natural-language-to-SQL integration
- Streamlit chat interface
- Schema and business documentation training
- Read-only SQL execution guard
- Ten example business questions
- Basic tests and setup instructions

> The included records are synthetic demo data, not the official Kaggle Superstore dataset. Replace them with the approved dataset if your internship requires it.

## 1. Requirements
- Python 3.10 or newer
- An OpenAI API key for the Vanna OpenAI integration
- Internet access for installing packages

## 2. Setup (Windows PowerShell)
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and add your API key:
```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

## 3. Create the database
```powershell
python -m src.seed_data
```

## 4. Train Vanna on the schema
```powershell
python -m src.train
```

Training uses Vanna's local ChromaDB vector store. Training data is stored locally in `chroma_db/`.

## 5. Run the application
```powershell
streamlit run app.py
```
Open the local URL shown in the terminal.

## 6. Ten demo natural-language queries
1. What is the total sales amount?
2. What is the total profit?
3. Show sales by region.
4. Which five products have the highest sales?
5. Which category has the highest profit?
6. Show monthly sales for 2025.
7. Which are the top five customers by sales?
8. How many orders are there in each region?
9. What is the average discount by category?
10. Which sub-category has the lowest total profit?

## Project structure
```text
sql-business-intelligence-vanna/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── seed_data.py
│   ├── vanna_client.py
│   └── train.py
├── data/
│   └── .gitkeep
└── tests/
    └── test_database.py
```

## Notes / troubleshooting
- Never commit `.env` or share your API key.
- If PowerShell blocks activation, run:
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
  and activate the environment again.
- If Vanna package APIs change in a newer release, install the pinned version in `requirements.txt`.
- The app displays generated SQL and its results. Only read-only `SELECT` / `WITH` queries are allowed.
- This is a learning/demo implementation; review generated SQL and results before relying on them for business decisions.
