
import scrapy
import json
import datetime
import pandas as pd 
import pymongo
from scrapy.crawler import CrawlerProcess
from scrapy.http.request.json_request import JsonRequest
from pprint import pprint
import requests
import time


class ScrapeDrSmile(scrapy.Spider):
    
    name = "ART"
    start_urls = ['https://www.artsy.net/artists']
    artists_information = []    

    def parse(self,response):
        i = 1
        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

        for alp in alphabet:
            for i in range(100):
                data={"id":"ArtistsByLetterQuery","query":"query ArtistsByLetterQuery(\n  $letter: String!\n  $size: Int\n  $page: Int\n) {\n  viewer {\n    ...ArtistsByLetter_viewer_qU0ud\n  }\n}\n\nfragment ArtistsByLetter_viewer_qU0ud on Viewer {\n  artistsConnection(letter: $letter, page: $page, size: $size) {\n    pageInfo {\n      endCursor\n      hasNextPage\n    }\n    pageCursors {\n      ...Pagination_pageCursors\n    }\n    artists: edges {\n      artist: node {\n        internalID\n        name\n        href\n        id\n      }\n    }\n  }\n}\n\nfragment Pagination_pageCursors on PageCursors {\n  around {\n    cursor\n    page\n    isCurrent\n  }\n  first {\n    cursor\n    page\n    isCurrent\n  }\n  last {\n    cursor\n    page\n    isCurrent\n  }\n  previous {\n    cursor\n    page\n  }\n}\n","variables":{"letter":alp,"size":100,"page":i}}
                try:
                    yield JsonRequest(
                                url="https://metaphysics-production.artsy.net/v2",
                                method='POST',
                                callback = self.reservation,
                                body=json.dumps(data),
                                )
                    time.sleep(5)
                except Exception:
                    continue

    def reservation(self,response) :    

        all_data = json.loads(response.text)["data"]["viewer"]["artistsConnection"]["artists"]
        for data in all_data:
            self.artists_information.append(data["artist"])
        
        print(self.artists_information)

process = CrawlerProcess()
process.crawl(ScrapeDrSmile)
process.start()
