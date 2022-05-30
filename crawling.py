from selenium import webdriver
import constants as const
import re
import time

class Naver_scrapping(webdriver.Chrome):
    def __init__(self, driver_path = "/Users/hyojin/chromedriver", teardown=False):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('start-maximized')
        super(Naver_scrapping, self).__init__(options=options, executable_path=driver_path)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
    def land_page(self, link=const.MOVIE_DIRECORY_URL):
        self.get(link)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
        if link==const.MOVIE_DIRECORY_URL:
            self.find_element_by_class_name('tab_type_6').find_element_by_css_selector('#old_content > div.tab_type_6 > ul > li:nth-child(3) > a').click()
            self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
    def land_directory_of_year(self, year):
        self.find_element_by_class_name('directory_item_other').find_element_by_css_selector('#old_content > table > tbody > tr:nth-child(1) > td:nth-child('+str(2024-year)+') > a').click()
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
    def land_next_page(self):
        self.find_element_by_class_name("pagenavigation").find_element_by_css_selector("#old_content > div.pagenavigation > table > tbody > tr > td.next").click()
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
    def get_movies_in_the_page(self):
        movie_urls = []
        while True:
            for i in range(20):
                try:
                    movie_urls.append(self.find_element_by_css_selector('#old_content > ul > li:nth-child('+str(i+1)+') > a').get_attribute('href'))
                except:
                    break
            try:
                self.land_next_page()
            except:
                break
        return movie_urls
    def get_movie_information(self, movie_urls):
        infos = []
        for url in movie_urls:
            self.land_page(url)
            infos.append(self.get_movie_info())
        return infos
    def get_movie_info(self):
        info = []
        #2.title
        try:
            info.append(self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.mv_info > h3 > a").text)
        except:
            info.append(None)
        #3.original title
        try:
            info.append(self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.mv_info > strong").get_attribute("title"))
        except:
            info.append(None)
        #4.scope
        try:
            string = ""
            for country in self.find_elements_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[1]/p/span[1]/a'):
                string = string + country.text + " "
            if string=="":
                info.append(None)
            else:
                info.append(string)
        except:
            info.append(None)
        #5.director
        try:
            info.append(self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4) > p > a").text)
        except:
            info.append(None)
        #6.actor
        self.get(self.current_url.replace("basic", "detail"))
        try:
            self.find_element_by_css_selector("#actorMore").click() #펼쳐보기
        except:
            pass
        

        self.back()

        #7.country
        try:
            string = ""
            for country in self.find_elements_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[1]/p/span[2]/a'):
                string = string + country.text + " "
            if string=="":
                info.append(None)
            else:
                info.append(string)
        except:
            info.append(None)
        #8.opening_date
        try:
            info.append(self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4) > a:nth-child(1)").text+self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4) > a:nth-child(2)").text)
        except:
            info.append(None)
        #9.playing_time
        try:
            info.append(self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(3)").text)
        except:
            info.append(None)
        #10.domestic_rate
        try:
            info.append(self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a").text)
        except:
            info.append(None)
        #11.foreign_rate
        try:
            info.append(self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a:nth-child(2)").text)
        except:
            info.append(None)
        #12.description(subtitle & content)
        #subtitle
        try:
            string = ""
            for txt in self.find_elements_by_css_selector("#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div > h5"):
                string = string + txt.text
            if string=="":
                info.append(None)
            else:
                info.append(string)
        except:
            info.append(None)
        #content
        try:
            string = ""
            for txt in self.find_elements_by_css_selector("#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div > p"):
                string = string + txt.text
            if string=="":
                info.append(None)
            else:
                info.append(string)
        except:
            info.append(None)

        #13.audience_rate
        try:
            info.append(self.find_element_by_xpath('//*[@id="actualPointPersentBasic"]/div/em[1]').text \
                    +   self.find_element_by_xpath('//*[@id="actualPointPersentBasic"]/div/em[2]').text \
                    +   self.find_element_by_xpath('//*[@id="actualPointPersentBasic"]/div/em[3]').text \
                    +   self.find_element_by_xpath('//*[@id="actualPointPersentBasic"]/div/em[4]').text)
        except:
            info.append(None)
        #15.journalist_rate
        try:
            info.append(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/div[1]/div[2]/div/a/div/em[1]').text \
                    +   self.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/div[1]/div[2]/div/a/div/em[2]').text \
                    +   self.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/div[1]/div[2]/div/a/div/em[3]').text \
                    +   self.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/div[1]/div[2]/div/a/div/em[4]').text)
        except:
            info.append(None)

        #17.netizen_rate
        try:
            info.append(self.find_element_by_xpath('//*[@id="pointNetizenPersentBasic"]/em[1]').text \
                    +   self.find_element_by_xpath('//*[@id="pointNetizenPersentBasic"]/em[2]').text \
                    +   self.find_element_by_xpath('//*[@id="pointNetizenPersentBasic"]/em[3]').text \
                    +   self.find_element_by_xpath('//*[@id="pointNetizenPersentBasic"]/em[4]').text)
        except:
            info.append(None)

        #count
        self.get(self.current_url.replace("basic", "point"))
        #audience_count
        try:
            info.append(self.find_element_by_class_name("grade_audience").find_element_by_css_selector("#actual_point_tab_inner > span > em").text)
        except:
            info.append(None)
        #journalist_count
        try:
            info.append(self.find_element_by_css_selector("#content > div.article > div.section_group.section_group_frst > div:nth-child(6) > div > div.title_area > span > em").text)
        except:
            info.append(None)
        #netizen_count
        try:
            info.append(self.find_element_by_class_name("grade_netizen").find_element_by_css_selector("#graph_area > div.grade_netizen > div.title_area.grade_tit > div.sc_area > span > em").text)
        except:
            info.append(None)
        self.back()

        #19.poster_url
        try:
            info.append(self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.poster > a > img").get_attribute("src"))
        except:
            info.append(None)
        #20.image_url
        try:
            images = ""
            for i in range(int(self.find_element_by_css_selector("#_MainPhotoArea > div.title_area > span > em").text)):
                images=images+self.find_element_by_css_selector("#_MainPhotoArea > div.viewer > div > img").get_attribute("src") + " "
                self.find_element_by_css_selector("#_MainPhotoArea > div.viewer > a._NextBtn._NoOutline.pic_next").click()
            if images=="":
                info.append(None)
            else:
                info.append(images)
        except:
            info.append(None)
        #21.video_name & video_url
        try:
            vnames = ""
            urls = ""
            for i in range(int(self.find_element_by_css_selector("#content > div.article > div.section_group.section_group_frst > div:nth-child(4) > div > div > span > em").text)):
                xpath = '//*[@id="content"]/div[1]/div[4]/div[4]/div/ul/li['+str(i+1)+']/p/a'
                vnames = vnames + self.find_element_by_xpath(xpath).get_attribute("title") + " "
                self.find_element_by_xpath(xpath).click()
                urls = urls + self.current_url + " "
                self.back()
            if vnames=="":
                info.append(None)
            else:
                info.append(vnames)
            if urls=="":
                info.append(None)
            else:
                info.append(urls)
        except:
            info.append(None)
        




        return info


    def get_actor_information(self):
        pass
    def get_director_information(self):
        pass
    def get_review_data(self):
        pass







    def get_number_of_movies(self):
        movies = self.find_elements_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li/dl/dt/a')
        num = len(movies)
        return num
    def get_movie_information_showing(self):
        opt1 = "([ ])"
        opt2 = "([ㄱ-힣 ])"
        infos = []
        i=1
        max = self.get_number_of_movies()
        while(1):
            info = []
            #Title
            try:
                info.append(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
                    +']/dl/dt/a').text)
            except:
                info.append(None)
            #Movie Rate
            try:
                info.append(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
                    +']/dl/dt/span').text)
            except:
                info.append(None)
            #Netizen Rate
            try:
                rate=float(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
                    +']/dl/dd[1]/dl/dd[1]/div/a/span[2]').text)
                if rate>0:
                    info.append(rate)
                else:
                    info.append(None)
            except:
                info.append(None)
            #Netizen Count
            try:
                info.append(int(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
                    +']/dl/dd[1]/dl/dd[1]/div/a/span[3]/em').text.replace(",","")))
            except:
                info.append(0)
            #Journalist Score
            try:
                info.append(float(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
                    +']/dl/dd[1]/dl/dd[2]/div/a/span[2]').text))
            except:
                info.append(None)
            #Journalist Count
            try:
                info.append(int(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
                    +']/dl/dd[1]/dl/dd[2]/div/a/span[3]/em').text.replace(",","")))
            except:
                info.append(0)
            #Scope, Playing Time, Opening Date
            spo = self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
                +']/dl/dd[2]/dl/dd[1]').text.split('|')
            #Scope
            try:
                info.append(re.sub(opt1, "", spo[0]))
            except:
                info.append(None)
            #Playing Time
            try:
                info.append(re.sub(opt2, "", spo[1]))
            except:
                info.append(None)
            #Opening Date
            try:
                info.append(re.sub(opt2, "", spo[2]).replace(".","-"))
            except:
                info.append(None)
            #Director
            try:
                info.append(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
                    +']/dl/dd[2]/dl/dd[2]/span/a').text)
            except:
                info.append(None)
            #Image URL
            try:
                info.append(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
                    +']/div/a/img').get_attribute('src'))
            except:
                info.append(None)
            infos.append(info)
            i+=1
            if(i>max):
                break
        return infos
if __name__ == '__main__':
    crawler = Naver_scrapping()
    crawler.land_page(const.SAMPLE_URL)
    # crawler.land_directory_of_year(2023)
    # mvs = crawler.get_movies_in_the_page()
    # print(len(mvs))
    # crawler.land_page(mvs[0])
    # print(crawler.get_movie_information(mvs[0]))
    info = crawler.get_movie_info()
    print(info)




    # nv_movie = Naver_scrapping()
    # nv_movie.land_page()
    # result = nv_movie.get_movie_information()
    # print("\n\n")
    # print(result)
    # print("\n\n")
    # print(len(result))


