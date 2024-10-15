# Question 1

## Overview

This is a Tkinter-based text summarization application that uses the Hugging Face BART model for summarization. The app provides two key functionalities:
1. **Summarize Text**: Generates a summary from the input text using the BART model.
2. **Rephrase Summary**: Provides a variation of the summary by using random sampling.

## Features

- **Summarization**: Automatically generates a concise summary for any input text.
- **Rephrasing**: Offers a rephrased version of the summary for variety.
- **Clear Text**: Allows clearing both the input and output fields.
- **Help Menu**: Provides information on how to use the application and displays application details.

## Requirements

Before running the application, make sure you have the following packages installed:

- `tkinter`: For creating the graphical user interface.
- `transformers`: For using the Hugging Face BART model.
- `torch`: Required for model inference with `transformers`.

## Package Installation

To install the required Python packages, use the following commands:

```bash
pip install -r requirements.txt
```

## How to Run the Application

- Clone this repository or copy the code to your local machine.
- Ensure that the necessary packages are installed.
- Run the following command in your terminal or command prompt:

```bash
python question1/summarizer_app.py
```
- The application window will open, allowing you to input text, summarize it, rephrase the summary, and clear the fields.

## Usage Instructions
- Enter the text you want to summarize in the Input Text area.
- Click the Summarize button to get the summarized output.
- Click the Rephrase button to generate a variation of the summary.
- Use the Clear button to reset both the input and output fields.
- Navigate to the Help menu for more details about the application and instructions.

# Question 2