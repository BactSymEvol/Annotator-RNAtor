import importlib.util
import os
import sys
import subprocess

package_name = 'python3-pyqt5'
package_name2 = 'ncbi-blast+'
subname = 'blastn'
package_name3 = 'networkx'
package_name4 = 'bwa'
package_name5 = 'subread'
package_name6 = 'bash'
package_name7 = 'parallel'
package_name8 = 'pandas'
package_name = 'bowtie2'

#Check whether PyQt5 is installed or not
spec = importlib.util.find_spec(package_name)
if spec is None:
    print(package_name +" is not installed")
    print("Installing" + "" + package_name)
    subprocess.run(["sudo", "apt-get", "install", "python3-pyqt5"])
else:
    print(package_name + " is installed")

#Check whether blast is installed or not
spec = importlib.util.find_spec(package_name2)
if spec is None:
    print(package_name2 +" is not installed")
    print("Installing" + "" + package_name2)
    subprocess.run(["sudo", "apt-get", "install", "ncbi-blast+"])
else:
    print(package_name2 + " is installed")

#Check whether networkx is installed or not
spec = importlib.util.find_spec(package_name3)
if spec is None:
    print(package_name3 +" is not installed")
    print("Installing" + "" + package_name3)
    subprocess.run(["sudo", "apt-get", "install", "python-networkx"])
else:
    print(package_name3 + " is installed")

#Check whether bwa is installed or not
spec = importlib.util.find_spec(package_name4)
if spec is None:
    print(package_name4 +" is not installed")
    print("Installing" + "" + package_name4)
    subprocess.run(["sudo", "apt-get", "install", "bwa"])
else:
    print(package_name4 + " is installed")

#Check whether subread is installed or not
spec = importlib.util.find_spec(package_name5)
if spec is None:
    print(package_name5 +" is not installed")
    print("Installing" + "" + package_name5)
    subprocess.run(["sudo", "apt", "install", "subread"])
else:
    print(package_name5 + " is installed")

#Check whether bash is installed or not
spec = importlib.util.find_spec(package_name6)
if spec is None:
    print(package_name6 +" is not installed")
    print("Installing" + "" + package_name6)
    subprocess.run(["sudo", "apt", "install", "bash"])
else:
    print(package_name6 + " is installed")

#Check whether parallel GNU is installed or not
spec = importlib.util.find_spec(package_name7)
if spec is None:
    print(package_name7 +" is not installed")
    print("Installing" + "" + package_name7)
    subprocess.run(["sudo", "apt-get", "install", "parallel"])
else:
    print(package_name7 + " is installed")

#Check whether pandas is installed or not
spec = importlib.util.find_spec(package_name8)
if spec is None:
    print(package_name8 +" is not installed")
    print("Installing" + "" + package_name8)
    subprocess.run(["pip", "install", "pandas"])
else:
    print(package_name8 + " is installed")

#Check whether bowtie2 is installed or not
spec = importlib.util.find_spec(package_name8)
if spec is None:
    print(package_name8 +" is not installed")
    print("Installing" + "" + package_name8)
    subprocess.run(["sudo", "apt-get", "install", "bowtie2"])
else:
    print(package_name8 + " is installed")
