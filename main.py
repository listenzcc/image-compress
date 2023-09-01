"""
File: main.py
Author: Chuncheng Zhang
Date: 2023-09-01
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Performance investigation for image compression.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2023-09-01 ------------------------
# Requirements and constants
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from PIL import Image
from io import BytesIO
from pathlib import Path
from tqdm.auto import tqdm
from rich import print

# %% ---- 2023-09-01 ------------------------
# Function and class


def correct_format(format):
    if format.upper() == 'JPG':
        return 'JPEG'

    return format


def analysis(img, format):
    bytes1 = BytesIO()
    bytes2 = BytesIO()

    img1 = img.convert(mode='RGB')
    img2 = img.convert(mode='P', palette=Image.ADAPTIVE)

    img1.save(bytes1, format=correct_format(format))
    img2.save(bytes2, format='png')

    return img1, img2, bytes1, bytes2


class MyImage(object):
    def __init__(self, path):
        self.path = path
        self.img = Image.open(path)
        self.info = self.analysis()

        if self.info is not None:
            print(self.info)

    def analysis(self):
        img = self.img
        format = self.path.name.split('.')[-1]

        if not format.lower() == 'png':
            return None

        img1, img2, bytes1, bytes2 = analysis(img, format)

        mat = np.array(img1).astype(np.longlong)
        mat = mat[:, :, 0] * 255 * 255 + mat[:, :, 1] * 255 + mat[:, :, 2]
        mat = mat.astype(np.longlong).flatten()

        colors = len(np.unique(mat))
        total = len(mat)

        n1 = len(bytes1.getvalue())
        n2 = len(bytes2.getvalue())

        info = dict(
            name=self.path.name,
            format=format,
            img1=img1,
            img2=img2,
            img1_size=n1,
            img2_size=n2,
            compress_ratio=n2 / n1,
            colors=colors,
            total=total,
        )

        return info


# %% ---- 2023-09-01 ------------------------
# Play ground
files = list(Path(__file__).parent.joinpath('images').iterdir())
print(files)

infos = []
for file in tqdm(files, 'Processing image...'):
    img = MyImage(file)

    if img.info is not None:
        infos.append(img.info)

df = pd.DataFrame(infos)
df

# %% ---- 2023-09-01 ------------------------
# Pending
plt.style.use('seaborn')
fig, ax = plt.subplots(1, 1)

ax.grid(True)
ax.set_title('Compress PNG using P mode')
ax.set_xlabel("Compress ratio")
ax.set_ylabel("Colors")

ax.scatter(df['compress_ratio'], df['colors'])
for i in df.index:
    ax.text(df.loc[i, 'compress_ratio'],
            df.loc[i, 'colors'], df.loc[i, 'name'].split('-')[1])

plt.tight_layout()

plt.show()

# %% ---- 2023-09-01 ------------------------
# Pending

# %%

# %%
# %%
