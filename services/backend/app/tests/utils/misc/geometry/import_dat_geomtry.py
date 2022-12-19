import sys
from pathlib import Path


def import_geometry(path: Path):
    with open(path) as stream:
        print(stream.read())


if __name__ == "__main__":
    print(Path.cwd())
    print(sys.argv)
    import_geometry(sys.argv[1])
