from pathlib import Path

from fhir.resources.R4B.bundle import Bundle, BundleEntry

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
        input_bundle = XmlBundle(file=file)
        output_bundle = self.__convert_helper(input_bundle)
        output_bundle.write(output_path / file.name)

    def __convert_helper(self, bundle: XmlBundle) -> XmlBundle:
        """
        Helper function to handle the actual conversion
        """

        result_bundle = Bundle(type=bundle.bundle.type)

        # Needs to be checked: this is not definied in the mapping
        result_bundle.identifier = bundle.bundle.identifier

        result_bundle.entry = []
        for entry in bundle.bundle.entry:
            result_entry = self.__convert_entry(entry)
            if result_entry:
                result_bundle.entry.append(result_entry)

        return XmlBundle(bundle=result_bundle)

    def __convert_entry(self, entry: BundleEntry) -> BundleEntry | None:
        return BundleEntry(resource=entry.resource)
