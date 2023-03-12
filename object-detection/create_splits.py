import argparse
import glob
import os
import random

import numpy as np

from utils import get_module_logger


def split(source, destination):
    """
    Create three splits from the processed records. The files should be moved to new folders in the
    same directory. This folder should be named train, val and test.

    args:
        - source [str]: source data directory, contains the processed tf records
        - destination [str]: destination data directory, contains 3 sub folders: train / val / test
    """
    # TODO: Implement function
    files = os.listdir(source)
    random.shuffle(files)

    import shutil
    from pathlib import Path
    Path(f"{destination}/train").mkdir(exist_ok=True, parents=True)
    Path(f"{destination}/test").mkdir(exist_ok=True, parents=True)
    Path(f"{destination}/val").mkdir(exist_ok=True, parents=True)

    train_len = int(len(files)*0.7)
    val_len = int(len(files)*0.2)

    copy = lambda f, d: shutil.copy(f"{source}/{f}", f"{d}/{f}")
    for i, f in enumerate(files):
        if i < train_len:
            copy(f, f"{destination}/train")
        elif i < train_len + val_len:
            copy(f, f"{destination}/val")
        else:
            copy(f, f"{destination}/test")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split data into training / validation / testing')
    parser.add_argument('--source', required=True,
                        help='source data directory')
    parser.add_argument('--destination', required=True,
                        help='destination data directory')
    args = parser.parse_args()

    logger = get_module_logger(__name__)
    logger.info('Creating splits...')
    split(args.source, args.destination)