import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
# with open(os.path.join(here, 'README.txt')) as f:
#     README = f.read()
# with open(os.path.join(here, 'CHANGES.txt')) as f:
#     CHANGES = f.read()

requires = [
            'kombu',
            'requests',
            'click',
            'boto',
    ]

setup(name='celery_adapter',
      version='0.1',
      description='Rating Analytics Celery Client',
      # long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Celery",
        "Topic :: Internet :: Worker",
        "Topic :: Internet :: Worker :: CLI :: Application",
        ],
      author='Diog Fernandes',
      author_email='diogo@geru.com.br',
      url='',
      keywords='worker sqs cli celery',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='requests-celery-adapter',
      install_requires=requires,
      entry_points = {
        'console_scripts': [
                            'cli-celery=celery_adapter:cli',
                           ],
      }
      )
