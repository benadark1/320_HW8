"""
Functions for user information for the social network project
Modified to work with Database
"""
# pylint: disable=R0903
# pylint: disable=W1203
# pylint: disable=R0801
# pylint: disable=C0116

from socialnetwork_model import dataset


def add_user_table(db):
    def add_user(**kwargs):
        with dataset.transaction():
            db.insert(**kwargs)

    return add_user


def update_user_table(db):
    def update_user(**kwargs):
        with dataset.transaction():
            db.update(**kwargs)

    return update_user


def delete_user_table(db):
    def delete_user(**kwargs):
        with dataset.transaction():
            db.delete(**kwargs)

    return delete_user


def search_user_table(db):
    def search_user(**kwargs):
        with dataset.transaction():
            return db.find_one(**kwargs)

    return search_user
