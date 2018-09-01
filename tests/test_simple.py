import scihub


def test_simple():
    sh = scihub.SciHub()

    try:
        res = sh.fetch(
            #"http://dx.doi.org/10.1103/physicsphysiquefizika.1.195"
            #"10.1103/physicsphysiquefizika.1.195"
            "http://link.aps.org/article/10.1103/PhysRevB.51.7464"
            # http://link.aps.org/article/10.1103/PhysRevB.62.4927
            # http://link.aps.org/article/10.1103/PhysRevLett.102.226401
            # http://link.aps.org/article/10.1103/PhysRev.166.863
            # http://link.aps.org/article/10.1103/PhysRevB.34.5390
        )
    except scihub.CaptchaNeededException:
        curl = sh.get_captcha_url()
        print(curl)
    else:
        assert(True)
        print(res['url'])
        with open('output.pdf', 'wb+') as fd:
            fd.write(res['pdf'])


if __name__ == "__main__":
    test_simple()
