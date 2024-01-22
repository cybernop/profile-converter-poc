from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser()

    parser.add_argument("--mappings", required=True, help="JSON mapping file")

    return parser.parse_args()


if __name__ == "__main__":
    from mapping import ProfilesMappings

    args = get_args()

    profiles_mapping = ProfilesMappings(args.mappings)
