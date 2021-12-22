from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
import subprocess
import shutil
from time import sleep
import re
import math
import warnings; warnings.filterwarnings('ignore')
import os
import sqlite3



path = os.getcwd()
driver = webdriver.Chrome(f'{path}/chromedriver')
driver.implicitly_wait(10)



def book_information(cate_name, data):
    try:
        id_url = driver.current_url
        n = id_url.find('ds/')
        b_id = id_url[n+3:]
        b_name = driver.find_element_by_class_name('gd_name').text
        print('\n책 이름: ', b_name)
        
        if b_id not in data:
            try:
                b_nameE = driver.find_element_by_class_name('gd_nameE').text
            except:
                b_nameE = None
                print('\n책 한 줄 요약이 없음.')
            
            try:
                b_rating = driver.find_element_by_class_name('yes_b').text
            except:
                b_rating = None
                print('\n책 평점이 없음')

            try:
                b_category1 = cate_name
                b_category2 = driver.find_element_by_css_selector('#infoset_goodsCate > div.infoSetCont_wrap > dl > dd > ul > li:nth-child(1) > a:nth-child(6)').text
            except:
                b_category2 = None
                print('\ncategory2 내용이 없음')
            
            try:
                b_summary = driver.find_element_by_class_name('infoWrap_txtInner').text
            except:
                b_summary = None
                print('\n책 내용 수집 실패')
            
            try:
                b_writer = driver.find_element_by_css_selector('#yDetailTopWrap > div.topColRgt > div.gd_infoTop > span.gd_pubArea > span.gd_auth > a:nth-child(1)').text
                b_date = driver.find_element_by_class_name('gd_date').text
            except:
                b_writer = None
                b_date = None
                print('\n writer나 date 내용이 없음')
            
            try:
                if driver.find_element_by_css_selector('#yDetailTopWrap > div.topColRgt > div.gd_infoBot > div.gd_infoTbArea > div:nth-child(4) > table > tbody > tr:nth-child(1) > th').text == '정가':
                    b_price = driver.find_element_by_css_selector('#yDetailTopWrap > div.topColRgt > div.gd_infoBot > div.gd_infoTbArea > div:nth-child(4) > table > tbody > tr:nth-child(1) > td > span > em').text
                elif driver.find_element_by_css_selector('#yDetailTopWrap > div.topColRgt > div.gd_infoBot > div.gd_infoTbArea > div:nth-child(3) > table > tbody > tr:nth-child(1) > th').text == '정가':
                    b_price = driver.find_element_by_css_selector('#yDetailTopWrap > div.topColRgt > div.gd_infoBot > div.gd_infoTbArea > div:nth-child(3) > table > tbody > tr:nth-child(1) > td > span > em').text
            except:
                b_price = None
                print('\n가격 정보가 없음.')
                
            try:
                cur.execute('insert into BOOK (id, name, nameE, writer, date, category1, category2, summary, price, rate) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                [b_id, b_name, b_nameE, b_writer, b_date, b_category1, b_category2, b_summary, b_price, b_rating])
                conn.commit()
                data[b_id] = []
            except:
                print('데이터는 다 긁었는데 data에 저장을 못함.')
        
        else:
            print(f'\n[{b_name}는 이미 data 안에 있습니다.')

    except:
        print('\n책 정보 수집에 실패했습니다. in book_information method')
        b_id = None
    return data, b_id

    

def user_review(id, b_id):
    try:
        if id == 'emReviewCountText':
            writer_selector = "#infoset_reviewContentList > div:nth-child({}) > div.reviewInfoTop > div > em.txt_id > a"
            score_selector = "#infoset_reviewContentList > div:nth-child({}) > div.reviewInfoTop > div > span > span:nth-child(1)"
            score_selectors = None
            more_selector = '#infoset_reviewContentList > div:nth-child({}) > div.reviewInfoBot.crop > a > div > span'
            review_selector = '#infoset_reviewContentList > div:nth-child({}) > div.reviewInfoBot.origin > div.review_cont'
            i, br_i = 3, 8
        
        elif id == 'txtOneCommentCount':
            writer_selector = "#infoset_oneCommentList > div.infoSetCont_wrap.rvCmtRow_cont.clearfix > div:nth-child({}) > div.cmt_etc > em.txt_id > a"
            score_selector = None
            score_selectors = '#infoset_oneCommentList > div.infoSetCont_wrap.rvCmtRow_cont.clearfix > div:nth-child({}) > div.cmtInfoBox > div.cmt_rating'
            more_selector = None
            review_selector = "#infoset_oneCommentList > div.infoSetCont_wrap.rvCmtRow_cont.clearfix > div:nth-child({}) > div.cmtInfoBox > div.cmt_cont > span"
            i, br_i = 1,7
    except:
        print('\nuser_review 메소드에서 html 태그 정보를 가져오지 못했습니다.')

    for i in range(i, br_i):
        try:
            # 리뷰어 이름, ID
            writer = driver.find_element_by_css_selector(writer_selector.format(i))
            writer_id = writer.get_attribute('onclick')
            r = re.compile('[0-9]+')
            m = r.search(writer_id)
            writer_id = m.group()
            writer = writer.text
        except:
            print('\nuser_review 메소드에서 review_id와 이름 가져오기에 실패했습니다.')
            continue
        
        try:
            # 리뷰 평점
            if score_selector is not None:
                score = driver.find_element_by_css_selector(score_selector.format(i)).text
            else:
                spans = driver.find_element_by_css_selector(score_selectors.format(i))
                score_spans = spans.find_elements_by_tag_name('span')
                score = score_spans[1].text
        except:
            print('\nuser_review 메소드에서 리뷰 평점 가져오기에 실패했습니다.')
            score = ''

        # 리뷰 더보기 선택
        if more_selector is not None:
            try:
                driver.find_element_by_css_selector(more_selector.format(i)).click()
            except:
                pass
            
        try:
            # 리뷰
            review = driver.find_element_by_css_selector(review_selector.format(i)).text 
        except:
            print('\nuser_review 메소드에서 리뷰 text 가져오기에 실패했습니다.')
            review = ''

        try:
            # 데이터 축적
            cur.execute('insert into REVIEW (book_id, reviewer_id, reviewer, rate, review) values (?, ?, ?, ?, ?)',
            [b_id, writer_id, writer, score, review])
            conn.commit()
            print(f'{writer}가 남긴 책:{b_id} 리뷰 저장 완료')
        except:
            print(f'\nuser_review 메소드에서 {writer}의 리뷰 정보를 저장하지 못했슶니다.')
    print('\n6개 리뷰 끝')


def book_review(id, b_id, data):
    try:
        if id == 'emReviewCountText':
            print('\n<<<<<<장문 리뷰 수집 시작>>>>>>')
            review_sentence_num = int(driver.find_element_by_id(f'{id}').text[1:-1])
            review_sentence_pages = math.ceil(review_sentence_num /5) 
            page_selector = '//*[@id="infoset_reviewContentList"]/div[1]/div[1]/div/a[{}]'
            next_selector = '//*[@id="infoset_reviewContentList"]/div[1]/div[1]/div/a[12]'
            h_word = 'review_sort_area'
            # h = driver.find_element_by_id(h_word)

        elif id == 'txtOneCommentCount':
            print('\n<<<<<<한줄평 리뷰 수집 시작>>>>>>')
            review_sentence_num = int(driver.find_element_by_id(f'{id}').text[1:-2])
            review_sentence_pages = math.ceil(review_sentence_num /6)
            page_selector = '//*[@id="infoset_oneCommentList"]/div[2]/div[1]/div/a[{}]'
            next_selector = '//*[@id="infoset_oneCommentList"]/div[2]/div[1]/div/a[12]'
            # h_word = '//*[@id="infoset_oneCommentList"]/div[2]/div[1]/div'
            # h = driver.find_element_by_xpath(h_word)

        click_cnt = 0
        for rs_page in range(1, review_sentence_pages+1):
            print(f'\n--------{rs_page}번째 페이지--------')
            if click_cnt > 2:
                print(f'\n{click_cnt}번이나 리뷰 내 페이지 버튼 클릭에 실패해서 더이상 안할게요')
                break
            else:
                pass

            try:
                if id == 'emReviewCountText':
                    h = driver.find_element_by_id(h_word)
                    actions = ActionChains(driver).move_to_element(h)
                    sleep(2)
                    actions.perform()
                    sleep(2)
            except:
                print('\n스크롤 이동 못했음.')
                pass

            try:
                if rs_page == 1:
                    pass
                elif rs_page % 10 == 0:
                    driver.find_element_by_xpath(page_selector.format(11)).click()   
                elif rs_page % 10 == 1:
                    driver.find_element_by_xpath(next_selector).click()
                else:
                    p = (rs_page % 10) + 1
                    driver.find_element_by_xpath(page_selector.format(p)).click()
                    sleep(1.5)
                click_cnt = 0
            except:
                print(f'\n페이지 버튼을 클릭하지 못했어.')
                click_cnt += 1
                continue
            
            try:
                user_review(id, b_id)
            except:
                print('\nuser_review 함수 자체를 실행 못함.')

            sleep(1)
    except:
        print('\n장문 리뷰 수집을 시작도 못하고 끝냈어.')

    return data


# 데이터베이스 만들기
DATABASE_PATH = os.path.join(os.getcwd(), 'scrape_data_jiho_2_4.db')
conn = sqlite3.connect(DATABASE_PATH)
cur = conn.cursor()

# category table 만들기
cur.execute("""
create table if not exists CATEGORY(
    category_id TEXT,
    category_name TEXT
    )
""")

# book table 만들기
cur.execute("""
create table if not exists BOOK(
    id TEXT,
    name TEXT,
    nameE TEXT,
    writer TEXT,
    date TEXT,
    category1 TEXT,
    category2 TEXT,
    summary TEXT,
    price TEXT,
    rate TEXT
)
""")

# review table 만들기
cur.execute("""
create table if not exists REVIEW(
    book_id TEXT,
    reviewer_id TEXT,
    reviewer TEXT,
    rate TEXT,
    review TEXT
)
""")


# 카테고리 목록 수집하기
driver.get("http://www.yes24.com/24/category/bestseller")
category_id = dict()
categorys = driver.find_elements_by_css_selector('#category001 > ul > li')
for category in categorys:
    cate_name = category.find_element_by_tag_name('a').text
    cate_id = category.get_attribute('id')
    category_id[cate_name] = cate_id
    cur.execute('insert into CATEGORY (category_id, category_name) values (?,?)', [cate_id, cate_name])
    conn.commit()
print('==========category_id=============')
print(category_id)
print('\n\n')




data = dict()

for cate_name, cate_id in list(category_id.items())[2:4]:
    # 카테고리 클릭
    cate = driver.find_element_by_css_selector(f'#{cate_id} > a')
    print(f'\n======================================================{cate_name}======================================================')
    cate.click()
    sleep(1)

    for bs_page in range(1, 51):
        try:
            driver.get(f'http://www.yes24.com/24/category/bestseller?CategoryNumber={cate_id[8:]}&sumgb=06&PageNumber={bs_page}')
            print(f'\n=============================베스트셀러의 {bs_page}번째 페이지 접속========================== ')
            sleep(1)

            for i in range(1, 40, 2):
                # 베스트셀러 페이지로 이동
                driver.get(f'http://www.yes24.com/24/category/bestseller?CategoryNumber={cate_id[8:]}&sumgb=06&PageNumber={bs_page}')
                print(f'\n-------------------------{i//2+1}번째 책--------------------------------')

                # 베스트셀러 책 클릭해서 책링크로 이동
                try:
                    driver.find_element_by_css_selector(f"#category_layout > tbody > tr:nth-child({i}) > td.goodsTxtInfo > p:nth-child(1) > a:nth-child(1)").click()
                    print(f'\n책 사이트로 이동 성공')
                    sleep(0.5)
                except:
                    print(print(f'\n책 사이트로 이동 실패'))
                    continue
                
                # 책정보 수집
                try:
                    data, b_id = book_information(cate_name, data)
                    print(f'\n정보 수집 끝')
                except:
                    print(print(f'\n정보 수집 실패'))
                    pass
                    
                # 책 장문 리뷰 수집
                try:
                    data = book_review('emReviewCountText', b_id, data)
                    print(f'\n장문 리뷰 수집 끝.')
                except:
                    print(f'\n장문 리뷰 수집 실패.')
                    pass
                
                # 책 한줄평 리뷰 수집
                try:
                    data = book_review('txtOneCommentCount', b_id, data)
                    print(f'\n한줄평 리뷰 수집 끝.')
                except:
                    print(f"\n한줄평 리뷰 수집 실패")
                    pass
                
                # 책 링크에서 목록으로 이동 (뒤로가기)
                # driver.back()
        except:
            print(f'======================베스트셀러의 {bs_page}번째 페이지 접속 실패========================= ')
        