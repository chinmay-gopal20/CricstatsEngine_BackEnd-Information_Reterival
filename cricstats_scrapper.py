from selenium import webdriver

from cricbuzz_scrapper import CricbuzzScrapper
import json
import time
import pandas as pd
import pprint


class StatsScrapper:
    def __init__(self, url, driverPath, cricketers, outputPath):
        self.url = url
        self.driverPath = driverPath
        self.cricketers = cricketers
        self.outputPath = outputPath

        self.chromeOptions = self.getChromeoptions()
        self.driver = webdriver.Chrome(executable_path=self.driverPath, options=self.chromeOptions)

        self.startScrape()

    @staticmethod
    def getChromeoptions():
        chromeOptions = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chromeOptions.add_argument("--incognito")

        return chromeOptions

    # scroll down
    def scrollAndClick(self):
        y = 700
        for timer in range(0, 3):
            # self.driver.find_element_by_class_name('panel-body')\
            #     .find_element_by_xpath('//li[@role="presentation"]/a').click()
            self.driver.execute_script("window.scrollTo(0, " + str(y) + ")")
            y += 700
            time.sleep(1)

    # returns batting stats as json
    def getBattingStats(self, data, format):
        batting_stats = {}

        batting_table_body = data \
            .find_elements_by_xpath(
                '//div[@class="panel-body"]/div//div[@id="' + format + '-Batting"]'
                '//div[@class="table-responsive well"]/table/tbody/tr'
        )
        batting_overall_stat = data \
            .find_elements_by_xpath(
                '//div[@class="panel-body"]/div//div[@id="' + format + '' + '-Batting"]'
                '//div[@class="table-responsive well"]/table/tfoot/tr'
        )
        headers = ['year', 'innings', 'runs', 'balls', 'outs', 'avg', 'sr', 'hs',
                   '50s', '100s', '4s', '6s', 'dot_percent']

        # each year  batting stat
        for each_row in batting_table_body:
            batting_year_wise_stat = {}
            count = 0
            year = 0
            for each_col in list(each_row.get_attribute('innerText').split('\t')):
                if count == 0:
                    year = each_col
                    count += 1
                    continue
                batting_year_wise_stat[headers[count]] = each_col
                count += 1
            batting_stats[year] = batting_year_wise_stat

        # over all batting stat
        for each_row_overall in batting_overall_stat:
            batting_overall_stat_json = {}
            count = 0
            for each_col_overall in list(each_row_overall.get_attribute('innerText').split('\t')):
                if count == 0:
                    count += 1
                    continue
                batting_overall_stat_json[headers[count]] = each_col_overall
                count += 1
            batting_stats['overall'] = batting_overall_stat_json

        return batting_stats

    # returns bowling stats as json
    def getBowlingStats(self, data, format):
        bowling_stats = {}

        bowling_table_body = data \
            .find_elements_by_xpath(
                '//div[@class="panel-body"]/div//div[@id="' + format + '-Bowling"]'
                '//div[@class="table-responsive well"]/table/tbody/tr'
        )
        bowling_overall_stat = data \
            .find_elements_by_xpath(
                '//div[@class="panel-body"]/div//div[@id="' + format + '' + '-Bowling"]'
                '//div[@class="table-responsive well"]/table/tfoot/tr/td'
        )
        headers = ['year', 'innings', 'overs', 'runs', 'wickets', 'eco', 'avg', 'sr', '5w', 'bbi']

        # each year bowling stat
        for each_row in bowling_table_body:
            bowling_year_wise_stat = {}
            count = 0
            year = 0
            for each_col in list(each_row.get_attribute('innerText').strip().split('  ')):
                if count == 0:
                    year = each_col
                    count += 1
                    continue
                bowling_year_wise_stat[headers[count]] = each_col
                count += 1
            bowling_stats[year] = bowling_year_wise_stat

        # over all bowling stat
        count = 0
        bowling_overall_stat_json = {}
        for each_overall in bowling_overall_stat:
            if count == 0:
                count += 1
                continue
            bowling_overall_stat_json[headers[count]] = each_overall.get_attribute('innerText')
            count += 1
        bowling_stats['overall'] = bowling_overall_stat_json

        return bowling_stats

    # save data as json file
    def saveJson(self, data, filename):
        out_file = open(self.outputPath + filename, "w")
        json.dump(data, out_file)
        out_file.close()

    # get player profile from cricbuzz
    def getPlayerProfile(self, cricketer):
        cricbuzzScrapper = CricbuzzScrapper(self.driverPath, cricketer)
        return cricbuzzScrapper.startScrape()

    # main function
    def startScrape(self):
        try:
            self.driver.get(self.url)
            self.driver.maximize_window()
            time.sleep(2)

            # all_player_stats = []
            for each_cricketer in self.cricketers:
                print(each_cricketer)
                cricketer = each_cricketer[0]
                cricketing_nation = each_cricketer[1]
                player_stats = {}

                # Enter player name in search box and click submit
                try:
                    enter_cricketer_name = self.driver.find_element_by_id("q")
                    enter_cricketer_name.clear()
                    enter_cricketer_name.send_keys(cricketer)
                    self.driver.find_element_by_xpath('//form[@method="get"]/input[@type="submit"]').click()
                    time.sleep(2)
                except Exception as error:
                    print('Error - ', error)
                    print('Not able to search player - ', cricketer, '.')
                    continue

                # Click the player appears in search results
                try:
                    results = self.driver.find_element_by_xpath('//div[@class="panel-body"]/a')
                    if results.text.lower() == cricketer.lower():
                        results.click()
                        time.sleep(2)
                except Exception as error:
                    print('Error - ', error)
                    print('Player not found - ', cricketer, '.')
                    continue

                # Find the elements
                try:
                    player_data = self.driver.find_elements_by_xpath('//div[@class="col-lg-8"]/div')
                except Exception as error:
                    print('Error while fetching player stats - ', error)
                    continue

                # self.scrollAndClick()

                format_stats = {}
                # scrape data, exclude last(Ad) element
                for data_iter in range(len(player_data)-1):
                    try:
                        # first element is bio-data
                        if data_iter == 0:
                            player_stats['name'] = \
                                player_data[data_iter].find_element_by_class_name('panel-heading').text
                            player_stats['cricketing_nation'] = cricketing_nation
                            player_bio_list = \
                                player_data[data_iter].find_element_by_class_name('panel-body').text.split('\n')
                            for each_info in player_bio_list:
                                if 'Bats/Bowls' in each_info:
                                    keys = each_info.split(':')[0]
                                    values = each_info.split(':')[1]
                                    player_stats[keys.split('/')[0].lower()] = values.split('/')[0]
                                    player_stats[keys.split('/')[1].lower()] = values.split('/')[1]
                                else:
                                    key = each_info.split(':')[0].lower().replace(' ', '_')
                                    value = each_info.split(':')[1]
                                    player_stats[key] = value

                        # rest elements are stats
                        else:
                            format = player_data[data_iter].find_element_by_class_name('panel-heading').text
                            each_format_stat = {
                                'teams_played_for': player_data[data_iter]
                                                    .find_element_by_class_name('panel-body').text.split('\n')[0]
                                                    .replace('Teams played for: ', ''),
                                'batting': self.getBattingStats(player_data[data_iter],
                                                                format.capitalize() if format == 'TEST' else format),
                                'bowling': self.getBowlingStats(player_data[data_iter],
                                                                format.capitalize() if format == 'TEST' else format)
                            }
                            format_stats[format.lower()] = each_format_stat

                        player_stats['stats'] = format_stats

                    except Exception as error:
                        print('Error while scraping bio for player - ', cricketer, ' - ', error)
                        continue

                try:
                    player_stats['profile'] = self.getPlayerProfile(cricketer)
                except Exception as error:
                    print('Error while getting player profile - ', cricketer, ' : ', error)
                    player_stats['profile'] = ""

                # save each player data as json
                try:
                    self.saveJson(player_stats, cricketer.replace(' ', '_').lower() + '.json')
                except Exception as error:
                    print('Error while adding player stat to master list - ', cricketer, ' - ', error)

                # go back to prev page
                try:
                    self.driver.back()
                    time.sleep(2)
                except Exception as error:
                    print('Error while going to previous page - ', error)

            try:
                # pprint.pprint(all_player_stats)
                # self.saveJson(all_player_stats)
                self.driver.quit()
            except Exception as error:
                print('Error while closing browser - ', error)
                try:
                    self.driver.quit()
                except:
                    pass

        except Exception as error:
            print('Error while accessing cricketers list - ', error)


if __name__ == "__main__":
    url = 'http://www.cricmetric.com/index.py'
    driverPath = r'H:\Ongil\chromedriver\chromedriver1.exe'
    outputPath = 'H:/edu/sem IX/IR/package/cricstats_engine/data/'
    cricketers = pd.read_csv('players.csv').values.tolist()
    print(cricketers)
    service = StatsScrapper(url, driverPath, cricketers, outputPath)

