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
    #영화 연도 선택 페이지 이동 & 원하는 링크로 이동
    def land_page(self, link=const.MOVIE_DIRECORY_URL):
        self.get(link)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
        if link==const.MOVIE_DIRECORY_URL:
            self.find_element_by_class_name('tab_type_6').find_element_by_css_selector('#old_content > div.tab_type_6 > ul > li:nth-child(3) > a').click()
            self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
    #해당 연도 영화 목록으로 이동
    def land_directory_of_year(self, year):
        self.find_element_by_class_name('directory_item_other').find_element_by_css_selector('#old_content > table > tbody > tr:nth-child(1) > td:nth-child('+str(2024-year)+') > a').click()
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
    #영화 목록에서 다음 페이지로 이동
    def land_next_page(self):
        self.find_element_by_class_name("pagenavigation").find_element_by_css_selector("#old_content > div.pagenavigation > table > tbody > tr > td.next").click()
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
    def land_next_page_review(self):
        self.find_element_by_xpath('//*[@id="pagerTagAnchor2"]/em').click()
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
    #해당 연도의 각 영화 URL 수집 함수
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
    #해당 연도 데이터 크롤링
    

    #각 테이블에 삽입할 데이터 수집
    def get_movie_information(self, year):
        infos = []
        self.land_directory_of_year(year)
        movie_urls = self.get_movies_in_the_page()
        for i, url in enumerate(movie_urls):
            self.land_page(url)
            movie, jenre, image, video, director, casting, country, review = self.get_movie_info(i)
            infos.append([movie, jenre, image, video, director, casting, country, review])
        return infos
    
    #각 영화 정보 크롤링
    def get_movie_info(self, movie_index):
        movie = [movie_index]
        jenre_s = []
        image_s = []
        video_s = []
        director = [movie_index]
        casting_s = []
        country_s = []
        review_s = []

        # -- movie table --
        #[title, original_title, opening_date, playing_time, domestic_rate, foreign_rate, (cumulative_audience,) subtitle, content, poster_url,
        # audience_rate, journalist_rate, netizen_rate, audience_count, journalist_count, netizen_count]
        #title
        try:
            movie.append(self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.mv_info > h3 > a").text)
        except:
            movie.append(None)
        #original title
        try:
            movie.append(self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.mv_info > strong").get_attribute("title"))
        except:
            movie.append(None)
        #opening_date
        try:
            movie.append((self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4) > a:nth-child(1)").text+self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(4) > a:nth-child(2)").text).replace(".", "-"))
        except:
            movie.append(None)
        #playing_time
        try:
            movie.append(int((self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(3)").text).replace("분", "")))
        except:
            movie.append(None)
        #domestic_rate
        try:
            movie.append(self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a").text)
        except:
            movie.append(None)
        #foreign_rate
        try:
            movie.append(self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a:nth-child(2)").text)
        except:
            movie.append(None)
        #cumulative_audience
        try:
            movie.append(self.find_element_by_xpath('/html/body/div/div[4]/div[3]/div[1]/div[2]/div[1]/dl/dd[5]/div/p/text()'))
        except:
            movie.append(None)
        #subtitle
        try:
            string = ""
            for txt in self.find_elements_by_css_selector("#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div > h5"):
                string = string + txt.text
            if string=="":
                movie.append(None)
            else:
                movie.append(string.replace("\n"," "))
        except:
            movie.append(None)
        #content
        try:
            string = ""
            for txt in self.find_elements_by_css_selector("#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div > p"):
                string = string + txt.text
            if string=="":
                movie.append(None)
            else:
                movie.append(string.replace("\n", " "))
        except:
            movie.append(None)
        #poster_url
        try:
            movie.append(self.find_element_by_css_selector("#content > div.article > div.mv_info_area > div.poster > a > img").get_attribute("src"))
        except:
            movie.append(None)
        #audience_rate
        try:
            movie.append(float(self.find_element_by_xpath('//*[@id="actualPointPersentBasic"]/div/em[1]').text \
                    +   self.find_element_by_xpath('//*[@id="actualPointPersentBasic"]/div/em[2]').text \
                    +   self.find_element_by_xpath('//*[@id="actualPointPersentBasic"]/div/em[3]').text \
                    +   self.find_element_by_xpath('//*[@id="actualPointPersentBasic"]/div/em[4]').text))
        except:
            movie.append(None)
        #journalist_rate
        try:
            movie.append(float(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/div[1]/div[2]/div/a/div/em[1]').text \
                    +   self.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/div[1]/div[2]/div/a/div/em[2]').text \
                    +   self.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/div[1]/div[2]/div/a/div/em[3]').text \
                    +   self.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/div[1]/div[2]/div/a/div/em[4]').text))
        except:
            movie.append(None)

        #netizen_rate
        try:
            movie.append(float(self.find_element_by_xpath('//*[@id="pointNetizenPersentBasic"]/em[1]').text \
                    +   self.find_element_by_xpath('//*[@id="pointNetizenPersentBasic"]/em[2]').text \
                    +   self.find_element_by_xpath('//*[@id="pointNetizenPersentBasic"]/em[3]').text \
                    +   self.find_element_by_xpath('//*[@id="pointNetizenPersentBasic"]/em[4]').text))
        except:
            movie.append(None)
        #audience_count
        self.get(self.current_url.replace("basic", "point"))
        try:
            movie.append(int(self.find_element_by_class_name("grade_audience").find_element_by_css_selector("#actual_point_tab_inner > span > em").text))
        except:
            movie.append(None)
        #journalist_count
        try:
            movie.append(int(self.find_element_by_css_selector("#content > div.article > div.section_group.section_group_frst > div:nth-child(6) > div > div.title_area > span > em").text))
        except:
            movie.append(None)
        #netizen_count
        try:
            movie.append(int(self.find_element_by_class_name("grade_netizen").find_element_by_css_selector("#graph_area > div.grade_netizen > div.title_area.grade_tit > div.sc_area > span > em").text))
        except:
            movie.append(None)
        self.back()

        # -- country table --
        #country
        # [movie_index, country_name]
        try:
            for ctr in self.find_elements_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[1]/p/span[2]/a'):
                country = [movie_index]
                country.append(ctr.text)
                country_s.append(country)
        except:
            country_s.append(None)

        # -- jenre --
        #[movie_index, jenre_type]
        #jenre
        try:
            for jnr in self.find_elements_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[1]/p/span[1]/a'):
                jenre = [movie_index]
                jenre.append(jnr.text)
                jenre_s.append(jenre)
        except:
            jenre_s.append(None)

        # -- image table --
        #image_url
        try:
            for i in range(int(self.find_element_by_css_selector("#_MainPhotoArea > div.title_area > span > em").text)):
                image = [movie_index]
                image.append(self.find_element_by_css_selector("#_MainPhotoArea > div.viewer > div > img").get_attribute("src"))
                image_s.append(image)
                self.find_element_by_css_selector("#_MainPhotoArea > div.viewer > a._NextBtn._NoOutline.pic_next").click()
        except:
            image_s.append(None)

        # -- video table -- 성공 ^_^
        #[movie_index, video_name, video_url]
        #video_name & video_url
        try:
            self.get(self.current_url.replace("basic", "media"))
            num_v = len(self.find_elements_by_css_selector("#content > div.article > div.obj_section2.noline > div > div.ifr_module > div > div > ul > li > p.tx_video.ico > a"))
            for index in range(num_v):
                vd = crawler.find_elements_by_css_selector("#content > div.article > div.obj_section2.noline > div > div.ifr_module > div > div > ul > li > p.tx_video.ico > a")[index]
                video = [movie_index]
                video.append(vd.text)
                vd.click()
                self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
                video.append(self.current_url)
                self.back()
                self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
                video_s.append(video)
            self.back()
            self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
            if video_s==[]:
                video_s.append(None)
        except:
            video_s.append(None)

        # -- casting table --
        #[movie_index, actor_name, actor_original_name, role1, role2]
        try:
            self.get(self.current_url.replace("basic", "detail"))
            self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
            try:
                self.find_element_by_css_selector("#actorMore").click() #펼쳐보기
                self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
            except:
                pass
            
            num_actor = len(self.find_elements_by_css_selector("#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li > div > a"))
            for i in range(num_actor):
                actor_info = [movie_index]
                atr = self.find_elements_by_css_selector("#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li > div > a")[i]
                #actor_name
                actor_info.append(atr.text)
                #actor_original_name
                try:
                    actor_info.append(self.find_element_by_css_selector("#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li:nth-child("+str(i+1)+") > div > em").text)
                except:
                    actor_info.append(None)
                #role1  
                try:
                    actor_info.append(self.find_element_by_css_selector("#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li:nth-child("+str(i+1)+") > div > div > p.in_prt > em").text)
                except:
                    actor_info.append(None)
                #role2
                try:
                    actor_info.append(self.find_element_by_css_selector("#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li:nth-child("+str(i+1)+") > div > div > p.pe_cmt > span").text)
                except:
                    actor_info.append(None)
                casting_s.append(actor_info)
            # self.back()
            # self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
            if casting_s==[]:
                casting_s.append(None)
        except:
            casting_s.append(None)

        # -- director table --
        #director name
        try:
            director.append(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div/div/div[2]/div/a').text)
        except:
            director.append(None)
        #director original name
        try:
            director.append(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div/div/div[2]/div/em').text)
        except:
            director.append(None)


        self.back()
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)

        # -- review table --
        #[movie_index, review_title, review_date, review_content, recommendation]
        self.get(self.current_url.replace("basic", "review"))
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
        #추천 리뷰 상위 10개
        try:
            for i, rev in enumerate(self.find_elements_by_xpath('//*[@id="reviewTab"]/div/div/ul/li/a/strong')):
                review = [movie_index]
                # review title
                review.append(rev.text)
                # reviewer
                review.append(self.find_element_by_xpath('//*[@id="reviewTab"]/div/div/ul/li['+str(i+1)+']/span/a').text)
                # review date
                review.append(self.find_element_by_xpath('//*[@id="reviewTab"]/div/div/ul/li['+str(i+1)+']/span/em[1]').text.replace(".", "-"))
                # review content
                review.append(self.find_element_by_xpath('//*[@id="reviewTab"]/div/div/ul/li['+str(i+1)+']/p/a').text)
                # recommendation
                review.append(int(self.find_element_by_xpath('//*[@id="reviewTab"]/div/div/ul/li['+str(i+1)+']/span/em[2]').text.replace("추천 ", "")))

                review_s.append(review)
            if review_s==[]:
                review_s.append(None)
        except:
            review_s.append(None)
            
        self.back()
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
        
        
        return movie, jenre_s, image_s, video_s, director, casting_s, country_s, review_s


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
    crawler.land_page()

    infos = crawler.get_movie_information(2023)
    # infos = crawler.get_movie_info(10)
    print(infos)

   

    


                
