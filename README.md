# Back-end


```
0. DRF 폴더에서
1. python -m venv venv 
    - 가상 환경 생성
2. venv\Scripts\activate 
    - 가상 환경 연결
3. pip install -r .\requirements.txt
    - 백엔드 라이브러리 설치
4. python manage.py makemigrations <app-name>
5. python manage.py migrate <app-name>
6. python manage.py createsuperuser 
    - 초기 데이터 입력
7. python manage.py loaddata dummy.json
    - 어드민 계정 생성
8. python manage.py runserver
    - localhost:8000으로 지정되어 서버 실행됨
```