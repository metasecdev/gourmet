import unittest
import tempfile
import os
import shutil

import gourmet.gglobals as gglobals


class Test (unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # create a temporary directory for tests
        cls.tmp_dir = tempfile.mktemp(".pl")  # TODO: replace deprecated mktemp()
        os.makedirs(cls.tmp_dir)
        gglobals.gourmetdir = cls.tmp_dir

        # continue to import with gourmetdir location set to tmp_dir
        from gourmet.GourmetRecipeManager import GourmetApplication
        from gourmet.backends import db
        from gourmet.plugin_loader import get_master_loader

        db.RecData.__single = None
        GourmetApplication.__single = None
        cls.ml = get_master_loader()

    @classmethod
    def tearDownClass(cls):
        # delete temporary test database
        try:
            shutil.rmtree(cls.tmp_dir)
        except OSError as e:
            print("Error: {} : {}").format(cls.tmp_dir, e.strerror)

    def testDefaultPlugins (self):
        self.ml.load_active_plugins()
        print('active:',self.ml.active_plugins)
        print('instantiated:',self.ml.instantiated_plugins)
        self.assertEqual(len(self.ml.errors), 0)  # there should be 0 plugin errors

    def testAvailablePlugins (self):
        # search module directories for available plugins
        for module_name, plugin_set in self.ml.available_plugin_sets.items():
            if module_name not in self.ml.active_plugins:
                self.ml.activate_plugin_set(plugin_set)
        self.ml.save_active_plugins()
        self.assertTrue(os.path.exists(self.ml.active_plugin_filename))
        self.assertEqual(len(self.ml.errors), 0)  # there should be 0 plugin errors

if __name__ == '__main__':
    unittest.main()
