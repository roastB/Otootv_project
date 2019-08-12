## version
Windows 10  
Pycharm: 2019.1.2    
python: 3.7  
Django: 2.1.7
MariaDB :10.4

## package
```
requirements.txt  
pip freeze > requirements.txt  
pip install -r requirements.txt
```

## group 생성 
현재 groupcreate 사용은 보류되어 있습니다.
```
python manage.py creategroup
```

## 장고 내부 번역
https://docs.djangoproject.com/en/2.2/topics/i18n/translation/#how-django-discovers-language-preference  
 
```
 python manage.py makemessages -l ko  
 python manage.py makemessages -l en  
 python manage.py compilemessages
 ```
 
 python manage.py makemessages -l : 번역 파일 생성(계속 업데이트 가능)  
 python manage.py compilemessages : 번역 적용(세션 다시시작)
 
 1. 요청 된 URL에서 언어 접두사를 찾습니다.(i18n_patterns루트 URLconf에서 함수를 사용하는 경우에만 수행된다)    
 2.  현재 사용자 세션에서 LANGUAGE_SESSION_KEY 키를 찾습니다 .    
 3. 쿠키를 찾습니다 (사용 된 쿠키의 이름은 LANGUAGE_COOKIE_NAME의해 설정 (기본 이름은 django_language))    
 4. Accept-LanguageHTTP 헤더를 봅니다 .(이 헤더는 브라우저에서 전송되며 우선 순위에 따라 원하는 언어를 서버에 알려줍니다.
Django는 사용 가능한 번역이있는 언어를 찾을 때까지 헤더의 각 언어를 시도합니다.)  
 5. 전역 LANGUAGE_CODE설정을 사용합니다 .


 ## 모델 내용 번역 
 https://django-modeltranslation.readthedocs.io/en/latest/usage.html
 
 영어가 기본 언어
 세션이 영어면 modle field 에서 영어 호출, 한국어면 한국어 호출
 
 field 저장 -> field_ko, field_en 자동 복사 저장  
 ```
 ex)  
 Notice.objects.create(title = "1")  
 field=1,  field_ko=1,  field_en=1  
 Notice.objects.create(title_en = "1", title_ko="2")  
  field=1,  field_ko=1,  field_en=2
  ```
  
 fied 내용 -> field_en 저장 명령어  
 ```
 python manage.py update_translation_fields
 ```

 ## 카테고리 생성
django-modeltranslation을 적용해 영어 한국어 가능
 
 영어 한국어 동시 생성
 ```
python manage.py shell  
from vod.models import Category  
get = lambda node_id: Category.objects.get(pk=node_id)  
root = Category.add_root(name='Category', name_ko='카테고리')

node = get(root.pk).add_child(name='Education', name_ko='교육')  
node1 = get(node.pk).add_child(name='Elementary School', name_ko='초등학교')  
get(node1.pk).add_child(name='English', name_ko='영어')  
get(node1.pk).add_child(name='Korean', name_ko='한국어')  
get(node1.pk).add_child(name='Math', name_ko='수학')  
get(node1.pk).add_child(name='Science', name_ko='과학')  
get(node1.pk).add_child(name='ETC', name_ko='기타')

node1 =get(node.pk).add_child(name='Middle School', name_ko='중학교')  
get(node1.pk).add_child(name='English', name_ko='영어')  
get(node1.pk).add_child(name='Korean', name_ko='한국어')
get(node1.pk).add_child(name='Math', name_ko='수학')  
get(node1.pk).add_child(name='Science', name_ko='과핟')  
get(node1.pk).add_child(name='SSAT')  
get(node1.pk).add_child(name='ETC')

node1 =get(node.pk).add_child(name='High school', name_ko='고등학교')  
get(node1.pk).add_child(name='English', name_ko='영어')  
get(node1.pk).add_child(name='Korean', name_ko='한국어')  
get(node1.pk).add_child(name='Math', name_ko='수학')  
get(node1.pk).add_child(name='Science', name_ko='과학')  
get(node1.pk).add_child(name='SAT')  
get(node1.pk).add_child(name='ACT')  
get(node1.pk).add_child(name='ETC')

node1 =get(node.pk).add_child(name='General', name_ko='일반')  
get(node1.pk).add_child(name='TOEIC'', name_ko='토익')  
get(node1.pk).add_child(name='TOEFL', name_ko='토플')  
get(node1.pk).add_child(name='TEPS', name_ko='텝스')
get(node.pk).add_child(name='Sky Castle', name_ko='스카이 캐슬')    
get(node1.pk).add_child(name='ETC', name_ko='기타')  

node = get(root.pk).add_child(name='Travel', name_ko='여행')   
get(node.pk).add_child(name='North America', name_ko='북아메리카')  
get(node.pk).add_child(name='South America', name_ko='남아메리카')  
get(node.pk).add_child(name='Europe', name_ko='유럽')  
get(node.pk).add_child(name='Australia'', name_ko='호주')  
get(node.pk).add_child(name='ETC', name_ko='기타')

node = get(root.pk).add_child(name='Shopping', name_ko='쇼핑')   
get(node.pk).add_child(name='Accessories', name_ko='악세사지')  
get(node.pk).add_child(name='Shoes', name_ko='신발')  
get(node.pk).add_child(name='ETC', name_ko='기타')
 ```
 
## 라이브러리 변경
```
프로젝트\venv\프로젝트\Lib\site-packages\django_summernote\modles
프로젝트\venv\프로젝트\Lib\site-packages\django_summernote\admin
```

라이브러리 summernote attachment 모델에 필드 추가가 필요해서 변경 하였습니다. 
프로젝트 lib_change 폴더안 코드, 주석 제거하고 적용 해주세요 
 