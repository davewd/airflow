__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"


class MarkDownGenerator:
    def __init__(self) -> None:
        return None

    def generate_markdown_table(self):
        return ""


class ApplicationDefinition(MarkDownGenerator):
    def __init__(self, name: str) -> None:
        self.name = name

    def generate_documentation(self) -> List[str]:
        """
        Generate documentation for the application.

        This function generates a list of strings, where each string represents a
        section of the documentation. The sections are ordered in a specific way,
        and each section contains relevant information about the application.

        Parameters:
        None

        Returns:
        List[str]: A list of strings representing the documentation sections.
        """
        return []

    def generate_markdown_documentation(self):
        return ""

    def generate_html_documentation(self):
        return ""


class Service:
    def __init__(self, name=str) -> None:
        self.name = name


class ServiceDefinition(MarkDownGenerator):
    def __init__(self, service_id: str) -> None:
        self.service_id = service_id
