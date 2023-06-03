from collections import namedtuple

db_tuple = namedtuple('DB_Selectons', ['id', 'nickname', 'age', 'email', 'password', 'avatar'])
a = db_tuple(1, 'aboba', 22, 'assaf', 'asasdad', None)
print(a.id)
