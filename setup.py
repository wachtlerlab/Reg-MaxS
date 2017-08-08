from setuptools import setup, find_packages
setup(
        name="regmaxsn",
        use_scm_version=True,
        setup_requires=['setuptools_scm'],
        packages=find_packages(exclude=["^\."]),
        package_data={
                        '': ["ParFiles", "TestFiles"]
                    },
        exclude_package_data={'': ["Readme.txt"]},
        install_requires=["numpy>=1.11.2",
                          "matplotlib>=1.5.3",
                          "scipy>=0.18.1",
                          "pandas>=0.19.0",
                          "openpyxl>=2.4.7",
                          "xlrd>=1",
                          "seaborn>=0.7.1",
                          "tifffile>=0.11.1",
                          "pyemd>=0.4.4",
                          "statsmodels>=0.8"],
        python_requires=">=2.7",
    )