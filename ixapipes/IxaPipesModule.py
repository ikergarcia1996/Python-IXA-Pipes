from abc import abstractmethod
import os
import signal
from ixapipes.utils import download_file
import threading
import subprocess
from typing import Callable
from shlex import quote
import time


class IxaPipesModule:
    language: str
    server_port: int
    _executable_path: str
    stop_server: threading.Event
    server_thread: threading.Thread
    server_port: int

    @abstractmethod
    def __init__(
        self,
        language,
        server_port,
        executable_path,
        wget_url,
        run_server_function: Callable,
        output_format: str = "naf",
    ):

        self._executable_path = executable_path

        if not os.path.exists(self._executable_path):
            print(
                f"Executable not found, we will download it to: {self._executable_path}"
            )

            download_file(url=wget_url, output_path=self._executable_path)

        self.language = language
        self.server_port = server_port

        self.output_format = output_format

        self.stop_server: threading.Event = threading.Event()

        self.server_thread: threading.Thread = threading.Thread(
            target=run_server_function, args=[]
        )

        self.server_thread.daemon = True
        self.server_thread.start()

        time.sleep(1.0)  # wait for server to start

    @abstractmethod
    def _get_command(self):
        """To Override"""
        pass

    def _run_server(self, *args):
        self.server = subprocess.Popen(
            self._get_command(),
            stdout=subprocess.PIPE,
            shell=True,
            preexec_fn=os.setsid,
        )

    def close(self):
        os.killpg(os.getpgid(self.server.pid), signal.SIGTERM)
        print(f"Server closed")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _run_text(self, text: str, output_path: str = None):
        command: str = (
            f"echo {quote(text)} | "
            f"java -jar {quote(self._executable_path)} client -p {quote(str(self.server_port))}"
        )

        if output_path:
            command += f" > {quote(output_path)}"

        output = subprocess.check_output(command, shell=True)
        return output.decode("utf8") if not output_path else output_path

    def _run_file(self, file_path, output_path: str = None):
        command: str = (
            f"cat {quote(file_path)} |"
            f" java -jar {quote(self._executable_path)} client -p {quote(str(self.server_port))}"
        )

        if output_path:
            command += f" > {quote(output_path)}"

        output = subprocess.check_output(command, shell=True)
        return output.decode("utf8") if not output_path else output_path

    def __call__(
        self,
        text_list_or_path: str,
        output_path: str = None,
    ):

        if os.path.exists(text_list_or_path):
            # Is a path to a file
            return self._run_file(file_path=text_list_or_path, output_path=output_path)
        else:
            # Is a string
            return self._run_text(text=text_list_or_path, output_path=output_path)
