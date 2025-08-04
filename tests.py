from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content


def test_get_file_content():
    print(get_file_content("calculator", "lorem.txt"))
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


def test_get_files_info():
    print("Result for current directory:")
    print(f"{get_files_info('calculator', '.')}")

    print("Result for 'pkg' directory:")
    print(f"{get_files_info('calculator', 'pkg')}")

    print("Result for '/bin' directory:")
    print(f"{get_files_info('calculator', '/bin')}")

    print("Result for '../' directory:")
    print(f"{get_files_info('calculator', '../')}")


if __name__ == "__main__":
    # test_get_files_info()
    test_get_file_content()
