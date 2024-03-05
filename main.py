"""
main driver for a simple social network project
"""
# pylint: disable=C0200
# pylint: disable=R0912
# pylint: disable=R1710

import csv
from datetime import datetime
import logging

from peewee import IntegrityError

import users
import user_status
from socialnetwork_model import Users, Status

# Setting Up Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Tweak the format
formatter = logging.Formatter(
    "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
)
# Create output file_handler that writes to a file that changes name every day
file_handler = logging.FileHandler(
    filename=f"log_{datetime.now():%m_%d_%Y}.log"
)
# file_handler will be set to DEBUG
file_handler.setLevel(logging.DEBUG)
# file_handler will use our custom formatter
file_handler.setFormatter(formatter)
# Add file_handler to our logger
logger.addHandler(file_handler)


def load_users(filename):
    """
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    """
    try:
        with open(filename, 'r', encoding='UTF-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if "" in row.values():
                    fin_bool = False
                    break

                try:
                    user_id = row['USER_ID']
                    email = row['EMAIL']
                    user_name = row['NAME']
                    user_last_name = row['LASTNAME']
                    try:
                        user_insert = users.add_user_table(Users)
                        user_insert(user_id=user_id, email=email,
                                    user_name=user_name, user_last_name=user_last_name)
                        fin_bool = True
                        logger.info("New user with id %s was loaded successfully ", user_id)
                    except IntegrityError:
                        fin_bool = False
                        logger.error("Failed to load user with id %s", user_id)
                except KeyError:
                    print('Parameter omitted in csv file!')
                    return False
        return fin_bool
    except FileNotFoundError:
        print('File Not Found')
        return False


def validate_parameters(parameter, parameter_option):
    """
    validates user_id, email, user_name and user_last_name
    """
    if isinstance(parameter, str) and isinstance(parameter_option, str):
        if parameter_option.lower().strip() in ['user_id', 'user_name',
                                                'status_id', 'status_text', 'email']:
            param_check = parameter.strip().replace(' ', '')
            if '-' in parameter:
                param_check = param_check.replace('-', '')

            if '_' in parameter:
                param_check = param_check.replace('_', '')

            if (parameter_option.lower().strip() == 'user_id'
                    or parameter_option.lower().strip() == 'status_id'
                    and '.' in param_check):
                param_check = param_check.replace('.', '')

            if parameter_option.lower().strip() == 'email' and '@' in param_check:
                if '.' in param_check:
                    param_check = param_check.replace('.', '')
                param_check = param_check.replace('@', '')

            if (parameter_option.lower().strip() in ['user_id', 'user_name'] and
                    len(param_check) > 30 or
                    parameter_option.lower().strip() == 'user_last_name' and
                    len(param_check) > 100):
                logger.error("Length constraint violated for %s", parameter_option.lower().strip())
                return False
            if param_check.isalnum():
                return True

        return False

    if isinstance(parameter, list) and isinstance(parameter_option, list):
        out = []
        for index in range(len(parameter)):
            if parameter_option[index].lower().strip() in ['user_id', 'user_name',
                                                           'status_id', 'status_text',
                                                           'email', 'user_last_name']:
                param_check = parameter[index].strip().replace(' ', '')
                if '-' in param_check:
                    param_check = param_check.replace('-', '')

                if '_' in param_check:
                    param_check = param_check.replace('_', '')

                if (parameter_option[index].lower().strip() == 'user_id' or
                        parameter_option[index].lower().strip() == 'status_id'
                        and '.' in param_check):
                    param_check = param_check.replace('.', '')

                if parameter_option[index].lower().strip() == 'email' and '@' in param_check:
                    if '.' in param_check:
                        param_check = param_check.replace('.', '')
                    param_check = param_check.replace('@', '')
                if (parameter_option[index].lower().strip() in ['user_id', 'user_name'] and
                        len(param_check) > 30 or
                        parameter_option[index].lower().strip() == 'user_last_name' and
                        len(param_check) > 100):
                    logger.error("Length constraint violated for %s",
                                 parameter_option[index].lower().strip())
                    out.append(False)
                if param_check.isalnum():
                    out.append(True)
                else:
                    out.append(False)
        if all(out):
            return True
        return False


def load_status_updates(filename):
    """
    Opens a CSV file with status data and adds it to an existing
    instance of UserStatusCollection

    Requirements:
    - If a status_id already exists, it will ignore it and continue to
      the next.
    - Returns False if there are any errors(such as empty fields in the
      source CSV file)
    - Otherwise, it returns True.
    """
    try:
        with open(filename, 'r', encoding='UTF-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if "" in row.values():
                    fin_bool = False
                    break

                try:
                    status_id = row['STATUS_ID']
                    user_id = row['USER_ID']
                    status_text = row['STATUS_TEXT']
                    try:
                        user_insert = users.add_user_table(Users)
                        user_insert(user_id=user_id)
                        logger.error("No user exist for status with status id: %s d", status_id)
                        Users.delete(user_id=user_id)
                        fin_bool = False
                    except IntegrityError:
                        try:
                            status_insert = user_status.add_status_table(Status)
                            status_insert(status_id=status_id, user_id=user_id,
                                          status_text=status_text)
                            logger.info("New status with status id: %s was added successfully",
                                        status_id)
                            fin_bool = True
                        except IntegrityError:
                            logger.error("Failed to add new status with status id: %s", status_id)
                            fin_bool = False

                except KeyError:
                    print('Parameter omitted in csv file!')
                    return False
        return fin_bool
    except FileNotFoundError:
        print('File Not Found')
        return False


def add_user(user_id, email, user_name, user_last_name):
    """
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_user() returns False).
    - Otherwise, it returns True.
    """
    d_bool = validate_parameters([user_id, email, user_name, user_last_name],
                                 ['user_id', 'email', 'user_name', 'user_last_name'])
    if d_bool:
        try:
            user_insert = users.add_user_table(Users)
            user_insert(user_id=user_id, email=email, user_name=user_name,
                        user_last_name=user_last_name)
            logger.info("New user with id %s was added successfully ", user_id)
            return True

        except IntegrityError:
            logger.error("Failed to add new user with id %s", user_id)
            return False
    return d_bool


def update_user(user_id, email, user_name, user_last_name):
    """
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    """
    d_bool = validate_parameters([user_id, email, user_name, user_last_name],
                                 ['user_id', 'email', 'user_name', 'user_last_name'])
    if d_bool:
        if Users.find_one(user_id=user_id) is not None:
            user_update = users.update_user_table(Users)
            user_update(user_id=user_id, email=email, user_name=user_name,
                        user_last_name=user_last_name, columns=['user_id'])
            logger.info("User(%s) information was modified successfully", user_id)
            return True

        logger.error("Couldn't find to user with id %s to update!", user_id)
        return False
    return d_bool


def delete_user(user_id):
    """
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    """
    d_bool = validate_parameters(user_id, 'user_id')
    if d_bool:
        if Users.find_one(user_id=user_id) is not None:
            user_delete = users.delete_user_table(Users)
            user_delete(user_id=user_id)
            if Status.find_one(user_id=user_id) is not None:
                # Deleting all status associated with user with user_id
                Status.delete(user_id=user_id)
            logger.info("User(%s) information was deleted successfully", user_id)
            return True

        logger.error("Couldn't find to user with id %s to delete!", user_id)
        return False
    return d_bool


def search_user(user_id):
    """
    Searches for a user in user_collection(which is an instance of
    UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    """
    d_bool = validate_parameters(user_id, 'user_id')
    if d_bool:
        user_find = users.search_user_table(Users)
        fin_bool = user_find(user_id=user_id)
        return fin_bool
    return None


def add_status(status_id, user_id, status_text):
    """
    Creates a new instance of UserStatus and stores it in
    user_collection(which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_status() returns False).
    - Otherwise, it returns True.
    """
    d_bool = validate_parameters([user_id, status_id, status_text],
                                 ['user_id', 'status_id', 'status_text'])
    if d_bool:
        try:
            user_insert = users.add_user_table(Users)
            user_insert(user_id=user_id)
            logger.error("No user with user id:%s exist for status with status id: %s ",
                         user_id, status_id)
            Users.delete(user_id=user_id)
            return False
        except IntegrityError:
            try:
                status_insert = user_status.add_status_table(Status)
                status_insert(status_id=status_id, user_id=user_id, status_text=status_text)
                logger.info("New status with status id: %s was added successfully", status_id)

                return True
            except IntegrityError:
                logger.error("Failed to add new status with status id: %s", status_id)
                return False
    return d_bool


def update_status(status_id, user_id, status_text):
    """
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there are any errors.
    - Otherwise, it returns True.
    """
    d_bool = validate_parameters([user_id, status_id, status_text],
                                 ['user_id', 'status_id', 'status_text'])
    if d_bool:
        if Users.find_one(user_id=user_id) is not None:
            if Status.find_one(status_id=status_id) is not None:
                status_update = user_status.update_status_table(Status)
                status_update(status_id=status_id, status_text=status_text, columns=['status_id'])
                logger.info("User(%s) status information with status id:"
                            "%s was modified successfully",
                            user_id, status_id)
                return True
            logger.error("Couldn't find to status with id %s to update status information!",
                         status_id)
            return False

        logger.error("Couldn't find to user with id %s to update !", user_id)
        return False
    return d_bool


def delete_status(status_id):
    """
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    """
    d_bool = validate_parameters(status_id, 'status_id')
    if d_bool:
        if Status.find_one(status_id=status_id) is not None:
            status_delete = user_status.delete_status_table(Status)
            status_delete(status_id=status_id)
            logger.info("Status(%s) information was deleted successfully", status_id)
            return True

        logger.error("Couldn't find to status with id %s to delete!", status_id)
        return False
    return d_bool


def search_status(status_id):
    """
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    """
    d_bool = validate_parameters(status_id, 'status_id')
    if d_bool:
        status_find = user_status.search_status_table(Status)
        fin_bool = status_find(status_id=status_id)
        return fin_bool
    return None
