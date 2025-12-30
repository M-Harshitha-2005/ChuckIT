# ChunkIT – PDF Reading Companion with AI Chapter Summaries

A professional, minimalist Streamlit application designed to provide an elegant PDF reading experience combined with intelligent AI-generated chapter summaries.

## Overview

ChunkIT allows users to upload PDF documents and view them in a clean, Adobe Reader-like interface while offering on-demand AI summaries of detected chapters. The application emphasizes simplicity, performance, and readability.

## Features

- Clean PDF viewer with support for both small and large documents
- Automatic chapter detection using robust pattern matching
- AI-powered chapter summarization (detailed or bullet-point format)
- Resizable dual-panel layout for simultaneous viewing and summary reading
- Automatic removal of common non-content text (e.e., copyright notices, piracy warnings)
- Offline operation after initial model download

## Requirements

- Python 3.9 or higher

## Installation

1. Clone or download the project files.
2. Install the required dependencies:
pip install -r requirements.txt
text## Usage

1. Launch the application:
streamlit run app.py
text(Replace `app.py` with the actual filename if different.)

2. The application will open in your default web browser.
3. Upload a PDF document using the file uploader.
4. Select a detected chapter from the dropdown menu.
5. Choose the desired summary style and click "Generate Summary".
6. Read the PDF on the left panel while reviewing the AI summary on the right.

## Project Files

- `app.py` – Main application source code
- `requirements.txt` – Python package dependencies
- `README.md` – Project documentation

## Dependencies (requirements.txt)
streamlit==1.38.0
pypdf==4.3.1
transformers==4.44.2
torch==2.4.1
textThe summarization model (approximately 250 MB) is downloaded automatically on first run and cached locally for subsequent use.

## Notes

- For optimal performance with large PDFs, the application employs a professional PDF.js viewer when necessary.
- The application is designed for personal, offline use after initial setup.

