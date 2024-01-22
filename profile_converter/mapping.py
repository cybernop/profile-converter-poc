from pathlib import Path
import json
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class ProfilesMappings:
    """
    Mappings for multiple profiles
    """

    def __init__(self, mappings_file: str) -> None:
        self.__mappings_file = mappings_file
        self.__mappings: Dict[str, ProfileMapping] = None

        self.__load_mappings()

    def __load_mappings(self):
        try:
            mappings_json = Path(self.__mappings_file).read_text()
            mappings: dict = json.loads(mappings_json)
        except json.JSONDecodeError as e:
            logger.error("could not parse mapping: {}", e)
        else:
            self.__mappings = {
                profile: ProfileMapping(profile, mapping)
                for profile, mapping in mappings.items()
            }

    def mapping(self, source: str):
        """
        Get the mapping for a single profile
        """
        return self.__mappings.get(source)


class ProfileMapping:
    """
    Mapping from one profile to an other profile
    """

    def __init__(self, profile_name: str, mappings: dict) -> None:
        self.__source = profile_name
        self.__target: str = None
        self.__mapping: Dict[str, str] = None
        self.__values: Dict[str, str] = None

        self.__load_information(mappings)

    def __load_information(self, mappings: dict) -> None:
        try:
            self.__target, entries = list(mappings.items())[0]
            self.__mapping = entries.get("mappings", {})
            self.__values = entries.get("values", {})
        except KeyError as e:
            logger.error("could not load profile mapping: {}", e)
            raise AttributeError("malformed mappings", e)

    @property
    def source(self) -> str:
        """
        Source profile for this mapping
        """
        return self.__source

    @property
    def target(self) -> str:
        """
        Target profile for this mapping
        """
        return self.__target

    @property
    def mapping(self) -> Dict[str, str]:
        """
        Mapping entries for each field of the profile

        Provides information which field in the source profile is mapped to
        which field in the target
        """
        return self.__mapping

    @property
    def values(self) -> Dict[str, str]:
        """
        Fixed values for this mapping

        Contains a list of fields in the target profile that should receive a
        fixed value
        """
        return self.__values
