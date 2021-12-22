import os
import pandas as pd
import sqlite3

path = os.getcwd()
file_list = os.listdir(path)
files = [file for file in file_list if file.endswith('.db')]

df_category_ori = pd.DataFrame(columns=['category_id', 'category_name'])
df_book_ori = pd.DataFrame(columns=['id', 'name', 'nameE', 'writer', 'data', 'category1', 'category2', 'summary', 'price', 'rate'])
df_review_ori = pd.DataFrame(columns=['book_id', 'reviewer_id', 'reviewer', 'rate', 'review'])

print(files)

cate_cnt = False
for i in files:
    DATABASE_PATH = os.path.join(path, i)
    conn = sqlite3.connect(DATABASE_PATH)
    print(f'\n{i} 파일과 연결되었습니다.')

    try:
        book = pd.read_sql_query("SELECT * FROM BOOK", conn)
        df_book_ori = pd.concat([df_book_ori, book])
        print(f'df_book에 {len(book)}만큼 데이터가 추가되었습니다.')
    except:
        print(f'{i}에는 book 데이터가 없습니다.')

    try:
        review = pd.read_sql_query("SELECT * FROM REVIEW", conn)
        df_review_ori = pd.concat([df_review_ori, review])
        print(f'df_review에 {len(review)}만큼 데이터가 추가되었습니다.')
    except:
        print(f'{i}에는 review 데이터가 없습니다.')

    if cate_cnt==False:
        category = pd.read_sql_query("SELECT * FROM CATEGORY", conn)
        df_category_ori = pd.concat([df_category_ori, category])
        print(f'df_category에 {len(category)}만큼 데이터가 추가되었습니다.')
        cate_cnt = True

    # cur = conn.cursor()
    # print(f'\n{i} 파일과 연결되었습니다.')

    # cur.execute("SELECT * FROM BOOK")
    # book = cur.fetchall()
    # book = pd.DataFrame.from_records(data=book)
    # df_book_ori = pd.concat([df_book_ori, book])
    # print(f'df_book에 {len(book)}만큼 데이터가 추가되었습니다.')

    # cur.execute("SELECT * FROM REVIEW")
    # review = cur.fetchall()
    # review = pd.DataFrame.from_records(data=review)
    # df_review_ori = pd.concat([df_review_ori, review])
    # print(f'df_review에 {len(book)}만큼 데이터가 추가되었습니다.')
    
    # if cate_cnt == False:
    #     cur.execute("SELECT * FROM CATEGORY")
    #     category = cur.fetchall()
    #     category = pd.DataFrame.from_records(data=category)
    #     df_category_ori = pd.concat([df_category_ori, category])
    #     print(f'df_category에 {len(book)}만큼 데이터가 추가되었습니다.')
    # else:
    #     pass


df_category_ori = df_category_ori.reset_index()
df_book_ori = df_book_ori.reset_index()
df_review_ori = df_review_ori.reset_index()

print('\n\n최종')
print(len(df_category_ori))
print(len(df_book_ori))
print(len(df_review_ori))

df_category_ori.to_pickle('df_category_ori.pkl')
df_book_ori.to_pickle('df_book_ori.pkl')
df_review_ori.to_pickle('df_review_ori.pkl')
