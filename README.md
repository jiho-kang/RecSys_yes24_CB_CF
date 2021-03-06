비고: 개인 프로젝트
</br>

### 목차

[1. 프로젝트 제목](#1-프로젝트-제목)</br>
[2. 프로젝트 개요](#2-프로젝트-개요)</br>
[3. 분석 방법](#3-분석-방법)</br>
[4. 보완점 및 회고](#4-보완점-및-회고)</br>
[5. Next step after lesson learned](#5-next-step-after-lesson-learned)


# 1. 프로젝트 제목
### CF CB를 이용한 책 추천 시스템

</br>

# 2. 프로젝트 개요

### <기간>
- 2021.12.13-2021.12.22 (10일)

### <배경>
- 유저가 구입한 책 정보를 토대로 관심을 가질법한 다른 아이템 추천.
- 개인화 추천 시스템은 재구매를 유도하고 충성고객 확보의 효과가 있음. 매출 증대에 직접적이며 강력한 영향력을 행사하므로 많은 기업에서 추천 시스템을 이용 중임.
- 추천시스템에 대한 이해를 위해 기본적인 모델인 Content-Based Filtering(CB) 과 Collaborative Filtering(CF)을 이용하여 데이터를 분석하는 것이 목적.

### <데이터>
- yes24 홈페이지에서 웹 크롤링을 통해 데이터 수집 [(코드)](https://github.com/jiho-kang/RecSys_yes24_CB_CF/tree/main/crawling_code)
- yes24 홈페이지 -> BEST -> 카테고리별 -> Top 1000개의 책 -> 책ID, 책 제목, 부제, 작가, 출간일, 평점, 가격, 상위 카테고리, 하위 카테고리, 책 내용, 리뷰(유저ID, 유저이름, 평점, 리뷰 text) 수집
- 책 갯수: 4,598권 / 리뷰 갯수: 246,753개 / 유저 : 89,865명

</br>

# 3. 분석 방법 [(코드)](https://github.com/jiho-kang/RecSys_yes24_CB_CF/blob/main/RecSys_project_1_code.ipynb)
## 3-1. Content-Based Filtering, CB
- 선정 이유</br>
: 추천시스템의 가장 기본적인 방법 중 하나이며, 아이템의 특성으로 '줄거리'를 벡터화한다면 비슷한 내용의 책을 추천해줄 수 있을 것으로 생각.

- 방법</br>
  - 줄거리 전처리: 한글, 숫자, 영어 제외 모두 제거, 불용어 제거.
    - before
    - ![image](https://user-images.githubusercontent.com/43432539/154486276-55261b8d-6fac-44bf-bdc8-8dc4397fd132.png)
    - after
    - ![image](https://user-images.githubusercontent.com/43432539/154486406-9a3319a3-0868-4439-abbe-13857f1accc9.png)

  - tf-idf로 전처리된 줄거리 특성 벡터화.
  - 코사인 유사도로 줄거리끼리의 유사도 계산.

- 결과</br>
  ![image](https://user-images.githubusercontent.com/43432539/154487777-95e0032d-70ea-4d4d-bbc1-fc668f628c71.png)
  </br>
  
  ![image](https://user-images.githubusercontent.com/43432539/154486847-c29cf5af-db54-4aa1-a529-34dce55abdc3.png)

</br>

## 3-2. Collaborative Filtering, CF (Item-based)
- 선정이유</br>
: 추천시스템의 가장 기본적인 방법 중 하나이며, 유저의 수가 아이템의 수보다 현저히 많으며, 유저 * 책의 matrix가 sparse하기 때문에 user-based보다 item-based모델을 사용.

- 방법</br>
  - 평점이 value인 user * book matrix를 생성.
  - 코사인 유사도를 사용.

- 결과</br>
  - CB보다 조금 더 fresh한 아이템을 추천해줌.</br>
  ![image](https://user-images.githubusercontent.com/43432539/154487834-c05aec82-cf7d-4082-8d2c-3e241a68ce4f.png)

    ![image](https://user-images.githubusercontent.com/43432539/154487871-ac227c2d-76f1-4f2f-9270-fe690e76146b.png)

</br>

# 4. 보완점 및 회고
### <프로젝트 관리 측면>
- 업무 중요도에 따른 시간 분배</br>
  : 약 10일의 기간 중 크롤링 코드를 구현하고 데이터를 수집하는데 6일을 사용함. 본 프로젝트의 목표는 추천시스템의 기본적인 모델에 대한 이해도 향상이었기 때문에 데이터 수집보다 분석과 방법론에 더 많은 고민과 학습이 필요했으나 그러지 못했음.
- 시도한 내용 기록하기
  : 무엇을 공부했고,  어떤 것을 시도했고, 실패한 원인은 무엇인지 기록.

### <모델 측면>
- 유저 * 아이템의 평점 matrix가 sparse하기 때문에 유사도값이 낮다. ==> 평점을 n개 이상 남긴 유저만 사용하여 진행했다면 유사도값이 전반적으로 증가할 것이다.
- 유사도의 특성으로 CB는 줄거리, CF는 평점으로 각 하나씩만 사용함. 장르, 작가와 같은 다양한 특성을 고려한 모델을 만든다면 정확도가 높아질 것.
- 신규 유저의 경우 정보가 없으므로 추천이 어렵다.
- 선정한 모델의 이론과 개념에 대한 공부가 충분히 선행되어야 함.
- 프로젝트를 진행하며 논리적인 의사결정에 기반한 방법론 선정이 필요함. 본 프로젝트에서는 모델 선정이나 코사인 유사도를 사용한 이유가 명확하지 않음. 데이터와 해결하고자 하는 문제에 맞는 방법을 설정해야함.

</br>

# 5. Next step after lesson learned
- [KoBERT를 이용한 context 태깅 추출 & 개인-정책 매칭을 위한 추천시스템 구축](https://github.com/jiho-kang/NLP_RecSys_Project)
  - 프로젝트 진행 일정을 짜고, 중요한 업무를 우선하여 진행.
  - 방법론 선정을 위해 다양하게 공부하고 기록에 남김.
  - 여러가지 특성을 활용한 모델을 구현함.
