from pydantic import BaseModel

from pydanticio import read_records_from_file, write_records_to_file


class User(BaseModel):
    name: str
    age: int


def main(input_path: str, output_path: str) -> None:
    users = read_records_from_file(input_path, User)
    write_records_to_file(output_path, users)


if __name__ == "__main__":
    import sys

    main(sys.argv[1], sys.argv[2])
