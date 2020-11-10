from selenium import webdriver
import time


class CricbuzzScrapper:
    def __init__(self, driverPath, cricketer):
        self.driverPath = driverPath
        self.cricketer = cricketer

        self.cricbuzzURL = 'https://www.cricbuzz.com/search?q=' + self.cricketer.lower().replace(' ', '-')
        self.chromeOptions = self.getChromeoptions()
        self.driver = webdriver.Chrome(executable_path=self.driverPath, options=self.chromeOptions)

    @staticmethod
    def getChromeoptions():
        chromeOptions = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chromeOptions.add_argument("--incognito")

        return chromeOptions

    def startScrape(self):
        try:
            player_profile = ""
            self.driver.get(self.cricbuzzURL)
            self.driver.maximize_window()
            time.sleep(2)

            try:
                self.driver.find_element_by_xpath('//div[@class="cb-col-84 cb-col"]/a').click()
                time.sleep(2)
            except Exception as error:
                print('Error while clicking player[cricbuzz] - ', self.cricketer, ' : ', error)

            try:
                player_profile = self.driver.find_element_by_xpath('//div[@class="cb-col cb-col-100 cb-player-bio"]').text
            except Exception as error:
                print('Error while extracting player bio[cricbuzz] - ', self.cricketer, ' : ', error)

            try:
                self.driver.quit()
                # return player_profile
            except Exception as error:
                print('Error while closing browser[cricbuzz] - ', error)

            try:
                return player_profile
            except Exception as error:
                print('Error while returning player_bio[cricbuzz] - ', self.cricketer, ' : ', error)
                return player_profile if player_profile != "" else ""

        except Exception as error:
            print('Error while scraping cricketer data[cricbuzz] - ', self.cricketer, ' : ', error)
            return ""


# if __name__ == '__main__':
#     driverPath = r'H:\Ongil\chromedriver\chromedriver1.exe'
#     cricketer = 'MS DHoni'
#     CricbuzzScrapper(driverPath, cricketer)