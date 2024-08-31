
from convert_json import ConvertToJson


def main():
    file = "test.xlsx"
    temp_file_path = f"./file/{file}"
    converter = ConvertToJson()
    result = converter.convert(file_path=temp_file_path)
    print("result: ", result)



if __name__ == "__main__":
    main()