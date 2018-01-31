from setuptools import setup, find_packages

requires = ['kombu>=3.0.30',
            'requests==2.18.4',
            'six>=1.11.0'
            ]

extras_require = {
    'test': [
        'pytest>=3.2.2',
        'mock>=2.0.0',
        'redis>=2.10.6',
        'httpretty>=0.8.14',
    ],
    'cli': ['click==3.1']
}

setup(name='requests-celery-adapters',
      version='2.0.8',
      description='Requests lib adapters to send Celery messages (tasks)',
      # long_description=README + '\n\n' + CHANGES,
      classifiers=["Programming Language :: Python"],
      author='Diogo Fernandes',
      author_email='diogo@geru.com.br',
      url='',
      keywords='worker celery',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='requests-celery-adapter',
      install_requires=requires,
      extras_require=extras_require,
      entry_points="""\
      [paste.app_factory]
      main = rca:main
      [console_scripts]
      celery-send-task = rca.scripts.cli:send_task
      """,
      )
