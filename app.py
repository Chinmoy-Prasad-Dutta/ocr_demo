import io
import os
import time
import base64
# import spaces
import gradio as gr
from pathlib import Path
from transformers import AutoModel, AutoTokenizer


# ........................................................................................................


from utils.processimage import run_GOT


UPLOAD_FOLDER = "./uploads"
RESULTS_FOLDER = "./results"

for folder in [UPLOAD_FOLDER, RESULTS_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)
        
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# ........................................................................................................

def task_update(task):
    if "fine-grained" in task:
        return [
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=False),
        ]
    else:
        return [
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
        ]

def fine_grained_update(task):
    if task == "box":
        return [
            gr.update(visible=False, value = ""),
            gr.update(visible=True),
        ]
    elif task == 'color':
        return [
            gr.update(visible=True),
            gr.update(visible=False, value = ""),
        ]

def cleanup_old_files():
    current_time = time.time()
    for folder in [UPLOAD_FOLDER, RESULTS_FOLDER]:
        for file_path in Path(folder).glob('*'):
            if current_time - file_path.stat().st_mtime > 3600:  # 1 hour
                file_path.unlink()
                

title_html = """
<h2> <span class="gradient-text" id="text">General OCR Theory</span><span class="plain-text">Implementation for Demo purposes </span></h2> 
"""

with gr.Blocks() as demo:
    gr.HTML(title_html)
    gr.Markdown("""
    "This is a demo using G.0.T for Optical Character Recognition "
    
    ### Demo Guidelines
    You need to upload your image below and choose one mode of GOT, then click "Submit" to run GOT model. More characters will result in longer wait times.
    - **plain texts OCR & format texts OCR**: The two modes are for the image-level OCR.
    - **plain multi-crop OCR & format multi-crop OCR**: For images with more complex content, you can achieve higher-quality results with these modes.
    - **plain fine-grained OCR & format fine-grained OCR**: In these modes, you can specify fine-grained regions on the input image for more flexible OCR. Fine-grained regions can be coordinates of the box, red color, blue color, or green color.
    - **Warning: Please upload the file .jpeg, .jpg, .png format only. Other Format like PDF, .hvec etc do not work and will result in error.**
    """)
    
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="filepath", label="upload the image in .jpeg, .jpg, .png format only")
            task_dropdown = gr.Dropdown(
                choices=[
                    "plain texts OCR",
                    "format texts OCR",
                    "plain multi-crop OCR",
                    "format multi-crop OCR",
                    "plain fine-grained OCR",
                    "format fine-grained OCR",
                ],
                label="Choose one mode of GOT",
                value="plain texts OCR"
            )
            fine_grained_dropdown = gr.Dropdown(
                choices=["box", "color"],
                label="fine-grained type",
                visible=False
            )
            color_dropdown = gr.Dropdown(
                choices=["red", "green", "blue"],
                label="color list",
                visible=False
            )
            box_input = gr.Textbox(
                label="input box: [x1,y1,x2,y2]",
                placeholder="e.g., [0,0,100,100]",
                visible=False
            )
            submit_button = gr.Button("Submit-Image")
        
        with gr.Column():
            ocr_result = gr.Textbox(label="GOT-OCR output")

    with gr.Column():
        gr.Markdown("**The mathpix result will be automatically rendered here:**")
        html_result = gr.HTML(label="rendered html", show_label=True)


    task_dropdown.change(
        task_update,
        inputs=[task_dropdown],
        outputs=[fine_grained_dropdown, color_dropdown, box_input]
    )
    fine_grained_dropdown.change(
        fine_grained_update,
        inputs=[fine_grained_dropdown],
        outputs=[color_dropdown, box_input]
    )
    
    submit_button.click(
        run_GOT,
        inputs=[image_input, task_dropdown, fine_grained_dropdown, color_dropdown, box_input],
        outputs=[ocr_result, html_result]
    )
    

if __name__ == "__main__":
    cleanup_old_files()
    demo.launch()
