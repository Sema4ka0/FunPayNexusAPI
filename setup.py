from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()


setup(
    name='FunPayNexusAPI',
    version='0.0.4',
    author='Sema4ka0',
    author_email='seem.git@gmail.com',
    description='This is a convenient tool for developing and working with the site funpay.com',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url='https://github.com/Sema4ka0/FunPay-API',
    packages=find_packages(),
    install_requires=['requests_toolbelt', 'requests', 'beautifulsoup4', 'aiohttp'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='funpay api FunPayAPI tool bot tg lib',
    project_urls={
        'GitHub': 'https://github.com/Sema4ka0/FunPay-API',
        'Chanel': 'https://t.me/FunPayNexus'
    },
    python_requires='>=3.8'
)