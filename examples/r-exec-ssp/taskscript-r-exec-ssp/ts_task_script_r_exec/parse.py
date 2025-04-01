from typing import Dict


def parse_file(contents: bytes) -> Dict[str, str]:
    """Parses contents of a file"""
    return {"file": contents.decode("utf-8")}
