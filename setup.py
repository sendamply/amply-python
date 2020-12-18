from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

__version__ = None
with open('amply/version.py') as f:
    exec(f.read())

setup_args = dict(
    name='amply-mail',
    version=str(__version__),
    description='This is the Amply Python SDK that integrates with the v1 API.',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    keywords=['amply', 'email'],
    url='https://github.com/sendamply/amply-python'
)

install_requires = [
    'requests'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
