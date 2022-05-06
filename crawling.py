from selenium import webdriver
import constants as const
import re

class Naver_scrapping(webdriver.Chrome):
    def __init__(self, driver_path = "/Users/hyojin/chromedriver", teardown=False):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('start-maximized')
        super(Naver_scrapping, self).__init__(options=options, executable_path=driver_path)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
    def land_page(self):
        self.get(const.MOVIE_URL)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
    def get_number_of_movies(self):
        movies = self.find_elements_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li/dl/dt/a')
        num = len(movies)
        return num
    def get_movie_information(self):
        opt1 = "([ ])"
        opt2 = "([ㄱ-힣 ])"
        infos = []
        i=1
        while(1):
            info = []
            #Title
            try:
                info.append(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i)+']/dl/dt/a').text)
            except:
                info.append('null')
            #Movie Rate
            try:
                info.append(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i)+']/dl/dt/span').text)
            except:
                info.append('null')
            #Netizen Score
            try:
                info.append(float(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i)+']/dl/dd[1]/dl/dd[1]/div/a/span[2]').text))
            except:
                info.append('null')
            #Netizen Count
            try:
                info.append(int(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i)+']/dl/dd[1]/dl/dd[1]/div/a/span[3]/em').text))
            except:
                info.append(0)
            #Journalist Score
            try:
                info.append(float(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i)+']/dl/dd[1]/dl/dd[2]/div/a/span[2]').text))
            except:
                info.append(0)
            #Journalist Count
            try:
                info.append(int(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i)+']/dl/dd[1]/dl/dd[2]/div/a/span[3]/em').text))
            except:
                info.append(0)
            #Scope, Playing Time, Opening Date
            spo = self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i)+']/dl/dd[2]/dl/dd[1]').text.split('|')
            #Scope
            try:
                info.append(re.sub(opt1, "", spo[0]))
            except:
                info.append('null')
            #Playing Time
            try:
                info.append(re.sub(opt2, "", spo[1]))
            except:
                info.append('null')
            #Opening Date
            try:
                info.append(re.sub(opt2, "", spo[2]).replace(".","-"))
            except:
                info.append('null')
            #Director
            try:
                info.append(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i)+']/dl/dd[2]/dl/dd[2]/span/a').text)
            except:
                info.append('null')
            #Image URL
            try:
                info.append(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i)+']/div/a/img').get_attribute('src'))
            except:
                info.append('null')
            infos.append(info)
            i+=1
            if(i>self.get_number_of_movies()):
                break
        return infos
if __name__ == '__main__':
    nv_movie = Naver_scrapping()
    nv_movie.land_page()
    result = nv_movie.get_movie_information()
    print("\n\n")
    print(result)
    print("\n\n")
    print(len(result))


