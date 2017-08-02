from spider import Spider
from threading import Thread

DOMAIN = "https://du-conv-2.demo.greenitglobe.com"
USERNAME = 'gig'
PASSWORD = 'KrOe6gE9K5nCQdmretfXnj'
THREADS_NUMBER = 10

def target():
    spider = Spider(DOMAIN, USERNAME, PASSWORD)
    spider.crawle_page_in_queue()

for _ in range(THREADS_NUMBER):
    t = Thread(target=target)
    t.start()
