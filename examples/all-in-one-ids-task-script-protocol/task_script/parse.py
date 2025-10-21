from ids.schema import Model


def parse_file(contents: bytes) -> Model:
    """Parses contents of a file"""
    return Model(file=contents.decode("utf-8"))
