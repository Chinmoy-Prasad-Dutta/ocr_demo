import os
import uuid
import base64
import numpy as np
from PIL import Image
from transformers import AutoModel, AutoTokenizer
import shutil

# ........................................................................................................

tokenizer = AutoTokenizer.from_pretrained('ucaslcl/GOT-OCR2_0', trust_remote_code=True)
model = AutoModel.from_pretrained('ucaslcl/GOT-OCR2_0', trust_remote_code=True, low_cpu_mem_usage=True, device_map='cuda', use_safetensors=True)
model = model.eval().cuda()

UPLOAD_FOLDER = "./uploads"
RESULTS_FOLDER = "./results"

# for folder in [UPLOAD_FOLDER, RESULTS_FOLDER]:
#     if not os.path.exists(folder):
#         os.makedirs(folder)

# ........................................................................................................

from dotenv import load_dotenv
token = os.environ.get("HF_TOKEN1")

# ........................................................................................................

def run_GOT(image, got_mode, fine_grained_mode="", ocr_color="", ocr_box=""):
    unique_id = str(uuid.uuid4())
    image_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}.png")
    result_path = os.path.join(RESULTS_FOLDER, f"{unique_id}.html")
    
    shutil.copy(image, image_path)
    
    try:
        if got_mode == "plain texts OCR":
            res = model.chat(tokenizer, image_path, ocr_type='ocr')
            return res, None
        elif got_mode == "format texts OCR":
            res = model.chat(tokenizer, image_path, ocr_type='format', render=True, save_render_file=result_path)
        elif got_mode == "plain multi-crop OCR":
            res = model.chat_crop(tokenizer, image_path, ocr_type='ocr')
            return res, None
        elif got_mode == "format multi-crop OCR":
            res = model.chat_crop(tokenizer, image_path, ocr_type='format', render=True, save_render_file=result_path)
        elif got_mode == "plain fine-grained OCR":
            res = model.chat(tokenizer, image_path, ocr_type='ocr', ocr_box=ocr_box, ocr_color=ocr_color)
            return res, None
        elif got_mode == "format fine-grained OCR":
            res = model.chat(tokenizer, image_path, ocr_type='format', ocr_box=ocr_box, ocr_color=ocr_color, render=True, save_render_file=result_path)

        # res_markdown = f"$$ {res} $$"
        res_markdown = res

        if "format" in got_mode and os.path.exists(result_path):
            with open(result_path, 'r') as f:
                html_content = f.read()
            encoded_html = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
            iframe_src = f"data:text/html;base64,{encoded_html}"
            iframe = f'<iframe src="{iframe_src}" width="100%" height="600px"></iframe>'
            download_link = f'<a href="data:text/html;base64,{encoded_html}" download="result_{unique_id}.html">Download Full Result</a>'
            return res_markdown, f"{download_link}<br>{iframe}"
        else:
            return res_markdown, None
    except Exception as e:
        return f"Error: {str(e)}", None
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)