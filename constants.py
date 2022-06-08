MOVIE_URL = "https://movie.naver.com/movie/running/current.naver"
MOVIE_DIRECORY_URL = "https://movie.naver.com/movie/sdb/browsing/bmovie_nation.naver"
IMPLICIT_WAIT_TIME = 3
SAMPLE_URL = "https://movie.naver.com/movie/bi/mi/basic.naver?code=191639"
SAMPLE_URL2 = "https://movie.naver.com/movie/bi/mi/basic.naver?code=87717"
SAMPLE_URL3 = "https://movie.naver.com/movie/bi/mi/basic.naver?code=187940"
SAMPLE_URL4 = "https://movie.naver.com/movie/bi/mi/basic.naver?code=150389"
SAMPLE_URL5 = "https://movie.naver.com/movie/bi/mi/basic.naver?code=28876"



        # def get_number_of_movies(self):
        #     movies = self.find_elements_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li/dl/dt/a')
        # num = len(movies)
        # return num


    # def get_movie_information_showing(self):
    #     opt1 = "([ ])"
    #     opt2 = "([ㄱ-힣 ])"
    #     infos = []
    #     i=1
    #     max = self.get_number_of_movies()
    #     while(1):
    #         info = []
    #         #Title
    #         try:
    #             info.append(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
    #                 +']/dl/dt/a').text)
    #         except:
    #             info.append(None)
    #         #Movie Rate
    #         try:
    #             info.append(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
    #                 +']/dl/dt/span').text)
    #         except:
    #             info.append(None)
    #         #Netizen Rate
    #         try:
    #             rate=float(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
    #                 +']/dl/dd[1]/dl/dd[1]/div/a/span[2]').text)
    #             if rate>0:
    #                 info.append(rate)
    #             else:
    #                 info.append(None)
    #         except:
    #             info.append(None)
    #         #Netizen Count
    #         try:
    #             info.append(int(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
    #                 +']/dl/dd[1]/dl/dd[1]/div/a/span[3]/em').text.replace(",","")))
    #         except:
    #             info.append(0)
    #         #Journalist Score
    #         try:
    #             info.append(float(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
    #                 +']/dl/dd[1]/dl/dd[2]/div/a/span[2]').text))
    #         except:
    #             info.append(None)
    #         #Journalist Count
    #         try:
    #             info.append(int(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
    #                 +']/dl/dd[1]/dl/dd[2]/div/a/span[3]/em').text.replace(",","")))
    #         except:
    #             info.append(0)
    #         #Scope, Playing Time, Opening Date
    #         spo = self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
    #             +']/dl/dd[2]/dl/dd[1]').text.split('|')
    #         #Scope
    #         try:
    #             info.append(re.sub(opt1, "", spo[0]))
    #         except:
    #             info.append(None)
    #         #Playing Time
    #         try:
    #             info.append(re.sub(opt2, "", spo[1]))
    #         except:
    #             info.append(None)
    #         #Opening Date
    #         try:
    #             info.append(re.sub(opt2, "", spo[2]).replace(".","-"))
    #         except:
    #             info.append(None)
    #         #Director
    #         try:
    #             info.append(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
    #                 +']/dl/dd[2]/dl/dd[2]/span/a').text)
    #         except:
    #             info.append(None)
    #         #Image URL
    #         try:
    #             info.append(self.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li['+str(i) \
    #                 +']/div/a/img').get_attribute('src'))
    #         except:
    #             info.append(None)
    #         infos.append(info)
    #         i+=1
    #         if(i>max):
    #             break
    #     return infos