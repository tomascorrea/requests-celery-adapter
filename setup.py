import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = ['kombu==3.0.26',
            'requests==2.3.0',
            'click==3.1',
            'boto==2.30.0',
            ]

setup(name='celery_adapter',
      version='0.1',
      description='Rating Analytics Celery Client',
      # long_description=README + '\n\n' + CHANGES,
      classifiers=["Programming Language :: Python",
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
      entry_points="""\
      [paste.app_factory]
      main = rca:main
      [console_scripts]
      celery-send-task = rca.scripts.cli:send_task
      """,
      )
