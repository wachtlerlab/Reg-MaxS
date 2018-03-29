Welcome to regmaxsn repository!

Description
---

**Reg-MaxS and Reg-MaxS-N: Algorithms for co-registration of pairs and groups of neuron morphologies based on maximization of spatial overlap**

These algorithms have been discussed in detail in the following publication:

Kumaraswamy A., Kai K., Ai H., Ikeno H., Wachtler T. (2018). "Spatial registration of neuron morphologies based on maximization of volume overlap". In *BMC Bioinformatics*, DOI: [10.1186/s12859-018-2136-z](https://doi.org/10.1186/s12859-018-2136-z)

This repository contains scripts for running Reg-MaxS and Reg-MaxS-N algorithms for registering pairs and groups of neuron morphologies respectively.

The algorithms are written in  Python and at the moment work only with SWC files.

# Installation


With Conda (Linux or Windows):

1. Create a new environment: 
>conda create --name regmaxsn python=2.7 numpy scipy pillow matplotlib scikit-learn pandas seaborn openpyxl xlrd statsmodels
2. Activate environment: 
>(on Linux) source activate regmaxsn 
>(on Windows) activate regmaxsn
3. Install regmaxsn: 
>pip install \<path to Reg-MaxS repository\>
4. Create Reg-MaxS Workspace. Note where your Reg-MaxS Workspace is created.
>python \<path to Reg-MaxS repository\>/setupWorkspace.py

Without Conda, with pip and virtualenvwrapper (only for Linux):

1. Create a new environment: 
>mkvirtualenv regmaxsn
2. Activate environment: 
>workon regmaxsn
3. Install regmaxsn:
>pip install \<path to Reg-MaxS repository\>
4. Create Reg-MaxS Workspace. Note where your Reg-MaxS Workspace is created.
>python \<path to Reg-MaxS repository\>/setupWorkspace.py

NOTE: This environment must be activated every time you want to run Reg-MaxS, Reg-MaxS-N or any other scripts of this package.

# Usage:

## Reg-MaxS

1. First you need to create a parameter file for Reg-MaxS. This is created using the file
> \<path to your Reg-MaxS Workspace\>/utilityScripts/constructRegMaxSParFile.py

You need to open this .py file in a editor and change variables as needed. The detailed usage instructions of this script are provided at the top of it. Two different use cases have been illustrated using three examples. Take a look at them and modify the script according to your needs.

2. After editing the "constructRegMaxSParFile.py" as needed, create a parameter file as below:
> python \<path to your Reg-MaxS Workspace\>/utilityScripts/constructRegMaxSParFile.py

3. Run Reg-MaxS with this parameter file:
> python -m regmaxsn.scripts.algorithms.RegMaxS \<path to the above created Reg-MaxS parameter file\>

## Reg-MaxS-N

1. First you need to create a parameter file for Reg-MaxS-N. This is created using the file
> \<path to your Reg-MaxS Workspace\>/utilityScripts/constructRegMaxSNParFile.py

You need to open this .py file in a editor and change variables as needed. The detailed usage instructions of this script are provided at the top of it. Two different use cases have been illustrated using three examples. Take a look at them and modify the script according to your needs.

2. After editing the "constructRegMaxSNParFile.py" as needed, create a parameter file as below:
> python \<path to your Reg-MaxS Workspace\>/utilityScripts/constructRegMaxSNParFile.py

3. Run Reg-MaxS-N with this parameter file:
> python -m regmaxsn.scripts.algorithms.RegMaxSN \<path to the above created Reg-MaxS-N parameter file\>