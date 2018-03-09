class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        print('Found model: %s' % name)
        mappings = dict()
        for k,v in attrs.items():  #这里的attrs又是什么东西？（keys,value?），打印k,v会得到什么
            if isinstance(v,Field):
                print('Found mapping: %s ==> %s' % (k,v))
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)   #把User类下的字典{'id': 'IntegerField('id')'}删掉了,即删了id = IntegerField('id')，删掉的改存在mappings这个字典里
            attrs['__mappings__'] = mappings #这里需打印一下attrs和attrs['__mappings__']看看是什么？  ？？？
            attrs['__table__'] = name
            return type.__new__(cls,name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self,**kw): # **kw的意思还有巩固一下
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AssertionError(r"'Model' object has no attribute '%s'" % key)

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' %(self.__table__,','.join(fields),','.join(params))

        print('SQL:%s' %sql)
        print('ARGS: %s' % str(args))

class Field(object):

    def __init__(self,name,column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)  #(类实例所属类的名字，实例的名字)  ？？？

class StringField(Field):

    def __init__(self,name):
        super(StringField, self).__init__(name,'varchar(100)')

class IntegerField(Field):
    def __init__(self,name):
        super(IntegerField,self).__init__(name, 'bigint')


class User(Model):
    #定义类的属性到列的映射
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')

# #创建一个实例：
# u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
# #保存到数据库
# u.save()





u = User(id=1234, name='zbc', email='as@qwe', password='my-pwd')
u.save()





