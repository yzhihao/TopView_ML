#Python 爬虫笔记 json
在python2.7中貌似已经自带了json库，所以这一次我们可以省略掉安装步骤，直接
`import json`
json是一种轻量级的数据交换格式，在语法上与javascript对象的代码相同，之所以在这里写这个东西，是因为在抓取动态网页时，我们往往要和这个东西打交道。
json作为一种对象，在python中其实是以dict形式存在的，有时候也会是list形式，像下面这样
```
json_obj1={'key1':'value1','key2':'value2'}
#dict形式
json_obj2=['value1','value2','value3']
#list形式
```
这也就意味着，json在python中是可以像dict或者list一样处理的，包括使用它们的方法，或者进行迭代，甚至于，直接打印json对象的类型时，我们都可以看见，他的类型是以dict或者list类存在的。
```
print type(json_obj1)
>> 'dict'
print type(json_obj2)
>> 'list'
```
不仅如此，我们还可以用json模块自带的方法将python对象转化为json对象
```
json_str=json.dumps(json_obj1)
print type(json_str)
>> 'str'
```
或者将json对象转化成python对象
```
json_str2="{'key1':'value1'}"
json_obj3=json.loads(json_str2)
print type(json_obj3)
>> 'dict'
```
也就意味着哪怕我们不用json的时候，也可以把那些长的像dict一样的字符串转化成dict类型，话是这么说，不和json打交道的时候应该也没有人会去创造那种字符串就是了。