from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser()

    parser.add_argument("--mappings", required=True, help="JSON mapping file")

    return parser.parse_args()


if __name__ == "__main__":
    from pathlib import Path

    from converter import ProfileConverter
    from mapping import ProfilesMappings

    args = get_args()

    profiles_mapping = ProfilesMappings(args.mappings)

    input_path = Path("in")
    output_path = Path("out")

    converter = ProfileConverter(profiles_mapping)
    for input_file in input_path.glob("*.xml"):
        converter.convert(input_file, output_path)
