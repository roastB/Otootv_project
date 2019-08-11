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

## 언어 생생
처음 프로젝트를 시작할 때만 적용하는 명령어이므로, 현재는 project 내부의 locale을 복사하여 사용하시기 바랍니다.

명령어는 단순한 참고용입니다.
```
 python manage.py makemessages -l ko  
 python manage.py makemessages -l en  
 python manage.py compilemessages
 ```
 
 ## 카테고리 생성
 ```
python manage.py shell  
from vod.models import Category  
get = lambda node_id: Category.objects.get(pk=node_id)  
root = Category.add_root(name='Category')

node = get(root.pk).add_child(name='Education')  
node1 = get(node.pk).add_child(name='Elementary School')  
get(node1.pk).add_child(name='English')  
get(node1.pk).add_child(name='Korean')  
get(node1.pk).add_child(name='Math')  
get(node1.pk).add_child(name='Science')  
get(node1.pk).add_child(name='ETC')

node1 =get(node.pk).add_child(name='Middle School')  
get(node1.pk).add_child(name='English')  
get(node1.pk).add_child(name='Korean')
get(node1.pk).add_child(name='Math')  
get(node1.pk).add_child(name='Science')  
get(node1.pk).add_child(name='SSAT')  
get(node1.pk).add_child(name='ETC')

node1 =get(node.pk).add_child(name='High school')  
get(node1.pk).add_child(name='English')  
get(node1.pk).add_child(name='Korean')  
get(node1.pk).add_child(name='Math')  
get(node1.pk).add_child(name='Science')  
get(node1.pk).add_child(name='SAT')  
get(node1.pk).add_child(name='ACT')  
get(node1.pk).add_child(name='ETC')

node1 =get(node.pk).add_child(name='General')  
get(node1.pk).add_child(name='TOEIC'')  
get(node1.pk).add_child(name='TOEFL')  
get(node1.pk).add_child(name='TEPS')  
get(node1.pk).add_child(name='Science')  
get(node1.pk).add_child(name='ETC')  
get(node.pk).add_child(name='Sky Castle')

node = get(root.pk).add_child(name='Travel')   
get(node.pk).add_child(name='North America')  
get(node.pk).add_child(name='South America')  
get(node.pk).add_child(name='Europe')  
get(node.pk).add_child(name='Australia'')  
get(node.pk).add_child(name='ETC')
```


## 라이브러리 변경
```
프로젝트\venv\프로젝트\Lib\site-packages\django_summernote\modles
프로젝트\venv\프로젝트\Lib\site-packages\django_summernote\admin
```

라이브러리 summernote attachment 모델에 필드 추가가 필요해서 변경 하였습니다. 
프로젝트 lib_change 폴더안 코드, 주석 제거하고 적용 해주세요 