import sys
from pathlib import Path
import re


def import_geometry(path: Path):
    with open(path) as stream:
        parts = [part.strip() for part in re.split(r'-{2,}', stream.read())[4:-2]]
        # print(parts)
        points = []
        points_str = re.split(r'\n', parts[0])
        for line in points_str:
            line = line.strip()
            # print("blbi", line)
            if re.search(r"^\-?\d", line):
                point = re.split(r'\s+', line)
                point = {"y": point[0], "z": point[1]}
                points.append(point)
                # print("blbub", line)
                # print(point)
        # print(points)
        segments = []
        segment_str = re.split(r'\n', parts[1])
        # print(segment_str)
        for line in segment_str:
            line = line.strip()
            if re.search(r"^\d", line):
                segment = re.split(r'\s+', line)
                segment = {"startPointId": int(segment[0])-1, "endPointId": int(segment[1])-1, "thick": segment[2]}
                segments.append(segment)
        # print(segments)
        return {"points": points, "segments": segments}


        # print(parts)


if __name__ == "__main__":
    print(Path.cwd())
    print(sys.argv)
    import_geometry(sys.argv[1])
