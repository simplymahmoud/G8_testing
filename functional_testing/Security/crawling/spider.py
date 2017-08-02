from requests import ConnectionError
from client import Client
from threading import Thread
import time

class Spider(Client):

    def __init__(self, baseurl, login, password):
        self.baseurl = baseurl
        self.login = login
        self.password = password

        self.admin_portal_url = baseurl + "/cbgrid"
        self.end_user_portal_url = baseurl + '/g8vdc/#/decks'

        self.queue = set()
        self.crawled = set()
        self.error = set()

        #self.queue.add(self.end_user_portal_url)
        self.queue.add(self.admin_portal_url)
        #get login session
        Client.__init__(self, self.baseurl, self.login, self.password)

    def crawle_page_in_queue(self):
        previous_page = 0
        while True:
            if len(self.queue) == 0:
                break
            else:
                crawling_page_url = self.queue.pop()
                if crawling_page_url in self.crawled:
                    continue
                if '/system/login?user_logoff_=1' in crawling_page_url:
                    continue

            #open new page
            try:
                current_page = self._session.get(crawling_page_url)
            except ConnectionError:
                continue
            else:
                if "login/oauth/authorize" in current_page.url:
                    Client.__init__(self, self.baseurl, self.login, self.password)
                    continue

            #update self.queue
            self.update_queue_with_page_links(current_page.content)

            #update_error_pages
            if current_page.status_code != 200:
                self.error.add((current_page.url, current_page.status_code))
                if current_page.status_code == 502:
                    print previous_page
                    print current_page.url
                    break
            #update self.crawled
            self.crawled.add(current_page.url)
            previous_page = current_page
            print(len(self.queue), len(self.crawled))

        self.create_crawled_file()
        self.create_error_file()

    def create_crawled_file(self):
        file = open('crawled_pages.txt', 'a')
        for url in self.crawled:
            file.write(url)
            file.write('\n')

    def create_error_file(self):
        file = open('error_pages.txt', 'a')
        for url in self.error:
            file.write(str(url))
            file.write('\n')

    def update_queue_with_page_links(self, page):
        links = []
        page_lines = str(page).split('\n')
        for line in page_lines:
            if '<a' in line:
                if 'href' in line:
                    link_temp = line[line.find('href=')+6:]
                    if "'" in link_temp:
                        links.append(link_temp[:link_temp.find("'")])
                    elif '"' in link_temp:
                        links.append(link_temp[:link_temp.find('"')])

        self.remove_wrong_links(links)

    def remove_wrong_links(self,links):
        for link in links:
            link = link.replace(' ','%20')
            if 'greenitglobe.com' in link:
                self.queue.add(link)
            elif '/' in link and 'javascript' not in link:
                new_link = self.baseurl + link
                self.queue.add(new_link)
        return self.queue


