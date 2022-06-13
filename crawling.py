from selenium import webdriver
import constants as const
import re
import numpy as np
import time
import tqdm
from sql_functions import SQL

class Naver_scrapping(webdriver.Chrome):
    def __init__(self, driver_path = "/Users/hyojin/chromedriver", teardown=False):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('start-maximized')
        super(Naver_scrapping, self).__init__(options=options, executable_path=driver_path)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
    #영화 연도 선택 페이지 이동 & 원하는 링크로 이동
    def land_page(self, link=const.MOVIE_DIRECORY_URL):
        self.get(link)
        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
        if link==const.MOVIE_DIRECORY_URL:
            # self.find_element_by_class_name('tab_type_6').find_element_by_css_selector('#old_content > div.tab_type_6 > ul > li:nth-child(3) > a').click()
            self.find_element_by_xpath('/html/body/div/div[4]/div/div/div/div/div[1]/div[1]/ul/li[3]/a/img').click()
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
    def get_current_url(self):
        return self.current_url
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
    
    def get_movie_table_info(self, movie_code, year):
        movie = [movie_code]
        # -- movie table --
        #[movie_code, title, original_title, opening_date, playing_time, domestic_rate, foreign_rate, (cumulative_audience,) subtitle, content, poster_url,
        # audience_rate, journalist_rate, netizen_rate, audience_count, journalist_count, netizen_count]

        #movie code
        # movie.append(self.get_movie_code())
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
            opening_date = self.find_element_by_class_name("step1").find_element_by_xpath('/html/body/div/div[4]/div[3]/div[1]/div[2]/div[1]/dl/dd[1]/p').text.split(" ")[-3:-1]
            o_date = opening_date[0] + opening_date[1]
            if o_date.count('.')==2:
                movie.append(o_date.replace(".", "-"))
            elif o_date.count('.')==1:
                movie.append(o_date.replace(".", "-")+"-01")
            else:
                movie.append(str(year)+"-01-01")
        except:
            movie.append(None)
        #playing_time
        try:#
            movie.append(int((self.find_element_by_class_name("step1").find_element_by_xpath('/html/body/div/div[4]/div[3]/div[1]/div[2]/div[1]/dl/dd[1]/p/span[3]').text).replace("분", "")))
        except:
            movie.append(None)
        #domestic_rate
        try:#
            movie.append(self.find_element_by_class_name("step4").find_element_by_xpath('/html/body/div/div[4]/div[3]/div[1]/div[2]/div[1]/dl/dd[4]/p/a').text)
        except:
            movie.append(None)
        #foreign_rate
        try:#
            movie.append(self.find_element_by_class_name("step4").find_element_by_xpath('/html/body/div/div[4]/div[3]/div[1]/div[2]/div[1]/dl/dd[4]/p/a[2]').text)
        except:
            movie.append(None)
        #cumulative_audience
        try:
            movie.append(int(self.find_element_by_class_name("step9").find_element_by_xpath('/html/body/div/div[4]/div[3]/div[1]/div[2]/div[1]/dl/dd[5]/div/p').text.split('(')[0].replace("명", "").replace(",", "")))
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

        return movie
    
    def get_movie_code(self, url):
        # url = self.current_url
        print("movie URL: ", url)
        c_url = int(re.sub("([a-z])\w+[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]|(\/\/)", "", url))
        print("movie CODE: ", c_url)
        return c_url
    def get_review_code(self):
        return int(re.sub("([a-z])\w+[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]|(\/\/)|#(\w+)", "", self.current_url.split("&")[0].replace("#", "")))
    def get_actor_table_info(self, movie_code):
        # actor : [actor_name, original_actor_name, actor_code]
        # movie_actor : [movie_code, cast, role, actor_code]
        actor = []
        movie_actor = []    #intersection table

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
                actor_one = []
                movie_actor_one = [movie_code]

                atr = self.find_elements_by_css_selector("#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li > div > a")[i]
                
                #actor_name - actor
                actor_one.append(atr.text)
                #actor_original_name
                try:
                    actor_one.append(self.find_element_by_css_selector("#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li:nth-child("+str(i+1)+") > div > em").text)
                except:
                    actor_one.append(None)
                #cast - movie_actor
                try:
                    movie_actor_one.append(self.find_element_by_css_selector("#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li:nth-child("+str(i+1)+") > div > div > p.in_prt > em").text)
                except:
                    movie_actor_one.append(None)
                #role - movie_actor
                try:
                    movie_actor_one.append(self.find_element_by_css_selector("#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li:nth-child("+str(i+1)+") > div > div > p.pe_cmt > span").text)
                except:
                    movie_actor_one.append(None)
                
                atr.click()
                self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
                # actor_code
                actor_one.append(self.get_movie_code(self.current_url))
                movie_actor_one.append(self.get_movie_code(self.current_url))

                self.back()
                self.implicitly_wait(const.IMPLICIT_WAIT_TIME)

                try:
                    self.find_element_by_css_selector("#actorMore").click() #펼쳐보기
                    self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
                except:
                    pass

                actor.append(actor_one)
                movie_actor.append(movie_actor_one)
            
            self.get(self.current_url.replace("detail", "basic"))
            self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
            return actor, movie_actor
        except:
            return None, None


    def get_director_table_info(self, movie_code):
        # director : [director_name, original_director_name, director_code]
        # movie_actor : [movie_code, director_code]
        director = []
        movie_director = [] #intersection table

        try:
            self.get(self.current_url.replace("basic", "detail"))
            self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
            
            num_director = len(self.find_elements_by_css_selector("#content > div.article > div.section_group.section_group_frst > div:nth-child(2) > div > div > div > a"))
            if num_director == 1:
                director_one = []
                movie_director_one = [movie_code]
                #director name
                d_name = self.find_element_by_css_selector("#content > div.article > div.section_group.section_group_frst > div:nth-child(2) > div > div.dir_obj > div > a")
                director_one.append(d_name.text)
                #director original name
                try:
                    director_one.append(self.find_element_by_css_selector("#content > div.article > div.section_group.section_group_frst > div:nth-child(2) > div > div.dir_obj > div > em").text)
                except:
                    director_one.append(None)

                d_name.click()
                self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
                director_one.append(self.get_movie_code(self.current_url))
                movie_director_one.append(self.get_movie_code(self.current_url))
                self.back()
                self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
                
                director.append(director_one)
                movie_director.append(movie_director_one)
            else:
                for i in range(num_director):
                    director_one = []
                    movie_director_one = [movie_code]
                    #director name
                    d_name = self.find_element_by_css_selector("#content > div.article > div.section_group.section_group_frst > div:nth-child(2) > div > div:nth-child("+str(i+2)+") > div > a")
                    director_one.append(d_name.text)
                    #director original name
                    d_o_name = self.find_element_by_css_selector("#content > div.article > div.section_group.section_group_frst > div:nth-child(2) > div > div:nth-child("+str(i+2)+") > div > em").text
                    if d_o_name == '':
                        director_one.append(None)
                    else:
                        director_one.append(d_o_name)
                    d_name.click()
                    self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
                    director_one.append(self.get_movie_code(self.current_url))
                    movie_director_one.append(self.get_movie_code(self.current_url))
                    self.back()
                    self.implicitly_wait(const.IMPLICIT_WAIT_TIME)

                    director.append(director_one)
                    movie_director.append(movie_director_one)
            return director, movie_director
        except:
            return None, None
    def get_review_table_info(self, movie_code):
        # review : []
        # movie : [movie_code, review_code]
        review = []
        movie_review = []   #intersection table
        review2 = []

        try:
            self.get(self.current_url.replace("basic", "review"))
            self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
            num_review = int(self.find_element_by_xpath('/html/body/div/div[4]/div[3]/div[1]/div[4]/div/div/div/div/div[2]/span/em').text.replace(",",""))
            
            # if num_review%10==0:
            #     num_page = int(num_review/10)
            # else:
            #     num_page = int(num_review/10) + 1
            num_page = int(np.ceil(num_review/10))
            
            # print("start")
            for page in range(1, num_page+1):
                if page == 2:
                    break
                self.find_element_by_xpath('/html/body/div/div[4]/div[3]/div[1]/div[4]/div/div/div/div/div[3]/div/a['+str(page)+']/span').click()
                self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
                # print(page, "페이지")
                for i in range(10):
                    # print(i, "번째")
                    try:
                        review_one = []
                        movie_review_one = [movie_code]
                        
                        #id
                        review_one.append(self.find_element_by_css_selector("#reviewTab > div > div > ul > li:nth-child("+str(i+1)+") > span > a").text)
                        # print("--id")
                        #date
                        try:
                            review_one.append(self.find_element_by_css_selector("#reviewTab > div > div > ul > li:nth-child("+str(i+1)+") > span > em:nth-child(2)").text.replace(".", "-"))
                        except:
                            review_one.append(None)
                        # print("--date")

                        self.find_element_by_css_selector("#reviewTab > div > div > ul > li:nth-child("+str(i+1)+") > a > strong").click()
                        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
                        time.sleep(1)

                        r_code = self.get_review_code()
                        # print(r_code, "리뷰 코드")
                        review_one.append(r_code)
                        movie_review_one.append(r_code)
                        
                        #title
                        try:
                            review_one.append(self.find_element_by_css_selector("#content > div.article > div.obj_section.noline.center_obj > div.review > div.top_behavior > strong").text)
                        except:
                            review_one.append(None)
                        # print("--title")
                        #content
                        len_content = len(self.find_element_by_class_name("user_tx_area").find_elements_by_tag_name("p"))
                        content = ""
                        for i in range(len_content):
                            try:
                                content = content + " " + self.find_element_by_css_selector("#content > div.article > div.obj_section.noline.center_obj > div.review > div.user_tx_area > p:nth-child("+str(i+1)+")").text
                            except:
                                pass
                        #content > div.article > div.obj_section.noline.center_obj > div.review > div.user_tx_area > p:nth-child(11)
                        if content=="":
                            review_one.append(None)
                        else:
                            review_one.append(content)
                        # print("--content")
                        #lookup
                        try:
                            review_one.append(int(self.find_element_by_css_selector("#content > div.article > div.obj_section.noline.center_obj > div.review > div.board_title > div > span:nth-child(1) > em").text))
                        except:
                            review_one.append(None)
                        # print("--lookup")
                        #recommend
                        try:
                            review_one.append(int(self.find_element_by_css_selector("#goodReviewCount").text))
                        except:
                            review_one.append(None)
                        # print("--recommend")
                        
                        review2.extend(self.get_review2_table_info(r_code))
                        review.append(review_one)
                        movie_review.append(movie_review_one)
                        self.back()
                        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
                    except:
                        break

            return review, movie_review, review2
        except:
            return None, None, None



    def get_review2_table_info(self, r_code):
        review2 = []
        # #review2
        num_review2 = int(self.find_element_by_css_selector("#cbox_module > div > div.u_cbox_head > span").text)
        # print(num_review2)
        if num_review2==0:
            pass
        else:
            # if num_review2%20==0:
            #     num_page2 = int(num_review2/20)
            # else:
            #     num_page2 = int(num_review2/20)+1
            num_page2 = int(np.ceil(num_review2/20))
            for page2 in range(num_page2):
                if page2 == 5:
                    break
                elif page2 == 0:
                    pass
                else:
                    try:
                        self.find_element_by_xpath('//*[@id="cbox_module"]/div/div[5]/div/a['+str(page2)+']/span').click()
                        self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
                    except:
                        break
                for i in range(20):
                    try:
                        review2_one = [r_code]
                        #id
                        review2_one.append(self.find_element_by_xpath('//*[@id="cbox_module_wai_u_cbox_content_wrap_tabpanel"]/ul/li['+str(i+1)+']/div[1]/div/div[1]/span[1]/span/span/span/span').text)
                        #content
                        try:
                            review2_one.append(self.find_element_by_xpath('//*[@id="cbox_module_wai_u_cbox_content_wrap_tabpanel"]/ul/li['+str(i+1)+']/div[1]/div/div[2]').text)
                        except:
                            review2_one.append(None)
                        #date
                        try:
                            review2_one.append(self.find_element_by_xpath('//*[@id="cbox_module_wai_u_cbox_content_wrap_tabpanel"]/ul/li['+str(i+1)+']/div[1]/div/div[3]/span[1]').text)
                        except:
                            review2_one.append(None)
                        #good
                        try:
                            review2_one.append(int(self.find_element_by_xpath('//*[@id="cbox_module_wai_u_cbox_content_wrap_tabpanel"]/ul/li['+str(i+1)+']/div[1]/div/div[4]/div/a[1]/em').text))
                        except:
                            review2_one.append(None)
                        #bad
                        try:
                            review2_one.append(int(self.find_element_by_xpath('//*[@id="cbox_module_wai_u_cbox_content_wrap_tabpanel"]/ul/li['+str(i+1)+']/div[1]/div/div[4]/div/a[2]/em').text))
                        except:
                            review2_one.append(None)

                        review2.append(review2_one)
                    except:
                        break

        return review2
    def get_image_table_info(self, movie_code, url):
        #[movie_code, image_url]
        self.get(self.current_url.replace("detail", "basic"))
        try:
            self.get(url)
            self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
            image = []
            for i in range(int(self.find_element_by_css_selector("#_MainPhotoArea > div.title_area > span > em").text)):
                image_one = [movie_code]
                image_one.append(self.find_element_by_css_selector("#_MainPhotoArea > div.viewer > div > img").get_attribute("src"))
                image.append(image_one)
                self.find_element_by_css_selector("#_MainPhotoArea > div.viewer > a._NextBtn._NoOutline.pic_next").click()
            if image==[]:
                return None
            else:
                return image
        except:
            return None
    def get_video_table_info(self, movie_code):
        #[movie_index, video_name, video_url]
        try:
            self.get(self.current_url.replace("basic", "media"))
            video = []
            num_v = len(self.find_elements_by_css_selector("#content > div.article > div.obj_section2.noline > div > div.ifr_module > div > div > ul > li > p.tx_video.ico > a"))
            for index in range(num_v):
                vd = self.find_elements_by_css_selector("#content > div.article > div.obj_section2.noline > div > div.ifr_module > div > div > ul > li > p.tx_video.ico > a")[index]
                video_one = [movie_code]
                video_one.append(vd.text)
                vd.click()
                self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
                video_one.append(self.current_url)
                self.back()
                self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
                if video_one==[movie_code]:
                    pass
                else:
                    video.append(video_one)
            self.back()
            self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
            if video==[]:
                return None
            else:
                return video
        except:
            return None
    def get_jenre_table_info(self, movie_code):
        #[movie_index, jenre_type]
        try:
            jenre = []
            for jnr in self.find_elements_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[1]/p/span[1]/a'):
                jenre_one = [movie_code]
                jenre_one.append(jnr.text)
                jenre.append(jenre_one)
            return jenre
        except:
            return None
    def get_nation_table_info(self, movie_code):
        # [movie_code, country_name]
        try:
            nation = []
            for ctr in self.find_elements_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[1]/p/span[2]/a'):
                nation_one = [movie_code]
                nation_one.append(ctr.text)
                nation.append(nation_one)
            return nation
        except:
            return None
    def get_point_table_info(self, movie_code):
        #[movie_code, point_content, point_id, point_date, point_good, point_bad, point_star]
        try:
            point = []
            self.get(self.current_url.replace("basic", "point"))
            self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
            self.switch_to.frame('pointAfterListIframe')
            num_point = int(self.find_element_by_css_selector("body > div > div > div.score_total > strong > em").text.replace(",",""))
            if num_point%10==0:
                num_page = int(num_point/10)
            else:
                num_page = int(num_point/10) + 1
            for page in range(1, num_page+1):
                if page==11:
                    break
                elif page==1:
                    pass
                else:
                    self.find_element_by_css_selector("#pagerTagAnchor"+str(page)+" > em").click()

                for i in range(10):
                    try:
                        point_one = [movie_code]
                        #content
                        content = self.find_element_by_css_selector("#_filtered_ment_"+str(i)).text
                        if content=='':
                            point_one.append(None)
                        else:
                            point_one.append(content)
                        # try:
                        #     point_one.append(self.find_element_by_css_selector("#_filtered_ment_"+str(i)).text)
                        # except:
                        #     point_one.append(None)
                        
                        #id
                        point_one.append(self.find_element_by_css_selector("body > div > div > div.score_result > ul > li:nth-child("+str(i+1)+") > div.score_reple > dl > dt > em:nth-child(1) > a > span").text)
                        #date
                        point_one.append(self.find_element_by_css_selector("body > div > div > div.score_result > ul > li:nth-child("+str(i+1)+") > div.score_reple > dl > dt > em:nth-child(2)").text)
                        #good
                        point_one.append(int(self.find_element_by_css_selector("body > div > div > div.score_result > ul > li:nth-child("+str(i+1)+") > div.btn_area > a._sympathyButton > strong").text))
                        #bad
                        point_one.append(int(self.find_element_by_css_selector("body > div > div > div.score_result > ul > li:nth-child("+str(i+1)+") > div.btn_area > a._notSympathyButton > strong").text))
                        #star
                        point_one.append(int(self.find_element_by_css_selector("body > div > div > div.score_result > ul > li:nth-child("+str(i+1)+") > div.star_score > em").text))
                        
                        point.append(point_one)
                    except:
                        break
            self.get(self.current_url.replace("point", "basic"))
            return point
        except:
            return None

    #해당 연도 정보 취합
    def get_all_of_year(self, year, user):

        self.land_page()

        self.land_directory_of_year(year)
        movie_urls_of_year = self.get_movies_in_the_page()
        for url in movie_urls_of_year[194:]:
            print(url)
            movie_table = []
            # actor_table = []
            # movie_actor_table = []
            # director_table = []
            # movie_director_table = []
            # review_table = []
            # movie_review_table = []
            # review2_table = []
            # image_table = []
            # video_table = []
            # jenre_table = []
            # nation_table = []
            # point_table = []
            
            # self.get(url)
            try:
                self.get(url)
                self.implicitly_wait(const.IMPLICIT_WAIT_TIME)
            except:
                pass


            print(">>land page success")
            # self.switch_to.window(self.window_handles[-1]);
            try:
                movie_code = self.get_movie_code(url)
            except:
                self = Naver_scrapping()
                self.land_page(url)
                movie_code = self.get_movie_code(url)
            print(">>movie code complete")

            try:
                movie_table.append(self.get_movie_table_info(movie_code, year))
                user.input_data(table = "movie",
                    columns="movie_code, title, original_title, opening_date, \
                        playing_time, domestic_rate, foreign_rate, cumulative_audience, \
                        subtitle, content, poster_url, audience_rate, journalist_rate, \
                        netizen_rate, audience_count, journalist_count, netizen_count", 
                    data=movie_table)
                print(">>movie complete")
            except:
                print(">>movie failed ---")
            # #actor & movie_actor
            try:
                actor, movie_actor = self.get_actor_table_info(movie_code)
                user.input_data(table = "actor",
                        columns="actor_name, original_actor_name, actor_code", 
                        data=actor)
                print(">>actor complete")
            except:
                print(">>actor failed ---")
            try:
                user.input_data(table = "movie_actor",
                        columns="movie_code, cast, role, actor_code", 
                        data=movie_actor)
                print(">>movie actor complete")
            except:
                print(">>movie actor failed ---")
            # if actor==None:
            #     pass
            # else:
            #     actor_table.extend(actor)
            # if movie_actor==None:
            #     pass
            # else:
            #     movie_actor_table.extend(movie_actor)
            # #director & movie_director
            try:
                director, movie_director = self.get_director_table_info(movie_code)
                user.input_data(table = "director",
                        columns="director_name, original_director_name, director_code", 
                        data=director)
                print(">>director complete")
            except:
                print(">>director failed ---")
            try:
                user.input_data(table = "movie_director",
                        columns="movie_code, director_code", 
                        data=movie_director)
                print(">>movie director complete")
            except:
                print(">>movie director failed ---")
            # if director==None:
            #     pass
            # else:
            #     director_table.extend(director)
            # if movie_director==None:
            #     pass
            # else:
            #     movie_director_table.extend(movie_director)
            # #review
            
            # if review==None:
            #     pass
            # else:
            #     try:
            #         review_table.extend(review)
            #     except:
            #         pass
            # if movie_review==None:
            #     pass
            # else:
            #     try:
            #         movie_review_table.extend(movie_review)
            #     except:
            #         pass
            # if review2==None:
            #     pass
            # else:
            #     try:
            #         review2_table.extend(review2)
            #     except:
            #         pass
            # #image
            # image = self.get_image_table_info(movie_code)
            # if image==None:
            #     pass
            # else:
            #     try:
            #         image_table.extend(image)
            #     except:
            #         pass
            # #video
            # video = self.get_video_table_info(movie_code)
            # if video==None:
            #     pass
            # else:
            #     try:
            #         video_table.extend(video)
            #     except:
            #         pass
            # #jenre
            # jenre = self.get_jenre_table_info(movie_code)
            # if jenre==None:
            #     pass
            # else:
            #     jenre_table.extend(jenre)
            # #nation
            # nation = self.get_nation_table_info(movie_code)
            # if nation==None:
            #     pass
            # else:
            #     nation_table.extend(nation)
            # #point
            # point = self.get_point_table_info(movie_code)
            # if point==None:
            #     pass
            # else:
            #     point_table.extend(point)
           
            
            
            
            
            review, movie_review, review2 = self.get_review_table_info(movie_code)
            print(">>review function complete")
            try:
                user.input_data(table = "review",
                        columns="review_id, review_date, review_code, review_title, review_content, review_lookup, review_recommend", 
                        data=review)
                print(">>review complete")
            except:
                print(">>review failed ---")
            try:
                user.input_data(table = "movie_review",
                        columns="movie_code, review_code", 
                        data=movie_review)
                print(">>movie review complete")
            except:
                print(">>movie review failed ---")
            try:
                user.input_data(table = "review2",
                        columns="review_code, review2_id, review2_content, review2_date, review2_good, review2_bad", 
                        data=review2)
                print(">>review2 complete")
            except:
                print(">>review2 failed ---")
            
            try:
                user.input_data(table = "image",
                        columns="movie_code, image_url", 
                        data=self.get_image_table_info(movie_code, url))
                print(">>image complete")
            except:
                print(">>image failed ---")
            try:
                user.input_data(table = "video",
                        columns="movie_code, video_title, video_url", 
                        data=self.get_video_table_info(movie_code))
                print(">>video complete")
            except:
                print(">>video failed ---")
            try:
                user.input_data(table = "jenre",
                        columns="movie_code, jenre_name", 
                        data=self.get_jenre_table_info(movie_code))
                print(">>jenre complete")
            except:
                print(">>jenre failed ---")
            try:
                user.input_data(table = "nation",
                        columns="movie_code, country", 
                        data=self.get_nation_table_info(movie_code))
                print(">>nation complete")
            except:
                print(">>nation failed ---")
            try:
                user.input_data(table = "point",
                        columns="movie_code, point_content, point_id, \
                            point_date, point_good, point_bad, point_star", 
                        data=self.get_point_table_info(movie_code))
                print(">>point complete")
            except:
                print(">>point failed ---")
            
        # return movie_table, actor_table, movie_actor_table, director_table, movie_director_table, review_table, \
        #     movie_review_table, review2_table, image_table, video_table, jenre_table, nation_table, point_table


if __name__ == '__main__':
    # str = "총 601건"
    # print(int(str.replace(",","").replace("총 ", "").replace("건", "")))
    # crawler = Naver_scrapping()
    # crawler.land_page("https://movie.naver.com/movie/bi/mi/basic.naver?code=28876")

    # # print(int(crawler.find_element_by_xpath('/html/body/div/div[4]/div[3]/div[1]/div[4]/div/div/div/div/div[2]/span/em').text.replace(",","")))

    # movie_c = crawler.get_movie_code()
    # # infos = crawler.get_movie_information(2023)
    # # infos = crawler.get_movie_info(10)
    # rw, mrw, rw2 = crawler.get_review_table_info(movie_c)

    # print(rw)
    # print(mrw)
    # print(rw2)


    # crawler = Naver_scrapping()
    hyojin = SQL(db="naver", user="hyojin", password="gywls")
    # crawler.land_page()
    # crawler.land_page("https://movie.naver.com/movie/bi/mi/basic.naver?code=201335")
    # crawler.land_page("https://movie.naver.com/movie/bi/mi/review.naver?code=201335")
    # print(crawler.find_element_by_css_selector("#reviewTab > div > div > ul > li:nth-child(2) > span > em:nth-child(2)").text)
    # rw, mrw, rw2 = crawler.get_review_table_info(201335)
    # print(rw)
    # print(mrw)
    # print(rw2)

    # hyojin.input_data(table = "review",
    #                     columns="review_id, review_date, review_code, review_title, review_content, review_lookup, review_recommend", 
    #                     data=rw)
    # hyojin.input_data(table = "movie_review",
    #                     columns="movie_code, review_code", 
    #                     data=mrw)
    # hyojin.input_data(table = "review2",
    #                     columns="review_code, review2_id, review2_content, review2_date, review2_good, review2_bad", 
    #                     data=rw2)

    # crawler.get_all_of_year(2023, hyojin)
    #349
    # Naver_scrapping().get_all_of_year(2021, hyojin)
    # review = []
    # movie_review = []
    # review2 = []
    # point = []
    # image = []
    # video = []

    # img = crawler.get_image_table_info(10)
    # vd = crawler.get_video_table_info(10)

    # rev, mo_rev, rev2 = crawler.get_review_table_info(10)
    # pt = crawler.get_point_table_info(10)

    # try:
    #     image.extend(img)
    # except:
    #     pass    
    # try:
    #     video.extend(vd)
    # except:
    #     pass   
    # try: 
    #     review.extend(rev)
    # except:
    #     pass    
    # try:
    #     movie_review.extend(mo_rev)
    # except:
    #     pass    
    # try:
    #     review2.extend(rev2)
    # except:
    #     pass    
    # try:
    #     point.extend(pt)
    # except:
    #     pass    

    # print(image)
    # print(video)
    # print(review)
    # print(movie_review)
    # print(review2)
    # print(point)
    def get_all_of_year_main(year, user):
        crawler = Naver_scrapping()
        crawler.land_page()

        crawler.land_directory_of_year(year)
        movie_urls_of_year = crawler.get_movies_in_the_page()
        crawler.quit()
        for url in movie_urls_of_year[504:]:
            
            print(url)
            movie_table = []
            # actor_table = []
            # movie_actor_table = []
            # director_table = []
            # movie_director_table = []
            # review_table = []
            # movie_review_table = []
            # review2_table = []
            # image_table = []
            # video_table = []
            # jenre_table = []
            # nation_table = []
            # point_table = []
            
            # self.get(url)

            crawler = Naver_scrapping()


            crawler.get(url)
            crawler.implicitly_wait(const.IMPLICIT_WAIT_TIME)


            print(">>land page success")
            # self.switch_to.window(self.window_handles[-1]);

            movie_code = crawler.get_movie_code(url)

            print(">>movie code complete")

            try:
                movie_table.append(crawler.get_movie_table_info(movie_code, year))
                user.input_data(table = "movie",
                    columns="movie_code, title, original_title, opening_date, \
                        playing_time, domestic_rate, foreign_rate, cumulative_audience, \
                        subtitle, content, poster_url, audience_rate, journalist_rate, \
                        netizen_rate, audience_count, journalist_count, netizen_count", 
                    data=movie_table)
                print(">>movie complete")
            except:
                print(">>movie failed ---")
            # #actor & movie_actor
            try:
                actor, movie_actor = crawler.get_actor_table_info(movie_code)
                user.input_data(table = "actor",
                        columns="actor_name, original_actor_name, actor_code", 
                        data=actor)
                print(">>actor complete")
            except:
                print(">>actor failed ---")
            try:
                user.input_data(table = "movie_actor",
                        columns="movie_code, cast, role, actor_code", 
                        data=movie_actor)
                print(">>movie actor complete")
            except:
                print(">>movie actor failed ---")
            # if actor==None:
            #     pass
            # else:
            #     actor_table.extend(actor)
            # if movie_actor==None:
            #     pass
            # else:
            #     movie_actor_table.extend(movie_actor)
            # #director & movie_director
            try:
                director, movie_director = crawler.get_director_table_info(movie_code)
                user.input_data(table = "director",
                        columns="director_name, original_director_name, director_code", 
                        data=director)
                print(">>director complete")
            except:
                print(">>director failed ---")
            try:
                user.input_data(table = "movie_director",
                        columns="movie_code, director_code", 
                        data=movie_director)
                print(">>movie director complete")
            except:
                print(">>movie director failed ---")
            
            try:
                user.input_data(table = "image",
                        columns="movie_code, image_url", 
                        data=crawler.get_image_table_info(movie_code, url))
                print(">>image complete")
            except:
                print(">>image failed ---")
            try:
                user.input_data(table = "video",
                        columns="movie_code, video_title, video_url", 
                        data=crawler.get_video_table_info(movie_code))
                print(">>video complete")
            except:
                print(">>video failed ---")
            try:
                user.input_data(table = "jenre",
                        columns="movie_code, jenre_name", 
                        data=crawler.get_jenre_table_info(movie_code))
                print(">>jenre complete")
            except:
                print(">>jenre failed ---")
            try:
                user.input_data(table = "nation",
                        columns="movie_code, country", 
                        data=crawler.get_nation_table_info(movie_code))
                print(">>nation complete")
            except:
                print(">>nation failed ---")
            try:
                user.input_data(table = "point",
                        columns="movie_code, point_content, point_id, \
                            point_date, point_good, point_bad, point_star", 
                        data=crawler.get_point_table_info(movie_code))
                print(">>point complete")
            except:
                print(">>point failed ---")

            review, movie_review, review2 = crawler.get_review_table_info(movie_code)
            print(">>review function complete")
            try:
                user.input_data(table = "review",
                        columns="review_id, review_date, review_code, review_title, review_content, review_lookup, review_recommend", 
                        data=review)
                print(">>review complete")
            except:
                print(">>review failed ---")
            try:
                user.input_data(table = "movie_review",
                        columns="movie_code, review_code", 
                        data=movie_review)
                print(">>movie review complete")
            except:
                print(">>movie review failed ---")
            try:
                user.input_data(table = "review2",
                        columns="review_code, review2_id, review2_content, review2_date, review2_good, review2_bad", 
                        data=review2)
                print(">>review2 complete")
            except:
                print(">>review2 failed ---")
            crawler.quit()
    
    get_all_of_year_main(2020, hyojin)