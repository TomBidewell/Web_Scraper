from bs4 import BeautifulSoup
import requests
import csv
import datetime


class AccRaceData:

    def __init__(self, url):
        self.url = url
    
    def scrape_website(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        row_content = list()
        results = soup.find_all("tr", class_ = "rp-horseTable__commentRow")
        for result in results:
            summary = result.find("td").text.replace('\n', '')
            row_content.append(list([summary]))

        return ([tuple((j,i)) for i, j in enumerate(row_content, 1)])

    def write_to_csv(self):
        with open("data_tester.csv", 'w', newline = '') as f:
            write = csv.writer(f)
            write.writerow(["Summaries"])
            write.writerows(self.scrape_website())

    def add_to_csv(self):
        with open("data_tester.csv", 'a', newline = '') as f:
            write = csv.writer(f)
            write.writerows(self.scrape_website())



class LocactionUrls:

    def __init__(self, url):
        self.url = url
    
    def get_place_urls(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all("a", href = True, class_ = 'ui-link ui-link_table rp-raceCourse__panel__race__info__title__link js-popupLink')
        return results

    def first_add_data_to_csv(self):
        urls = self.get_place_urls()
        AccRaceData('https://racingpost.com' + urls[0]['href']).write_to_csv()

        for a in urls[1:]:
            AccRaceData('https://racingpost.com' + a['href']).add_to_csv()
    
    def continue_to_add_data_to_csv(self):
        urls = self.get_place_urls()
        for a in urls:
            AccRaceData('https://racingpost.com' + a['href']).add_to_csv()


url = "https://www.racingpost.com/results"

start_date = datetime.date(year = 2022, month = 12, day = 31)
end_date = datetime.date(year = 2023, month = 1, day = 28)



url_dated_first = url + str("/") + str(start_date)
LocactionUrls(url_dated_first).first_add_data_to_csv()

current_date = start_date + datetime.timedelta(days=1)

while current_date <= end_date:
    url_dated = url + str("/") + str(current_date)
    LocactionUrls(url_dated).continue_to_add_data_to_csv()
    current_date += datetime.timedelta(days=1)
    



