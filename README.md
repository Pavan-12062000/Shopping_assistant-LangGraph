# Shopping Assistant Project

A simple shopping assistant system that allows users to search for products, add them to a cart, view the cart, and proceed to checkout. This project uses Python and utilizes environment variables for configuration.

## Table of Contents
- [Installation](#installation)
- [Setup](#setup)
- [Running the Project](#running-the-project)
- [Project Structure](#project-structure)

---

## Installation

Follow these steps to set up the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/shopping-assistant.git
cd shopping-assistant
```

### 2. Create a Virtual Environment (Optional but Recommended)
It's recommended to set up a virtual environment to manage dependencies.
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install dependencies
Install the required dependencies via pip.
```bash
pip install -r requirements.txt
```

## Setup
Before running the application, you need to set up the .env file, which stores sensitive API keys and other configuration settings.
### 1. Create .env file
In the root directory of the project, create a file named .env.
### 2. Configure .env File
Populate the .env file with the following environment variables:
```bash
OPENAI_API_KEY = your_api_key
ENVIRONMENT = development
GROQ_API_KEY = your_api_key
```

## Running the project
Once you have installed the dependencies and set up your .env file, you can run the project.
### 1. Start the Application
To start the application and run the shopping assistant system, execute:
```bash
python main.py
```

### 2. Interact with the Shopping Assistant
Once the application is running, you will be prompted to interact with the shopping assistant. You can search for products, add them to your cart, view the cart, and proceed to checkout.

## Project Structure
Here’s an overview of the project structure:
shopping-assistant/

### Breakdown of files:

- **main.py**: The starting point of the application where the user interacts with the shopping assistant.
- **tools.py**: Contains the core logic such as cart management, checkout process, and order handling.
- **products.json**: A JSON file that holds sample product data used during product searches.
- **requirements.txt**: Contains all the dependencies for the project. It is used to set up the environment.
- **.env**: A configuration file where you will store sensitive information like API keys.
- **README.md**: This file, explaining the project setup and usage.
- **venv/**: The virtual environment directory that contains all the Python packages.

