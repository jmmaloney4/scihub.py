import scihub


def test_simple():
    sh = scihub.SciHub()

    try:
        res = sh.fetch(
            #"http://dx.doi.org/10.1103/physicsphysiquefizika.1.195"
            "10.1103/physicsphysiquefizika.1.195"
        )
    except scihub.CaptchaNeededException:
        curl = sh.get_captcha_url()
        print(curl)
    else:
        print(res)


if __name__ == "__main__":
    test_simple()
