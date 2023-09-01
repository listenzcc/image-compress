"""
File: convert.py
Author: Chuncheng Zhang
Date: 2023-08-29
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Convert everything using python

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2023-08-29 ------------------------
# Requirements and constants
import time
import tempfile
import threading

from PIL import Image
from io import BytesIO
from pathlib import Path
from tqdm.auto import tqdm
from zipfile import ZipFile
from rich import print, inspect


# %% ---- 2023-08-29 ------------------------
# Function and class
def zip_to_json(file_obj: tempfile._TemporaryFileWrapper):
    """Convert the zip file into file info array

    Args:
        file_obj (tempfile._TemporaryFileWrapper): The input zip file.

    Returns:
        list: The file info array.
    """
    files = []
    with ZipFile(file_obj.name) as arch:
        for zinfo in arch.infolist():
            files.append(
                {
                    "filename": zinfo.filename,
                    "file_size": zinfo.file_size,
                    "compressed_size": zinfo.compress_size,
                }
            )
    return files


def filename_to_image_format(filename):
    """Convert filename to its image format string

    Args:
        filename (string | Path): The filename to convert.

    Returns:
        string: The format string.
        None refers it is not an image.
    """
    extent_format_table = {
        'png': ('png', 'P'),
        'jpeg': ('jpeg', 'RGB')
    }

    return extent_format_table.get(Path(filename).name.split('.')[-1], None)


def zip_to_images(file_obj: tempfile._TemporaryFileWrapper):
    """Extract the images inside the zip file

    Args:
        file_obj (tempfile._TemporaryFileWrapper): The zip file.

    Returns:
        list: The image list.
    """
    images = []
    with ZipFile(file_obj.name) as arch:
        for zinfo in arch.infolist():
            format = filename_to_image_format(zinfo.filename)
            if format is None:
                continue

            print(f'{zinfo.filename} -> {format}')

            bytes_io = BytesIO(arch.read(zinfo.filename))
            img = Image.open(bytes_io)
            images.append((img, zinfo.filename))
    return images


def zip_to_image_compressed_zip(file_obj: tempfile._TemporaryFileWrapper):
    """Compress the zip file by compressing the images inside.

    Args:
        file_obj (tempfile._TemporaryFileWrapper): The zip file.

    Returns:
        str: The path of the compressed zip file.
    """
    p = Path(file_obj.name)
    output_path = Path(p.parent, 'compressed-' + p.name)

    with ZipFile(output_path, 'w') as new_arch:
        threads = []
        buffer_await = []

        with ZipFile(file_obj.name) as arch:

            for zinfo in tqdm(arch.filelist, 'Compressing...'):
                bytes_io = BytesIO(arch.read(zinfo.filename))

                def _compress(bytes_io, zinfo):
                    pair = filename_to_image_format(zinfo.filename)
                    print(zinfo, pair)
                    try:
                        if pair is None:
                            # The context is not an image, copy it
                            # new_arch.writestr(
                            #     zinfo.filename, bytes_io.getvalue())
                            buffer_await.append(
                                (zinfo.filename, bytes_io.getvalue()))
                        else:
                            format, mode = pair
                            # The context is an image, compress it
                            img = Image.open(bytes_io)
                            img = img.convert(
                                mode, palette=Image.ADAPTIVE, colors=256)
                            new_bytes_io = BytesIO()
                            img.save(new_bytes_io, format, optimize=True)

                            # new_arch.writestr(
                            #     zinfo.filename, new_bytes_io.getvalue())

                            buffer_await.append(
                                (zinfo.filename, new_bytes_io.getvalue()))

                            a = len(bytes_io.getvalue())
                            b = len(new_bytes_io.getvalue())
                            print(
                                f'Compress: {zinfo.filename} {b/a:0.4f} | {a} --> {b}')

                    except Exception as error:
                        import traceback
                        traceback.print_exc()

                # _compress(bytes_io, format, zinfo)
                t = threading.Thread(target=_compress, args=(
                    bytes_io, zinfo), daemon=True)
                threads.append(t)
                t.start()

            # while len(threads) > 0:
            #     threads = [t for t in threads if t.is_alive()]
            #     time.sleep(0.5)
            [t.join() for t in threads]

            for a, b in buffer_await:
                new_arch.writestr(a, b)
                print(f'Wrote {a}')

        print(f'Done writing {output_path}')

    return output_path


def zip_to_image_compressed_zip_single_thread(file_obj: tempfile._TemporaryFileWrapper):
    """Compress the zip file by compressing the images inside.

    Args:
        file_obj (tempfile._TemporaryFileWrapper): The zip file.

    Returns:
        str: The path of the compressed zip file.
    """
    p = Path(file_obj.name)
    output_path = Path(p.parent, 'compressed-' + p.name)

    with ZipFile(output_path, 'w') as new_arch:
        with ZipFile(file_obj.name) as arch:
            for zinfo in tqdm(arch.filelist, 'Compressing...'):
                bytes_io = BytesIO(arch.read(zinfo.filename))

                try:
                    pair = filename_to_image_format(zinfo.filename)
                    print(zinfo, pair)

                    if pair is None:
                        # The context is not an image, copy it
                        new_arch.writestr(zinfo.filename, bytes_io.getvalue())
                    else:
                        format, mode = pair

                        # The context is an image, compress it
                        img = Image.open(bytes_io)
                        img = img.convert(
                            mode, palette=Image.ADAPTIVE, colors=256)
                        new_bytes_io = BytesIO()
                        img.save(new_bytes_io, format, optimize=True)
                        new_arch.writestr(
                            zinfo.filename, new_bytes_io.getvalue())

                        a = len(bytes_io.getvalue())
                        b = len(new_bytes_io.getvalue())
                        print(
                            f'Compress: {b/a:0.4f} | {a} --> {b}')
                except Exception as error:
                    import traceback
                    traceback.print_exc()

    return output_path


# %% ---- 2023-08-29 ------------------------
# Play ground


# %% ---- 2023-08-29 ------------------------
# Pending


# %% ---- 2023-08-29 ------------------------
# Pending
