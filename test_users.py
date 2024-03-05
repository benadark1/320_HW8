"""
Module to test users.py
"""

from unittest import TestCase
from unittest.mock import MagicMock
import users


class TestUsersFunctions(TestCase):
    """
    Unit test class called TestUsers
    """

    def setUp(self):
        """
        Setup method to run before
        """
        self.dataset_table = MagicMock()

    # Testing add_user method
    def test_add_user_table(self):
        """
        test for add user table method
        """
        test_data = {
            'user_id': 'ben24',
            'email': 'John@uw.edu',
            'user_name': 'John',
            'last_name': 'Kuper'
        }
        # Call the function being tested
        user_add = users.add_user_table(self.dataset_table)
        user_add(**test_data)
        # Assert that insert method was called with correct arguments
        self.dataset_table.insert.assert_called_once_with(**test_data)

    # Testing modify_user method
    def test_update_user_table(self):
        """
        test for modify user method table
        """
        test_data = {
            'user_id': 'ben24',
            'email': 'John@uw.edu',
            'user_name': 'John',
            'last_name': 'Kuper'
        }
        # Call the function being tested
        user_update = users.update_user_table(self.dataset_table)
        user_update(**test_data)
        # Assert that insert method was called with correct arguments
        self.dataset_table.update.assert_called_once_with(**test_data)

    # Testing delete_user method
    def test_delete_user_table(self):
        """
        test for delete user method
        """
        test_data = {
            'user_id': 'ben24'
        }
        # Call the function being tested
        user_delete = users.delete_user_table(self.dataset_table)
        user_delete(**test_data)
        # Assert that insert method was called with correct arguments
        self.dataset_table.delete.assert_called_once_with(**test_data)

    # Testing search_user method
    def test_search_user_table(self):
        """
        test for search user method
        """
        test_data = {
            'user_id': 'ben24'
        }
        # Call the function being tested
        user_search = users.search_user_table(self.dataset_table)
        user_search(**test_data)
        # Assert that insert method was called with correct arguments
        self.dataset_table.find_one.assert_called_once_with(**test_data)
