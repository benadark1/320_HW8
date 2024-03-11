"""
Module for all database models related to social network
"""
# pylint: disable= R0903
from peewee import SqliteDatabase, Model, CharField, ForeignKeyField
from playhouse.dataset import DataSet

sqlite = SqliteDatabase('social_media.db', pragmas={'foreign_keys': 1})
sqlite.connect()


class BaseModel(Model):
    """
    BaseModel Class inheriting Peewee Model Class
    """

    class Meta:
        """
        Metaclass setting the parameter of the database to my sqlite database
        """
        database = sqlite


class UsersTable(BaseModel):
    """
    UserTable class inheriting from BaseModel
    """
    user_id = CharField(primary_key=True, max_length=30)
    user_name = CharField(max_length=30)
    user_last_name = CharField(max_length=100)
    user_email = CharField()


class StatusTable(BaseModel):
    """
    Status Table class inheriting from BaseModel
    """
    status_id = CharField(primary_key=True, max_length=30)
    user_id = ForeignKeyField(model=UsersTable, field='user_id',
                              on_delete="CASCADE")
    status_text = CharField()


sqlite.create_tables([UsersTable, StatusTable])

# Making a dataset from Sqlite Database above
dataset = DataSet(sqlite)
Users = dataset['Users']
Status = dataset['Status']
# Setting primary key as user_id and status_id
Users.insert(user_id='test')
Status.insert(status_id='test')
Users.create_index(['user_id'], unique=True)
Status.create_index(['status_id'], unique=True)
# Delete the dummy record afterwards.
Users.delete(user_id='test')
Status.delete(status_id='test')
sqlite.close()
dataset.close()
