"""
File: gradio-compress-docx-2.py
Author: Chuncheng Zhang
Date: 2023-08-29
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    The web interface with gradio in block design.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2023-08-29 ------------------------
# Requirements and constants
from PIL import Image
from io import BytesIO

import shlex
import subprocess
import gradio as gr
import pandas as pd
from pathlib import Path

from PyPDF2 import PdfReader

from util.convert import zip_to_json, zip_to_images, zip_to_image_compressed_zip


# %% ---- 2023-08-29 ------------------------
# Function and class
def callback_1(inp):
    compressed_zip_file = None
    files = []
    images = []
    md = ''

    try:
        files = zip_to_json(inp)
        images = zip_to_images(inp)
        compressed_zip_file = zip_to_image_compressed_zip(inp)

    except Exception as error:
        files.append(dict(error=f'{error}'))

    try:

        if inp.name.endswith('.pdf'):
            print(f'Parse {inp.name} as pdf file')
            reader = PdfReader(inp.name)
            pages = []

            images = []

            for page in reader.pages:
                pages.append(page.extract_text())
                print(page.images)
                for img in page.images:
                    images.append((Image.open(BytesIO(img.data)), img.name))
                    print(f'Image {img.name}')

            md = f'# {Path(inp.name).name}\n' + '\n'.join(pages)

        else:
            print(f'Parse {inp.name} as other format file')
            commands = shlex.split('pandoc -t markdown') + [f'{inp.name}']
            md = subprocess.check_output(commands)
            if isinstance(md, bytes):
                md = md.decode("utf-8")

    except Exception as error:
        md += f'# Can not markdown the input file\n-The error is {error}'

    df = pd.DataFrame(files)

    return compressed_zip_file, images, df, md


# %% ---- 2023-08-29 ------------------------
# Play ground

root = Path(__file__).parent
css = root.joinpath('src/style.css')

launch_kwargs = dict(
    share=True,
    server_name='0.0.0.0',
    server_port=10088
)

with gr.Blocks(css=css) as demo:
    gr.Markdown('The **markdown** block')

    with gr.Row():
        inp = gr.File(file_count='single')
        file_output = gr.File(label='Compressed file')

    gallery_output = gr.Gallery(
        label='Gallery', elem_id='_gradio_gallery_output', object_fit='contain', columns=4)

    markdown_output = gr.Markdown(
        elem_id='_gradio_markdown_output'
    )

    dataframe_output = gr.DataFrame(
        label='Contents', elem_id='_gradio_dataframe_output')

    kwargs = dict(
        fn=callback_1,
        inputs=inp,
        outputs=[file_output, gallery_output,
                 dataframe_output, markdown_output]
    )

    inp.change(**kwargs)

    demo.launch(**launch_kwargs)

# %% ---- 2023-08-29 ------------------------
# Pending


# %% ---- 2023-08-29 ------------------------
# Pending
