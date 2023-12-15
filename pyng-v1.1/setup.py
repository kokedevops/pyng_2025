import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

with open("requerimientos.txt") as f:
    install_requires = f.readlines()

setuptools.setup(
    name='pyng',
    version='0.0.1',
    description='Sondeo de hosts a través de ICMP para verificar su estado',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='JVD',
    author='Jorge Valenzuela',
    author_email='jorge.valenzuela.diaz@ciisa.cl',
    url='https://gitlab.com/jorge.valenzuela.diaz/pyng',
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires='>=3.4',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
