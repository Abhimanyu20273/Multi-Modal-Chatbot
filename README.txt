# Multi-Modal Chatbot

This is a multi-modal chatbot that leverages OpenAI APIs and Langchain to provide a versatile interaction experience. Users can upload images and documents in various formats such as PDF, Word, Excel, and text, and ask questions about the content of these images/documents.

## Features

- **Multi-Modal Support**: Accepts and processes images and documents in multiple formats.
- **OpenAI API Integration**: Utilizes advanced natural language processing capabilities from OpenAI.
- **Langchain Integration**: Enhances document understanding and interaction.
- **Versatile Document Handling**: Supports PDF, Word, Excel, and text files.
- **Interactive Q&A**: Users can ask questions about the uploaded content and receive accurate responses.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- An OpenAI API key
- Required Python libraries: 
        openai==1.30.2
        langchain==0.2.1
        langchain-community==0.2.1
        langchain-openai==0.1.7
        python-dotenv==1.0.1
        opencv-python==4.10.0.84
### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/abhimanyu.../multi-modal-chatbot.git
    cd multi-modal-chatbot
    ```

2. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your OpenAI API key:
    ```bash
    export OPENAI_API_KEY='your-api-key-here'
    ```

### Usage

1. Run the chatbot application:
    ```bash
    python multimodal_chatbot.py
    ```

2. Upload your document or image through the provided interface.

3. Ask questions about the content of the uploaded document or image.

### Example

1. Upload a PDF document.
2. Ask: "What is the main topic of the document?"
3. The chatbot will analyze the content and provide a response based on the extracted information.

## Supported Formats

- **PDF**: Extracts text and images from PDF documents.
- **Word**: Handles `.doc` and `.docx` files.
- **Excel**: Processes `.xls` and `.xlsx` files.
- **Text**: Reads plain text files.
- **Image**: Supports `.jpg` and `.png` formats


## Acknowledgements

- [OpenAI](https://openai.com/) for the powerful API.
- [Langchain](https://langchain.com/) for enhancing document interaction capabilities.

