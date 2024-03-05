"""
Module to test user_status_status.py
"""

from unittest import TestCase
from unittest.mock import MagicMock
import user_status


class TestUserStatusFunctions(TestCase):
    """
    Unit test class called Test user_status
    """

    def setUp(self):
        """
        Setup method to run before
        """
        self.dataset_table = MagicMock()
        self.test_data = {'user_id': 'ben24', 'user_name': 'John', 'last_name': 'Kuper'}

    # Testing add_status method
    def test_add_status_table(self):
        """
        test for add user table method
        """

        test_data = {
            'status_id': 'ben241253',
            'user_id': 'ben24',
            'status_text': 'yoooo'
        }
        # Call the function being tested
        status_add = user_status.add_status_table(self.dataset_table)
        status_add(**test_data)
        # Assert that insert method was called with correct arguments
        self.dataset_table.insert.assert_called_once_with(**test_data)

    # Testing modify_status method
    def test_update_status_table(self):
        """
        test for modify user method table
        """
        test_data = {
            'status_id': 'ben241253',
            'user_id': 'ben24',
            'status_text': 'yoooo'
        }
        # Call the function being tested
        status_update = user_status.update_status_table(self.dataset_table)
        status_update(**test_data)
        # Assert that insert method was called with correct arguments
        self.dataset_table.update.assert_called_once_with(**test_data)

    # Testing delete_status method
    def test_delete_status_table(self):
        """
        test for delete user method
        """
        test_data = {
            'status_id': 'ben241253'
        }
        # Call the function being tested
        status_delete = user_status.delete_status_table(self.dataset_table)
        status_delete(**test_data)
        # Assert that insert method was called with correct arguments
        self.dataset_table.delete.assert_called_once_with(**test_data)

    # Testing search_status method
    def test_search_status_table(self):
        """
        test for search user method
        """
        test_data = {
            'status_id': 'ben241253'
        }
        # Call the function being tested
        status_search = user_status.search_status_table(self.dataset_table)
        status_search(**test_data)
        # Assert that insert method was called with correct arguments
        self.dataset_table.find_one.assert_called_once_with(**test_data)
