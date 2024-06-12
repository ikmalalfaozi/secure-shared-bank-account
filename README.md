# Shamir's Secret Sharing for Secure Shared Bank Account Access

This project demonstrates the implementation of Shamir's Secret Sharing (SSS) algorithm to enhance the security of shared bank account access. The project includes key generation, secret sharing, key distribution, and secret reconstruction, ensuring no single individual has full control over the account.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

This project aims to address the security challenges in managing a shared bank account by implementing Shamir's Secret Sharing. The algorithm allows a secret (e.g., an encryption key) to be split into multiple parts, distributed to account holders, and reconstructed only when a certain threshold of parts is combined.

## Features

- **Key Generation**: Generate a secret key for secure transactions.
- **Secret Sharing**: Split the secret key using Shamir's Secret Sharing algorithm.
- **Key Distribution**: Distribute key shares to account holders.
- **Secret Reconstruction**: Reconstruct the secret key for account access.
- **Efficient Implementation**: Handles large numbers and provides performance metrics for sharing and reconstruction.

## Requirements

- Python 3.6+
- Streamlit
- SymPy
- Secrets
- Random

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ikmalalfaozi/secure-shared-bank-account.git
    cd secure-shared-bank-account
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit app for SSS simulation:
    ```bash
    streamlit run app.py
    ```

2. Open your web browser and navigate to `http://localhost:8501`.

3. Use the sidebar menu to navigate through the different stages:
    - **Key Generation**: Generate a new secret key.
    - **Secret Sharing**: Split the secret key into shares.
    - **Key Distribution**: Distribute shares to account holders.
    - **Secret Reconstruction**: Reconstruct the secret key using the shares.

4. Run the Streamlit app for fund transfer simulation
    ```bash
    streamlit run transfer.py
    ```

## Acknowledgments

Special thanks to Dr. Rinaldi Munir, S.T, M.T., for his guidance and the authors of the referenced materials that helped in the completion of this project.

