from pathlib import Path

from fhir.resources.R4B.bundle import Bundle


class XmlBundle:
    """
    Wrapper to handle XML (de)serialization for FHIR bundles

    Args:
        file:   File to read the bundle from
    """

    def __init__(self, bundle: Bundle = None, file: str | Path = None) -> None:
        self.__bundle: Bundle = None

        if bundle:
            self.__bundle = bundle
        elif file:
            if not isinstance(file, Path):
                file = Path(file)

            content = file.read_text()
            self.__bundle = Bundle.parse_raw(content, content_type="text/xml")

    def write(self, file: str | Path) -> None:
        """
        Write the FHIR bundle to XML file
        """
        if not isinstance(file, Path):
            file = Path(file)

        content = self.__bundle.xml(pretty_print=True)
        file.write_text(content)

    @property
    def bundle(self) -> Bundle:
        return self.__bundle
