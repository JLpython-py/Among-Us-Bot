#! python3
# tests.py

import csv
import os
import unittest

class TestMapBot(unittest.TestCase):

    def test_directories_in_data(self):
        dirnames = ['airship', 'mirahq', 'polus', 'theskeld']
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
                path = os.path.join(
                    'data', directory, subdir, f"{subdir}.csv")
                self.assertTrue(os.path.exists(path))

    def test_item_images_exist(self):
        directories = [d for d in os.listdir('data')\
                       if os.path.isdir(os.path.join('data', d))]
        subdirectories = ['actions', 'locations', 'tasks', 'vents']
        for directory in directories:
            for subdir in subdirectories:
                path = os.path.join(
                    'data', directory, subdir, f"{subdir}.csv")
                with open(path) as file:
                    data = list(csv.reader(file))
                    headers = data.pop(0)
                    items = [r[0] for r in data]
                for item in items:
                    imgpath = os.path.join(
                        'data', directory, subdir, f"{item}.png")
                    self.assertTrue(os.path.exists(imgpath), imgpath)

class TestRandomAmongUs(unittest.TestCase):

    def test_settings_file_exists(self):
        path = os.path.join('data', 'settings.txt')
        self.assertTrue(os.path.exists(path))

class TestMapInfo(unittest.TestCase):

    def test_reactions(self):
        reactions = {
            u'\u23ee': '⏮', u'\u23ea': '⏪', u'\u25c0': '◀', u'\u25b6': '▶',
            u'\u23e9': '⏩', u'\u23ed': '⏭', u'\u2714': '✔', u'\u274c': '❌'}
        for rxn in reactions:
            self.assertEqual(rxn, reactions[rxn])

if __name__ == '__main__':
    unittest.main()
