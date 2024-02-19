# The Recommender Application

This application is built using Python, the Streamlit library, and the Ollama API. It is designed to generate recommendation letters for students based on the classes they have taken and additional information provided by the user.

## How it works

The application uses the Ollama API to generate the recommendation letters. The user provides the student's first and last names, the purpose of the recommendation (e.g., applying for grad school), and any additional information that might be relevant. The user also selects from a list of classes that the student has taken.

The application then sends this information to the Ollama API, which generates a recommendation letter based on the input.

## Code Structure

The code is structured as follows:

- The Streamlit library is used to create the user interface. This includes text input fields for the student's first and last names, the purpose of the recommendation, and additional information. There is also a multi-select field for the classes the student has taken.
- The Ollama API is used to generate the recommendation letter. The input from the user is formatted into a prompt that is sent to the API. The API's response is then displayed in the application.
- Error handling is included to ensure that the user has provided all necessary information before the recommendation letter is generated.

## Installation and Setup

### Prerequisites

Ensure you have Python installed on your system. This application requires Python 3.11 or newer.

### Step 1: Install Python packages

You can install all required packages by running:

    pip install -r requirements.txt

### Step 2: Install Ollama

Before running the application, you need to install Ollama and pull the `openchat` large language model. Please visit https://github.com/ollama/ollama to download and install Ollama.

### Step 3: Run Ollama Serve and Pull the OpenChat Model

To make the Ollama API available for your application, run:

    ollama serve

This command starts a local server that allows your application to communicate with the Ollama API.

After installing Ollama and starting ollama serve, pull the `openchat` model by running:

    ollama pull openchat

This command downloads the OpenChat model to your local machine.
OpenChat is a small LLM model that is roughlu ~4 GB download.
Depending on your internet connection, it may take a few minutes to download Openchat.

## How to Run the Application

With Ollama running, you can now start the Streamlit application.

Navigate to the directory containing the Python application and run:

    streamlit run recommender_app.py

This command starts the Streamlit server and opens the application in your web browser.

## Dependencies

To manage project dependencies, it is recommended to use a `requirements.txt` file. The `requirements.txt` for this project includes:

    streamlit
    ollama

Following these instructions will help you to set up and run the Recommender Application on your local machine. For further assistance or troubleshooting, refer to the official Ollama and Streamlit documentation.
