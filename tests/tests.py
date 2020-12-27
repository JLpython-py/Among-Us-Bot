#! python3
# tests.py

import csv
import os
import unittest

class TestDataFilesExist(unittest.TestCase):

    def test_directories_in_data(self):
        dirnames = ['Airship', 'MiraHQ', 'Polus', 'TheSkeld']
        directories = [d for d in os.listdir('data')\
                       if os.path.isdir(os.path.join('data', d))]
        self.assertEqual(dirnames, directories)

    def test_csv_files_in_directories(self):
        directories = [d for d in os.listdir('data')\
                       if os.path.isdir(os.path.join('data', d))]
        files = ['actions.csv', 'locations.csv', 'tasks.csv', 'vents.csv']
        for directory in directories:
            for file in files:
                self.assertTrue(
                    os.path.exists(
                        os.path.join('data', directory, file)
                        )
                    )

    def test_images_in_directories(self):
        directories = [d for d in os.listdir('data')\
                       if os.path.isdir(os.path.join('data', d))]
        images = ['logo.png', 'Map.png', 'SabotageMap.png']
        for directory in directories:
            for img in images:
                self.assertTrue(
                    os.path.exists(
                        os.path.join('data', directory, img)
                        )
                    )

    def test_image_directories_in_directories(self):
        directories = [d for d in os.listdir('data')\
                       if os.path.isdir(os.path.join('data', d))]
        subdirectories = ['actions', 'locations', 'tasks', 'vents']
        for directory in directories:
            for subdirectory in subdirectories:
                self.assertTrue(
                    os.path.exists(
                        os.path.join('data', directory, subdirectory)
                        )
                    )

    def test_csv_item_images_in_corresponding_subdirectory(self):
        directories = [d for d in os.listdir('data')\
                       if os.path.isdir(os.path.join('data', d))]
        directories = ['MiraHQ', 'Polus', 'TheSkeld']
        subdirectories = ['actions', 'locations', 'tasks', 'vents']
        for directory in directories:
            for subdirectory in subdirectories:
                path = os.path.join(
                    'data', directory, f"{subdirectory}.csv")
                with open(path) as file:
                    data = list(csv.reader(file))
                    del data[0]
                    items = [r[0] for r in data]
                for item in items:
                    image = os.path.join(
                        'data', directory, subdirectory, f"{item}.png")
                    self.assertTrue(os.path.exists(image), image)

if __name__ == '__main__':
    unittest.main()
