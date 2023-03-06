import itertools
import requests
import string
import argparse


def is_url_exists(url):
    try:
        get = requests.get(url, allow_redirects=False)
        code = get.status_code
        if (code == 404):
            return False
        if (code == 400):
            print(f"{url} --> Bad Request might be server request api")
            return False
        code = int(code / 100)
        match code:
            case 2:
                if any(i in get.text.lower() for i in ["page not found", "ops", "not found", "be found", "404"]):
                    return False
                return True
            case 3:
                print(f"{url} --> Redirected")
                return False
            case 5:
                print(f"{url} --> Server Error")
                return False
            case 4:
                print(f"{url} --> Client error might be secret page")
                return True

    except requests.exceptions.RequestException:
        return False


def main(args):
    for i in range(1, args.length + 1):
        for item in itertools.product(string.ascii_lowercase, repeat=i):
            generated_page = "".join(item)
            url_to_check = f"https://{args.base_url}/{generated_page}"
            if is_url_exists(url=url_to_check):
                print(f"{url_to_check} --> Normal page")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url")
    parser.add_argument("length", type=int)
    args = parser.parse_args()
    main(args)
