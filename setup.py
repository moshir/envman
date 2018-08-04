import os
from setuptools import setup, find_packages


dir = os.path.join(os.path.dirname(__file__), "envman")

setup(name='envman',
      version='1.0.1',
      description='A simple environment manager ',
      author='moshir mikael',
      author_email='moshirm@amazon.fr',
      license='MIT',
      packages = {
          "envman" : "envman",
          "envman.ssm" : "envman/ssm",
          "envman.api" : "envman/api",
          "envman.tests" : "envman/tests",
          "envman.utils" : "envman/utils"
      },
      package_dir = {'envman': 'envman'},
      zip_safe=False
      )