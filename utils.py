from tqdm import tqdm
import urllib.request
from typing import Iterable, Sized, TextIO, List, Union


def partitions(iterable: Sized, n: int = 1) -> Iterable:
    l: int = len(iterable)
    p: int = l // n
    for ndx in range(0, l, p):
        yield iterable[ndx : min(ndx + p, l)]


def read_lines(input_file: TextIO, num_lines: int) -> List[str]:
    lines: List[str] = []
    for line in input_file:
        lines.append(line)
        if len(lines) == num_lines:
            return lines
    return lines


def file_iterator(file_path: str, batch_size: int) -> Iterable:
    with open(file_path, "r", encoding="utf8") as input_file:
        lines: List[str] = read_lines(input_file=input_file, num_lines=batch_size)
        while lines:
            yield lines
            lines = read_lines(input_file=input_file, num_lines=batch_size)


class MyProgressBar:
    def __init__(self):
        self.pbar: Union[tqdm, None] = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar = tqdm(total=total_size if total_size else None)

        downloaded: int = block_num * block_size
        self.pbar.update(downloaded)

    def close(self):
        if self.pbar:
            self.pbar.clear()
            self.pbar.close()


def download_file(url: str, output_path: str):
    pbar: MyProgressBar = MyProgressBar()
    try:
        urllib.request.urlretrieve(url, output_path, pbar)
    finally:
        pbar.close()
