import scihub


def test_simple():
    urls = [
        "http://dx.doi.org/10.1103/physicsphysiquefizika.1.195",
        "10.1103/physicsphysiquefizika.1.195",
        "http://link.aps.org/article/10.1103/PhysRevB.51.7464",
        "http://link.aps.org/article/10.1103/PhysRevB.62.4927",
        "http://link.aps.org/article/10.1103/PhysRevLett.102.226401",
        "http://link.aps.org/article/10.1103/PhysRev.166.863",
        "http://link.aps.org/article/10.1103/PhysRevB.34.5390",
    ]

    for url in urls:
        res = None
        sh = scihub.SciHub()
        try:
            res = sh.fetch(url)
        except scihub.CaptchaNeededException:
            curl = sh.get_captcha_url()
            assert(curl is not None)
            assert(curl is not '')
            print('catcha' , curl)
        except scihub.DocumentUrlNotFound:
            assert(res is None)
        else:
            assert(res is not None)
            assert(res.get('url') is not None)
            assert(res.get('pdf') is not None)
            with open(url.replace('/', '_'), 'wb+') as fd:
                fd.write(res['pdf'])


if __name__ == "__main__":
    test_simple()
