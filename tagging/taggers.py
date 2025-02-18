# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import datetime

from docker.models.containers import Container

from tagging.docker_runner import DockerRunner
from tagging.git_helper import GitHelper


def _get_program_version(container: Container, program: str) -> str:
    return DockerRunner.run_simple_command(container, cmd=f"{program} --version")


def _get_pip_package_version(container: Container, package: str) -> str:
    PIP_VERSION_PREFIX = "Version: "

    package_info = DockerRunner.run_simple_command(
        container,
        cmd=f"pip show {package}",
        print_result=False,
    )
    version_line = package_info.split("\n")[1]
    assert version_line.startswith(PIP_VERSION_PREFIX)
    return version_line[len(PIP_VERSION_PREFIX) :]


class TaggerInterface:
    """Common interface for all taggers"""

    @staticmethod
    def tag_value(container: Container) -> str:
        raise NotImplementedError


class SHATagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        return GitHelper.commit_hash_tag()


class DateTagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")


class UbuntuVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        os_release = DockerRunner.run_simple_command(
            container,
            "cat /etc/os-release",
        ).split("\n")
        for line in os_release:
            if line.startswith("VERSION_ID"):
                return "ubuntu-" + line.split("=")[1].strip('"')
        raise RuntimeError(f"did not find ubuntu version in: {os_release}")


class PythonVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        return "python-" + _get_program_version(container, "python").split()[1]


class PythonMajorMinorVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        full_version = PythonVersionTagger.tag_value(container)
        return full_version[: full_version.rfind(".")]


class JupyterNotebookVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        return "notebook-" + _get_program_version(container, "jupyter-notebook")


class JupyterLabVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        return "lab-" + _get_program_version(container, "jupyter-lab")


class JupyterHubVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        return "hub-" + _get_program_version(container, "jupyterhub")


class RVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        return "r-" + _get_program_version(container, "R").split()[2]


class TensorflowVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        try:
            return "tensorflow-" + _get_pip_package_version(container, "tensorflow")
        except AssertionError:
            return "tensorflow-" + _get_pip_package_version(container, "tensorflow-cpu")


class PytorchVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        return "pytorch-" + _get_pip_package_version(container, "torch").split("+")[0]


class JuliaVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        return "julia-" + _get_program_version(container, "julia").split()[2]


class SparkVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        SPARK_VERSION_LINE_PREFIX = r"   /___/ .__/\_,_/_/ /_/\_\   version"

        spark_version = _get_program_version(container, "spark-submit")
        version_line = next(
            filter(
                lambda line: line.startswith(SPARK_VERSION_LINE_PREFIX),
                spark_version.split("\n"),
            )
        )
        return "spark-" + version_line.split(" ")[-1]


class JavaVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container: Container) -> str:
        return "java-" + _get_program_version(container, "java").split()[1]
