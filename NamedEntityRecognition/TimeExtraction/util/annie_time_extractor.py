


def read_annie_file():
    file_location = input("enter file location for \"gazette.annie\": ")
    file = open(file_location)
    txt = file.read()

    return txt


def extract_named_entity_dictionary(txt: str, NE_type='OG'):
    lines = txt.split("\n")
    for line in lines:
        if NE_type in line:
            print(line)


def write_to_file_as_NE_dictionary():
    ...


def main():
    txt = read_annie_file()
    NE_type = input("Please enter NE_type.. (\"DT\", \"LC\", \"TI\", \"PS\", \"OG\", ...)")
    extract_named_entity_dictionary(NE_type=NE_type, txt=txt)


if __name__ == "__main__":
    main()
