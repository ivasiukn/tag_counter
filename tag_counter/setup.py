from setuptools import setup

setup(
    name='tag_counter',
    packages=['tag_counter', 'tag_counter.services'],
    version='0.1',
    license='MIT',
    description='Simple tag counter',
    author='Nazariy Ivasyuk',
    author_email='ivasiukn@gmail.com',
    url='https://github.com/ivasiukn/tag_counter',
    download_url='https://github.com/ivasiukn/tag_counter/archive/0.1.tar.gz',
    keywords=['tag', 'count'],
    install_requires=['pyyaml'],
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
        ],
    entry_points={'console_scripts': ['tag_counter = tag_counter.main_executor:main']}
    )
