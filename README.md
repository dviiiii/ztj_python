> 查看django版本
```shell
python -m django --version
```

> 创建对象（项目）
```shell
 django-admin startproject mysite
```

> 启动项目（开发）
```shell
 python manage.py runserver
```


> 创建应用
```shell
 python manage.py startapp hqdba
```

> 创建数据库表
```shell
 python manage.py migrate
```

> 创建数据库表
```shell
 python manage.py migrate
```

> 应用模型文件迁移（修改的部分）
```shell
 python manage.py makemigrations hqdba
```

> 查看要执行的sql
```shell
 python manage.py sqlmigrate hqdba 0001
```

> 修改模型的3个步骤
```shell
 1.编辑 models.py 文件，改变模型。
 2.运行 python manage.py makemigrations 为模型的改变生成迁移文件。
 3.运行 python manage.py migrate 来应用数据库迁移。
```




