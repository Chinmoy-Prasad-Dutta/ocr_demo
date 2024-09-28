# GOT-OCR

General OCR Theory is a unified End-to-End Model. Here, I have made a simple implementation of this model using HuggingFace and Gradio

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt File.


```bash

python -m pip install requirements.txt

```

**Please Note :** This app may require a HuggingFace token. Make a .env file and fill that file with 
```
HF_TOKEN1 = "your_huggingface_token"
```
For more information on huggingface token visit [this link](https://huggingface.co/docs/hub/en/security-tokens)

**Some additional requirements**(for running on local machine):
1. Nvidia CUDA drivers


## Usage

1. Clone the repository
```
git clone https://github.com/Chinmoy-Prasad-Dutta/ocr_demo.git
```

cd into the directory
Open terminal and follow the installation process
After the installation of requirements.txt run the command 
```
python app.py
```

The Gradio app will run on local machine provided the requirements are met.

Thank you!