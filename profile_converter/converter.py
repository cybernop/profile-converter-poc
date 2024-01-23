from pathlib import Path
import re

from fhir.resources.R4B.bundle import Bundle, BundleEntry
from fhir.resources.R4B.domainresource import DomainResource

from bundle import XmlBundle
from mapping import ProfilesMappings, ProfileMapping


PROFILE_REGEX = re.compile(r".+\/([\w]+)(\|[\d\.]+)?")


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
        resource = entry.resource

        source_profile = PROFILE_REGEX.search(resource.meta.profile[0]).group(1)
        if mapping := self.__mappings.mapping(source_profile):
            return BundleEntry(resource=_convert_resource(entry.resource, mapping))
        else:
            return None


def _convert_resource(
    resource: DomainResource, mapping: ProfileMapping
) -> DomainResource:
    result_resource = DomainResource(resource_type=resource.resource_type)

    for source, target in mapping.mapping.items():
        pass

    for attribute, value in mapping.values.items():
        pass
    result = _get_resource_attr(resource, "meta.profile")
    _set_resource_attr(resource, "meta.profile", result + "/5")
    _set_resource_attr(resource, "meta.id", "5")
    pass


def _get_resource_attr(resource, path):
    """
    Iterate through the 'dots' of the path the get to the last element of the
    provided path

    TODO: handle lists along the path
    """
    res = resource[0] if isinstance(resource, list) else resource
    if "." in path:
        element, rest_path = path.split(".", 1)
        return _get_resource_attr(getattr(res, element), rest_path)
    else:
        attr = getattr(res, path)
        return attr[0] if isinstance(attr, list) else attr


def _set_resource_attr(resource, path, value):
    """
    Iterate through the 'dots' of the path until we reach the end of the path.
    There we set the value and return the resource. During the walk we make
    sure to leave the rest of the tree intact.

    TODO: handle lists along the path
    """
    res_is_list = isinstance(resource, list)
    if "." in path:
        element, rest_path = path.split(".", 1)
        attr = getattr(resource[0] if res_is_list else resource, element)
        _set_resource_attr(attr, rest_path, value)
        setattr(resource[0] if res_is_list else resource, element, attr)
    else:
        attr_is_list = isinstance(
            getattr(resource[0] if res_is_list else resource, path), list
        )
        val = [value] if attr_is_list else value
        setattr(resource[0] if res_is_list else resource, path, val)
    return resource
