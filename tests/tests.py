#! python3
# tests.py

import csv
import os
import unittest

class TestDataFilesCorrectlyOrganized(unittest.TestCase):

    def test_directories_in_data(self):
        dirnames = ['Airship', 'MIRAHQ', 'Polus', 'TheSkeld']
        directories = [d for d in os.listdir('data')\
                       if os.path.isdir(os.path.join('data', d))]
        self.assertEqual(dirnames, directories)

    def test_subdirectories_in_directories(self):
        directories = [d for d in os.listdir('data')\
                       if os.path.isdir(os.path.join('data', d))]
        subdirnames = ['actions', 'locations', 'maps', 'tasks', 'vents']
        for directory in directories:
            path = os.path.join('data', directory)
            subdirectories = [sd for sd in os.listdir(path)\
                              if os.path.isdir(os.path.join(path, sd))]
            self.assertEqual(subdirnames, subdirectories)

    def test_csv_data_in_subdirectories(self):
        directories = [d for d in os.listdir('data')\
                       if os.path.isdir(os.path.join('data', d))]
        subdirectories = ['actions', 'locations', 'tasks', 'vents']
        for directory in directories:
            for subdir in subdirectories:
                self.assertTrue(
                    os.path.exists(
                        os.path.join(
                            'data', directory, subdir, f"{subdir}.csv"
                            )))

if __name__ == '__main__':
    unittest.main()
