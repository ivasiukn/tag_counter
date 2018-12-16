from setuptools import setup

setup(name='tag_counter',
      version='0.1',
      description='Simple tag counter',
      url='https://github.com/ivasiukn/tag_counter',
      author='Nazariy Ivasyuk',
      author_email='ivasiukn@gmail.com',
      #license='MIT',
      packages=['tag_counter']
      ,entry_points={'console_scripts': ['tag_counter = tag_counter.main_executor:main']}
      #,zip_safe=False
      )
