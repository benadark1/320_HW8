"""
Module to test main.py
"""
# pylint: disable=C0301
import io
from unittest.mock import patch, Mock, mock_open
from unittest import TestCase
from peewee import SqliteDatabase
from socialnetwork_model import StatusTable, UsersTable, Status, Users
from playhouse.dataset import DataSet
import main


class TestMain(TestCase):
    """
    Unit test class called TestMain
    """

    def setUp(self):
        self.sqlite = SqliteDatabase(':memory:', pragmas={"foreign_keys": 1})
        self.sqlite.bind([StatusTable, UsersTable])
        self.sqlite.connect()
        self.sqlite.create_tables([StatusTable, UsersTable])
        self.dataset = DataSet(self.sqlite)
        self.Users = Users
        self.Status = Status

    def tearDown(self):
        self.sqlite.drop_tables([StatusTable, UsersTable])
        self.sqlite.close()
        self.Users.delete()
        self.Status.delete()
        self.dataset.close()

    def test_validate_parameters(self):
        """
        test validate_parameters method
        """
        tests = (
            ('badark07', 'user_id', True),
            ('badark070000000000000000000000000',
             'user_id', False),
            ('badark070000000000000000000000000',
             'user_name', False),
            ('badark_07', 'status_id', True),
            ('ben@uw.edu', 'email', True),
            ('[adark@07', 'email', False),
            (['[adark@07', 'badark@07'], ['email', 'email'], False),
            (['b01', 'badark@07', 'Ben', 'Adark'], ['user_id', 'email', 'user_name', 'user_last_name'], True)
        )
        for test in tests:
            expected_output = test[2]
            self.assertEqual(main.validate_parameters(test[0], test[1]),
                             expected_output)

    def test_load_users(self):
        """
        test load_users method
        """
        tests = (
            # Missing parameter test case
            ([
                 {"USER_ID": "John", "EMAIL": "Doe", "NAME": "student"},
                 {"USER_ID": "Jane", "EMAIL": "Smith", "NAME": "student", "LASTNAME": "Doe2"},
                 {"USER_ID": "Doe", "EMAIL": "John", "NAME": "student", "LASTNAME": "Doe3"},
                 {"USER_ID": "Smith", "EMAIL": "Jane", "NAME": "student", "LASTNAME": "Doe4"},
             ], False),
            # Working test case
            ([
                 {"USER_ID": "John", "EMAIL": "Doe", "NAME": "student1", "LASTNAME": "Doe1"},
                 {"USER_ID": "Jane", "EMAIL": "Smith", "NAME": "student2", "LASTNAME": "Doe2"},
                 {"USER_ID": "Doe", "EMAIL": "John", "NAME": "student3", "LASTNAME": "Doe3"},
                 {"USER_ID": "Smith", "EMAIL": "Jane", "NAME": "student4", "LASTNAME": "Doe4"},
             ], True),
            # Multiple row test case
            ([
                 {"USER_ID": "John", "EMAIL": "Doe", "NAME": "student", "LASTNAME": "Doe1"},
                 {"USER_ID": "John", "EMAIL": "Doe", "NAME": "student", "LASTNAME": "Doe1"},
                 {"USER_ID": "Jane", "EMAIL": "Smith", "NAME": "student", "LASTNAME": "Doe2"},
                 {"USER_ID": "Doe", "EMAIL": "John", "NAME": "student", "LASTNAME": "Doe3"},
                 {"USER_ID": "Smith", "EMAIL": "Jane", "NAME": "student", "LASTNAME": "Doe4"},
             ], False),
            # Empty parameter test
            ([
                 {"USER_ID": "John", "EMAIL": "Doe", "NAME": "student", "LASTNAME": ""},
                 {"USER_ID": "John", "EMAIL": "Doe", "NAME": "student", "LASTNAME": "Doe1"},
                 {"USER_ID": "Jane", "EMAIL": "Smith", "NAME": "student", "LASTNAME": "Doe2"},
                 {"USER_ID": "Doe", "EMAIL": "John", "NAME": "student", "LASTNAME": "Doe3"},
                 {"USER_ID": "Smith", "EMAIL": "Jane", "NAME": "student", "LASTNAME": "Doe4"},
             ], False)
        )
        test_counter = 0
        for test in tests:
            mock_dict_reader1 = Mock(
                # Setting return value of mocked method to iterable list of dictionary
                return_value=iter(test[0])
            )
            expected_output = test[1]
            with patch('main.csv.DictReader', mock_dict_reader1):
                self.assertEqual(main.load_users(filename='accounts1.csv'),
                                 expected_output)
                if test_counter < 1:
                    self.assertFalse(main.load_users(filename='ccounts.csv'))
                    test_counter += 1
        # Testing file not found error
        with (
            patch("sys.stdout", new_callable=io.StringIO) as mock_stdout,
            patch("main.csv.open", mock_open()) as mock_file,
        ):
            mock_file.side_effect = FileNotFoundError
            main.load_users("accouns.csv")
            self.assertEqual(
                mock_stdout.getvalue().strip().split("\n"), ["File Not Found"]
            )

    def test_load_status_updates(self):
        """
        test load_status_updates method
        """
        main.add_user('John01', 'J1@u.edu', 'John1', 'Breezy1')
        main.add_user('John02', 'J2@u.edu', 'John2', 'Breezy2')
        main.add_user('John03', 'J3@u.edu', 'John3', 'Breezy3')
        tests = (
            # Working test case
            ([
                 {"STATUS_ID": "John97_001", "USER_ID": "John01", "STATUS_TEXT": "Heyo"},
                 {"STATUS_ID": "John98_001", "USER_ID": "John02", "STATUS_TEXT": "Heyo there"},
                 {"STATUS_ID": "John99_001", "USER_ID": "John03", "STATUS_TEXT": "Heyo you there"}
             ], True),
            # Missing parameter test case
            ([
                 {"STATUS_ID": "John97_001", "USER_ID": "John01"},
                 {"STATUS_ID": "John98_001", "USER_ID": "John02", "STATUS_TEXT": "Heyo there"},
                 {"STATUS_ID": "John99_001", "USER_ID": "John03", "STATUS_TEXT": "Heyo you there"}
             ], False),
            # Multiple row test case
            ([
                 {"STATUS_ID": "John97_001", "USER_ID": "John01", "STATUS_TEXT": "Heyo"},
                 {"STATUS_ID": "John98_001", "USER_ID": "John02", "STATUS_TEXT": "Heyo there"},
                 {"STATUS_ID": "John98_001", "USER_ID": "John02", "STATUS_TEXT": "Heyo there"},
                 {"STATUS_ID": "John98_002", "USER_ID": "John02", "STATUS_TEXT": "Heyo there"},
                 {"STATUS_ID": "John99_001", "USER_ID": "John03", "STATUS_TEXT": "Heyo you there"}
             ], False),
            # Empty parameter test
            ([
                 {"STATUS_ID": "John97_001", "USER_ID": "John01", "STATUS_TEXT": ""},
                 {"STATUS_ID": "John98_001", "USER_ID": "John02", "STATUS_TEXT": "Heyo there"},
                 {"STATUS_ID": "John98_001", "USER_ID": "John02", "STATUS_TEXT": "Heyo there"},
                 {"STATUS_ID": "John98_002", "USER_ID": "John02", "STATUS_TEXT": "Heyo there"},
                 {"STATUS_ID": "John99_001", "USER_ID": "John03", "STATUS_TEXT": "Heyo you there"}
             ], False)
        )
        test_counter_1 = 0
        mock_counter = 0
        for test in tests:
            mock_dict_reader1 = Mock(
                # Setting return value of mocked method to iterable list of dictionary
                return_value=iter(test[0])
            )
            mock_bool = [True, False, False, False]
            mock_user_status_add_status = Mock(return_value=mock_bool[mock_counter])
            mock_counter += 1
            expected_output = test[1]
            with patch('main.csv.DictReader', mock_dict_reader1):
                self.assertEqual(main.load_status_updates(filename='status_updates1.csv'),
                                 expected_output)
                if test_counter_1 < 1:
                    self.assertFalse(main.load_status_updates(filename='tatus_updates.csv'))

                    test_counter_1 += 1
        # Testing file not found error
        with (
            patch("sys.stdout", new_callable=io.StringIO) as mock_stdout,
            patch("main.open", mock_open()) as mock_file,
        ):
            mock_file.side_effect = FileNotFoundError
            main.load_users("astatus_updates.csv")
            self.assertEqual(
                mock_stdout.getvalue().strip().split("\n"), ['File Not Found']
            )

    def test_add_user(self):
        """
        test add_user method
        """
        tests = (
            ('adark_01', 'adark@uw.edu', 'aarol', 'adark', True),
            ('adark_01', 'adark@uw.edu', 'aarol', 'adark', False),
            ('adark_02', 'adark@uw.edu', 'aarol', 'adark', True),
            ('adark_02', 'adark@uw.edu', 'aarol', 'adark', False),
            ('dadark_04', 'dadark@uw.edu', 'darol', 'dadark', True),
            ('dabark_040000000000000000000000000000000000000000',
             'dadark@uw.edu', 'darol', 'dadark', False),
            ("John", "Doe", "student", "Doe1", True),
            ("Jane", "Smith", "student", "Doe2", True),
            ("Doe", "John", "student", "Doe3", True),
            ("Smith", "Jane", "student", "Doe4", True),
        )
        for test in tests:
            expected_output = test[4]
            self.assertEqual(main.add_user(test[0], test[1], test[2],
                                           test[3]), expected_output)

    def test_update_user(self):
        """
        test update_user method
        """
        main.add_user('adark_01', 'adark@uw.edu', 'aarol', 'adark', )
        tests = (
            ('adark_01', 'adark1@uw.edu', 'aarol1', 'adark1', True),
            ('dadark_04', 'dadark@uw.edu', 'darol', 'dadark', False),
            ('dabark_040000000000000000000000000000000000000000',
             'dadark@uw.edu', 'darol', 'dadark', False),
        )
        for test in tests:
            expected_output = test[4]
            self.assertEqual(main.update_user(test[0], test[1], test[2],
                                              test[3]), expected_output)

    def test_delete_user(self):
        """
        test delete_user method
        """
        main.add_user('adark_01', 'adark@uw.edu', 'aarol', 'adark', )

        tests = (
            ('adark_05', False),
            ('adark_01', True),
            ('dabark_040000000000000000000000000000000000000000',
             False),
        )
        for test in tests:
            expected_output = test[1]
            self.assertEqual(main.delete_user(test[0]), expected_output)

    def test_search_user(self):
        """
        test search_user method
        """
        main.add_user('adark_01', 'adark@uw.edu', 'aarol', 'adark', )
        main.add_user('badark_02', 'badark@uw.edu', 'barol', 'badark')
        tests_1 = (
            ('adark_01', ['adark_01', 'adark@uw.edu', 'aarol', 'adark']),
            ('badark_02', ['badark_02', 'badark@uw.edu', 'barol', 'badark'])
        )
        for test in tests_1:
            expected_output = test[1]
            actual_output = main.search_user(test[0])
            self.assertEqual([actual_output['user_id'], actual_output['email'],
                              actual_output['user_name'],
                              actual_output['user_last_name']], expected_output)

        # Testing for user not in database
        self.assertEqual(main.search_user('adark05.1'), None)

    def test_add_status(self):
        """
       test add_status method
        """
        temp_data = (
            ('adark', 'adark@uw.edu', 'aarol', 'adark1'),
            ('badark', 'badark@uw.edu', 'barol', 'badark2'),
            ('cadark', 'cadark@uw.edu', 'carol', 'cadark3')
        )
        for data in temp_data:
            main.add_user(data[0], data[1], data[2], data[3])
        tests = (
            ('4', 'adark', 'Imperfect weather today', True),
            ('4', 'dadark', 'Imperfect weather today', False),
            ('2', 'badark', 'Perfect weather yesterday', True),
            ('2', 'badark', 'Perfect weather yesterday', False),
            ('5', 'cadark', 'I will make it through today', True),
            ('6', 'badark', 'I will make NOT it through today', True),
            ('7', 'badark', 'I will make NOT it through today', True)
        )
        for test in tests:
            expected_output = test[3]
            self.assertEqual(main.add_status(test[0], test[1],
                                             test[2]), expected_output)
            if test[3]:
                result = main.search_user(test[1])
                self.assertIsNotNone(result)
                self.assertEqual(result['user_id'], test[1])

    def test_update_status(self):
        """
        test update_status method
        """
        temp_data = (
            ('adark', 'adark@uw.edu', 'aarol', 'adark1'),
            ('badark', 'badark@uw.edu', 'barol', 'badark2'),
            ('cadark', 'cadark@uw.edu', 'carol', 'cadark3')
        )
        for data in temp_data:
            main.add_user(data[0], data[1], data[2], data[3])
        temp_data_2 = (
            ('1', 'adark', 'Perfect weather today'),
            ('2', 'badark', 'Perfect weather yesterday'),
            ('3', 'cadark', 'Perfect weather tomorrow'),
        )
        for data in temp_data_2:
            main.add_status(data[0], data[1], data[2])
        tests = (
            ('1', 'badark', 'Perfect weather today', True),
            ('5', 'badark', 'Perfect weather today', False),
            ('20', 'nadark', 'I will make it through today', False),
            ('2', 'nadark', 'I will make it through today', False),
            ('2', 'adark', 'I will make NOT it through today', True),
            ('3', 'adark', 'I will make NOT it through today', True)
        )
        for test in tests:
            expected_output = test[3]
            self.assertEqual(main.update_status(test[0], test[1],
                                                test[2]), expected_output)

    def test_delete_status(self):
        """
        test_delete_status method
        """
        main.add_user('adark', 'adark@uw.edu', 'aarol', 'adark1')
        main.add_status('1', 'adark', 'Perfect weather today')
        tests = (
            ('4', False),
            ('1', True)
        )
        for test in tests:
            expected_output = test[1]
            self.assertEqual(main.delete_status(test[0]), expected_output)

    def test_search_status(self):
        """
        test_search_status method
        """
        temp_data = (
            ('adark', 'adark@uw.edu', 'aarol', 'adark1'),
            ('badark', 'badark@uw.edu', 'barol', 'badark2'),
            ('cadark', 'cadark@uw.edu', 'carol', 'cadark3')
        )
        for data in temp_data:
            main.add_user(data[0], data[1], data[2], data[3])
        temp_data_2 = (
            ('1', 'adark', 'Perfect weather today'),
            ('2', 'badark', 'Perfect weather yesterday'),
            ('3', 'cadark', 'Perfect weather tomorrow'),
        )
        for data in temp_data_2:
            main.add_status(data[0], data[1], data[2])
        tests = (
            ('1', ['1', 'adark', 'Perfect weather today']),
            ('2', ['2', 'badark', 'Perfect weather yesterday'])
        )
        for test in tests:
            expected_output = test[1]
            expected_output[1] = main.search_user(test[1][1])['user_id']
            actual_output = main.search_status(test[0])
            self.assertEqual([actual_output['status_id'], actual_output['user_id'],
                              actual_output['status_text'],
                              ], expected_output)
        # Test for non existent status
        self.assertIsNone(main.search_status('4'))
