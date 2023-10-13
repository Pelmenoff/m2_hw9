from peewee import Model, CharField, PostgresqlDatabase

db = PostgresqlDatabase('postgres', user='postgres', password='password', host='localhost')

class BaseModel(Model):
    class Meta:
        database = db

class Author(BaseModel):
    name = CharField(unique=True)

class Quote(BaseModel):
    text = CharField(max_length=4096)
    author = CharField()

db.connect()
db.create_tables([Author, Quote], safe=True)
db.close()