import chardet
import itertools


def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
    return result["encoding"]


def head(file_path, n=10):
    try:
        with open(file_path, "r", encoding="gb2312") as f:
            lines = [line.strip() for line in itertools.islice(f, n)]
    except:
        with open(
            file_path, "r", encoding=detect_encoding(file_path), errors="ignore"
        ) as f:
            lines = [line.strip() for line in itertools.islice(f, n)]
    return lines
