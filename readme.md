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