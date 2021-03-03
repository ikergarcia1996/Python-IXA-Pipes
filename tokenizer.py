import os
from utils import download_file, partitions, file_iterator
import threading
import subprocess
from typing import List, Union
from shlex import quote
import logging
import datetime
import multiprocessing as mp
from functools import partial


class IxaPipesTokenizer:

    language: str
    server_port: int
    notok: bool
    normalize: str
    untokenizable: str
    outputFormat: str
    offsets: bool
    inputkaf: bool
    hardParagraph: bool
    kafversion: str
    _tokenizer_path: str = os.path.expanduser(
        "~/.cache/python-ixa-pipes/ixa-pipe-tok-2.0.0-exec.jar"
    )
    _wget_url: str = "https://drive.google.com/u/0/uc?id=1FVLapcQq2ZEfcre3SY_cNcBHuQoYKHNe&export=download"

    def __init__(
        self,
        language: str,
        port: int = 8890,
        tokenizer_path: str = None,
        notok: bool = False,
        normalize: str = None,
        untokenizable: str = None,
        outputFormat: str = "naf",
        offsets: bool = False,
        inputkaf: bool = False,
        hardParagraph: bool = False,
        kafversion: str = None,
        num_workers: int = 1,
        line_by_line: bool = False,
    ):

        if tokenizer_path:
            self._tokenizer_path = tokenizer_path

        if not os.path.exists(self._tokenizer_path):
            print(
                f"Tokenizer not found, we will download it to: {self._tokenizer_path}"
            )
            if not os.path.exists(os.path.dirname(self._tokenizer_path)):
                os.makedirs(os.path.dirname(self._tokenizer_path))

            download_file(url=self._wget_url, output_path=self._tokenizer_path)

        self.language = language
        self.server_port = port
        self.notok = notok
        self.normalize = normalize
        self.untokenizable = untokenizable
        self.outputFormat = outputFormat
        self.offsets = offsets
        self.inputkaf = inputkaf
        self.hardParagraph = hardParagraph
        self.kafversion = kafversion
        self.num_workers = num_workers
        self.line_by_line = line_by_line

        self.stop_server: threading.Event = threading.Event()

        self.server_thread: threading.Thread = threading.Thread(
            target=self._run_server, args=[]
        )

        self.server_thread.setDaemon(True)
        self.server_thread.start()

    def _run_server(self):

        options: List[str] = []

        if self.notok:
            options.append("--notok")

        if self.normalize:
            options.append(f"--normalize {quote(self.normalize)}")

        if self.untokenizable:
            options.append(f"--untokenizable {quote(self.untokenizable)}")

        if self.offsets:
            options.append("--offsets")

        if self.inputkaf:
            options.append("--inputkaf")

        if self.hardParagraph:
            options.append("--hardParagraph")

        if self.kafversion:
            options.append(f"--kafversion {quote(self.kafversion)}")

        options.append(f"--outputFormat {quote(self.outputFormat)}")

        print(f"Loading tokenizer from {quote(self._tokenizer_path)}")
        command: str = (
            f"java -jar {quote(self._tokenizer_path)} server "
            f"-l {quote(self.language)} "
            f"-p {quote(self.server_port)} "
            f"{' '.join(options)}"
        )
        os.system(command)

    def close(self):
        self.stop_server.set()
        print(f"Server closed")

    def __call__(
        self,
        input_text: Union[List[str], str],
        split_lines: bool = True,
        output_path: str = None,
    ):
        pass

    def _tokenize_line(self, line: str, output_path: str = None):
        command: str = (
            f"echo {quote(line)} | "
            f"java -jar {quote(self._tokenizer_path)} client -p {quote(self.server_port)}"
        )

        if output_path:
            command += f" > {quote(output_path)}"

        output = subprocess.check_output(command)
        return output

    def _tokenize_lines(self, lines: List[str], output_path: str = None):

        tokenized_lines = [
            self._tokenize_line(line=line, output_path=output_path) for line in lines
        ]
        return tokenized_lines if not output_path else None

    def _tokenize_lines_mp(self, lines: List[str], output_path: str = None):

        with mp.Pool(self.num_workers) as pool:
            tokenized_lines = pool.map(
                self._tokenize_lines, partitions(lines, n=self.num_workers)
            )

        tokenized_lines = [item for sublist in tokenized_lines for item in sublist]

        if output_path:
            with open(output_path, "w+", encoding="utf8") as output_file:
                print("\n".join(tokenized_lines), file=output_file)
        else:
            return tokenized_lines

    def _tokenize_text(self, text: str, output_path: str = None):
        output = self._tokenize_line(text)

        if output_path:
            with open(output_path, "w+", encoding="utf8") as output_file:
                print(output, file=output_file)
        else:
            return output

    def _tokenize_file(self, file_path, output_path: str = None):
        command: str = (
            f"cat {quote(file_path)} |"
            f" java -jar {quote(self._tokenizer_path)} client -p {quote(self.server_port)}"
        )

        if output_path:
            command += f" > {quote(output_path)}"

        output = subprocess.check_output(command)
        return output

    def _tokenize_file_lines(
        self, file_path: str, batch_size: int = 1024, output_path: str = None
    ):
        if self.num_workers == 1:
            tokenized_lines_batch = []
            for lines in file_iterator(file_path=file_path, batch_size=batch_size):
                tokenized_lines_batch = self._tokenize_lines(
                    lines=lines, output_path=output_path
                )
                if output_path:
                    pass
