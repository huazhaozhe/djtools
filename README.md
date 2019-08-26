## Django工具

### 全局对象
Flask中有4个全局对象(request, session, current_app, g), 可以在Flask的很多地方用到而不需要传入
Django本身没有提供这样的工具

关于这个的讨论:
+ [Global Django requests](https://nedbatchelder.com/blog/201008/global_django_requests.html)
+ [Django Copy Flask: 实现Flask中的全局request对象](https://smartkeyerror.com/Django-Copy-Flask-%E5%AE%9E%E7%8E%B0Flask%E4%B8%AD%E7%9A%84%E5%85%A8%E5%B1%80request%E5%AF%B9%E8%B1%A1.html)


有众多的第三方插件实现了:
+ [django-tools ThreadLocal](https://github.com/jedie/django-tools/blob/master/django_tools/middlewares/ThreadLocal.py)
+ [django-globals](https://github.com/svetlyak40wt/django-globals/)
+ ...

这些第三方实现都是基于了threading.local, 不过这是有缺陷的, werkzeug.local [Context Locals](https://werkzeug.palletsprojects.com/en/0.15.x/local/) 中有说明:
>The Python standard library has a concept called “thread locals” (or thread-local data). A thread local is a global object in which you can put stuff in and get back later in a thread-safe and thread-specific way. That means that whenever you set or get a value on a thread local object, the thread local object checks in which thread you are and retrieves the value corresponding to your thread (if one exists). So, you won’t accidentally get another thread’s data.<br>
This approach, however, has a few disadvantages. For example, besides threads, there are other types of concurrency in Python. A very popular one is greenlets. Also, whether every request gets its own thread is not guaranteed in WSGI. It could be that a request is reusing a thread from a previous request, and hence data is left over in the thread local object.

因此参照Flask的全局对象实现, 利用Django的中间件实现了global_request, global_user的全局对象, 外加global_g对象<br>
需要注意的是, 这三个全局对象是和request相关的, 在视图处理request之前生成, 返回response之前销毁, 并且生成和销毁时发送了信号<br>
另外全局request对象push的地方放在了process_view而不是process_request, 这样可以得到request的body


### 实例的更改的历史记录

这个也有几个第三方实现: [django-simple-history](https://github.com/treyhunner/django-simple-history), 使用这些插件必须在每个模型中定义特定字段且需要额外注册步骤

我有遇到一个需求是, 我需要知道是那个request那个用户, 更改了那些实例的那些值, 更改的值之前和之后的值分别是啥<br>
Django的模型中一般得不到request, 或者每次都需要需要传入参数<br>
如果有个东西能在request存在的时间段内检测到所有实例更改, 就可以实现这个需求, 刚好Django db模块有好几个内置信号, 在模型实例发生更改前后可以发送信号, 再和全局g对象联合起来, 需求得到实现

用到的东西:
1. 模型基类继承: 所有用户定义模型均继承自UidBaseModel, 添加一些共用字段
2. 模型Minix: Django不默认提供update_fields值, 因此混入InstanceChangedFieldsMixin, 添加_changed_fields跟踪实例字段值的变化
3. Django信号机制: 模型实例在保存删除前后均有信号, 请求完成信号, 这里使用了自定义信号
4. 全局request和g对象: 在一个request内, 接收模型实例保存删除的信号并得到更改记录, 最终request完成生成记录保存到数据库


### 其他
更改了manage.py, 多个settings配置文件情况下, 需要指定--settings选项, 默认--settings=djtools.settings.base
```python
python manage.py runserver 0:8000 --settings=djtools.settings.local
```
