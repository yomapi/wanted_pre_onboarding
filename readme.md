# 백엔드 코스 - 5차 선발과제

원티드 "프리온보딩 백엔드 코스" 선발 과제를 진행한 프로젝트입니다.


# Install
*이 프로젝트는 [poetry](https://python-poetry.org/docs/)로 패키지 관리를 하였습니다.
~~~ python
poetry install
# 아래 명령어는 django 마이그레이션 파일에 맞춰, table을 생성합니다. DB 설정을 먼저 진행해주세요
python apis/manage.py migrate	
python apis/manage.py runserver
~~~

## Config

~~~ yaml
# aips/configs/config_real.yml 에 설정해줍니다.
# aips/configs/config_example.yml 을 참고하세요.
databases:
	host: "host url"
	port: 3306
	database: "db name"
	username: "username"
	password: "passwd"
	timezone: "+09:00"
secrets:
	django: "django-something-something"
~~~

## DOCS
이 프로젝트는 swagger 문서를 제공합니다.
서버 실행 후, http://localhost:8000/swagger/ 로 접속해서 확인할 수 있습니다.

# 요구사항 분석

1. 채용공고 등록
    1. 존재하지 않는 회사일 경우 채용공고 등록 불가능
    2. reward 음수 등록 불가능
2. 채용공고 수정
    1. 회사 id는 수정 불가능
    2. partilial로 수정 가능
3. 채용공고 삭제
    1. soft delete가 아니며, DB에서 바로 삭제
4. 채용공고 목록조회
    1. limit, offset 등의 pagnation은 별도로 API에 구현하지 않음
5. 채용공고 상세 조회
    1. 회사가올린 다른 채용공고는 limit 50, offset 0을 주어서 조회
6. 채용공고 지원
    1. 중복지원은 불가능

# DB설계

- 복잡한 테이블 구조는 필요하지 않음.
- Applicant(사용자) 와 Company(회사)는 구조상 차이가 없어, userType등의 필드를 주어서 하나의 테이블 내에서 구분하려 하였으나 
”**개발 시 참조하세요!” 에서 2개의 모델을 구분지어 명시해두었으며,** 추후에 이 프로젝트가 진행되어 규모가 커졌을 때를 가정하면, 일반 사용자와 기업 사용자에 필요한 데이터가 달라질 것으로 생각하여 테이블을 분리

![스크린샷 2022-10-17 오후 7.39.07.png](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/1c138c5c-5e41-4857-bfd6-7287920e2092/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2022-10-17_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_7.39.07.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20221017%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20221017T130259Z&X-Amz-Expires=86400&X-Amz-Signature=83026802997dc9ec670fcfefe955fd9beb8587d59914d9b103f5aaaf0ce9a1c6&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22%25E1%2584%2589%25E1%2585%25B3%25E1%2584%258F%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25B5%25E1%2586%25AB%25E1%2584%2589%25E1%2585%25A3%25E1%2586%25BA%25202022-10-17%2520%25E1%2584%258B%25E1%2585%25A9%25E1%2584%2592%25E1%2585%25AE%25207.39.07.png%22&x-id=GetObject)

# 구조 설계

- 복잡한 비지니스 로직이 없기 때문에, API와 repository 2개의 레이어로 나눔
- API
    - request, response를 담당
    - 간단한 비지니스 모델 구현
- repository
    - DB와 직접적으로 통신하면서 데이터를 읽고/쓰는 레이어

![스크린샷 2022-10-17 오후 7.59.48.png](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/3a9f86f9-24f6-4505-aeb6-2ce0fa89523c/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2022-10-17_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_7.59.48.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20221017%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20221017T130324Z&X-Amz-Expires=86400&X-Amz-Signature=0c6dcb95791af311584ec18ef458e6441fb8fe9e015fc99a157e2db2a5aad34c&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22%25E1%2584%2589%25E1%2585%25B3%25E1%2584%258F%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25B5%25E1%2586%25AB%25E1%2584%2589%25E1%2585%25A3%25E1%2586%25BA%25202022-10-17%2520%25E1%2584%258B%25E1%2585%25A9%25E1%2584%2592%25E1%2585%25AE%25207.59.48.png%22&x-id=GetObject)

# 고려한 점

1. 프로젝트 규모가 커진다고 가정할 때, 자주 반복될 것으로 예상되는 코드는 재사용이 가능하도록 설계
2. readme와 swagger를 이용하여, 프로젝트를 상세하게 설명
3. 구현할 로직이 비교적 간단하고, API에 비지니스 로직이 거의 없기 때문에, TDD로 구현하지 않되, repository 레이어의 기능은 Unit test를 통해 검증

# 구현 내용

- [x]  채용공고 등록
- [x]  채용공고 수정
- [x]  채용공고 삭제
- [x]  채용공고 목록조회
- [x]  채용공고 상세조회
- [x]  채용공고 지원