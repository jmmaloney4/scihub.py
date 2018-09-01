# -*- coding: utf-8 -*-

import argparse
import hashlib
import logging
import os

import requests
from bs4 import BeautifulSoup
from retrying import retry

# log config
logging.basicConfig()
logger = logging.getLogger('scihub.py')
logger.setLevel(logging.DEBUG)

# constants
HEADERS = {
    # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0)'
                  # ' Gecko/20100101 Firefox/27.0'
}
AVAILABLE_SCIHUB_BASE_URL = [
    "sci-hub.tw",
    "sci-hub.is",
    "sci-hub.sci-hub.tw",
    "sci-hub.mn",
    "80.82.77.84",
    "80.82.77.83",
    "sci-hub.la",
    "sci-hub.io",
    "sci-hub.hk",
    "sci-hub.bz",
    "tree.sci-hub.la",
    "sci-hub.ws",
    "sci-hub.tv",
    "sci-hub.sci-hub.tv",
    "sci-hub.sci-hub.mn",
    "sci-hub.sci-hub.hk",
    "sci-hub.name",
    "sci-hub.cc",
    "www.sci-hub.cn",
    "sci-hub.biz",
    "sci-hub.ac",
]


class SciHub(object):
    """
    SciHub class can fetch/download papers from sci-hub.io
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = HEADERS
        self.available_base_url_list = AVAILABLE_SCIHUB_BASE_URL
        self.base_url = 'https://' + self.available_base_url_list[0] + '/'
        self.captcha_url = None

    def set_proxy(self, proxy):
        '''
        Set proxy for session.
        Proxy format like socks5://user:pass@host:port
        '''
        self.session.proxies = {
            "http": proxy,
            "https": proxy,
        }

    def _change_base_url(self):
        del self.available_base_url_list[0]

        if len(self.available_base_url_list) == 0:
            raise Exception("No more scihub urls available, none are working")

        self.base_url = 'https://' + self.available_base_url_list[0] + '/'
        logger.info(
            "I'm changing to {0}".format(self.available_base_url_list[0])
        )

    @retry(wait_random_min=100, wait_random_max=1000, stop_max_attempt_number=3)
    def fetch(self, identifier):
        """
        Fetches the paper by first retrieving the direct link to the pdf.
        If the indentifier is a DOI, PMID, or URL pay-wall, then use Sci-Hub
        to access and download paper. Otherwise, just download paper directly.
        """
        logger.info('Downloading with {0}'.format(self.base_url))
        url = self._get_direct_url(identifier)
        logger.info('\t  {0}'.format(url))

        try:
            # verify=False is dangerous but sci-hub.io
            # requires intermediate certificates to verify
            # and requests doesn't know how to download them.
            # as a hacky fix, you can add them to your store
            # and verifying would work. will fix this later.
            res = self.session.get(url, verify=False)

            if res.headers['Content-Type'] != 'application/pdf':
                self._set_captcha_url(url)
                self._change_base_url()
                logger.error('CAPTCHA needed')
                raise CaptchaNeededException(
                    'Failed to fetch pdf with identifier {0}'
                    '(resolved url {1}) due to captcha'.format(identifier, url)
                )
            else:
                return {
                    'pdf': res.content,
                    'url': url
                }

        except requests.exceptions.ConnectionError:
            logger.error(
                '{0} cannot acess,changing'.format(
                    self.available_base_url_list[0]
                )
            )
            self._change_base_url()

        except requests.exceptions.RequestException as e:
            return dict(
                err='Failed to fetch pdf with identifier %s '
                    '(resolved url %s) due to request exception.' % (
                        identifier, url
                    )
            )


    def _set_captcha_url(self, url):
        self.captcha_url = url

    def get_captcha_url(self):
        return self.captcha_url

    def _get_direct_url(self, identifier):
        """
        Finds the direct source url for a given identifier.
        """
        id_type = self._classify(identifier)
        logger.debug('id_type = {0}'.format(id_type))

        return identifier if id_type == 'url-direct' \
            else self._search_direct_url(identifier)

    def _search_direct_url(self, identifier):
        """
        Sci-Hub embeds papers in an iframe. This function finds the actual
        source url which looks something like

            https://moscow.sci-hub.io/.../....pdf.
        """
        url = self.base_url + identifier
        logger.info('scihub url {0}'.format(url))
        res = self.session.get(url, verify=False)
        logger.info('Scraping scihub site')
        s = BeautifulSoup(res.content, 'html.parser')
        iframe = s.find('iframe')
        if iframe:
            return iframe.get('src') if not iframe.get('src').startswith('//') \
                else 'https:' + iframe.get('src')

    def _classify(self, identifier):
        """
        Classify the type of identifier:
        url-direct - openly accessible paper
        url-non-direct - pay-walled paper
        pmid - PubMed ID
        doi - digital object identifier
        """
        if (identifier.startswith('http') or identifier.startswith('https')):
            if identifier.endswith('pdf'):
                return 'url-direct'
            else:
                return 'url-non-direct'
        elif identifier.isdigit():
            return 'pmid'
        else:
            return 'doi'


class CaptchaNeededException(Exception):
    pass
