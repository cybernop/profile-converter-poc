from pathlib import Path

from bundle import XmlBundle

from mapping import ProfilesMappings


class ProfileConverter:
    """
    Comvert for profiles
    """

    def __init__(self, mappings: ProfilesMappings) -> None:
        self.__mappings = mappings

    def convert(self, file: Path, output_path: Path) -> None:
        """
        Convert profiles from a XML file using the mappings
        """
        input_bundle = XmlBundle(file)
        output_bundle = self.__convert_helper(input_bundle)
        output_bundle.write(output_path / file.name)

    def __convert_helper(self, bundle: XmlBundle) -> XmlBundle:
        """
        Helper function to handle the actual conversion
        """
        return bundle
