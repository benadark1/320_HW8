"""
Classes to manage the user status messages
Modified to work with Database
"""
# pylint: disable=R0903
# pylint: disable=W1203
# pylint: disable=R0801
# pylint: disable=C0116

from socialnetwork_model import dataset


def add_status_table(db):
    def add_status(**kwargs):
        with dataset.transaction():
            db.insert(**kwargs)

    return add_status


def update_status_table(db):
    def update_status(**kwargs):
        with dataset.transaction():
            db.update(**kwargs)

    return update_status


def delete_status_table(db):
    def delete_status(**kwargs):
        with dataset.transaction():
            db.delete(**kwargs)

    return delete_status


def search_status_table(db):
    def search_status(**kwargs):
        with dataset.transaction():
            return db.find_one(**kwargs)

    return search_status

