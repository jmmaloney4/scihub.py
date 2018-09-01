import scihub

import requests


def test_exists():

    working = []

    for base in scihub.AVAILABLE_SCIHUB_BASE_URL:
        url = 'https://' + base
        print(url)
        try:
            res = requests.get(url, timeout=0.5, verify=False)
            print(res.status_code)
            if res.status_code == 200:
                working.append(url)
        except:
            pass

    assert(len(working) > 0)
    print('Working urls')
    print(working)


if __name__ == "__main__":
    test_exists()
