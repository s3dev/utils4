
# utils3
---
The **utils3** library is a collection of commonly used Python 3.5 utilities. These utilities include database connection classes, colourmaps, JSON config file loading, program event logging, error reporting, console user interface, etc.

`utils3` is a Python 3.5 continuation of the discontinued Python 2.7 `utils` package, which ended with v6.1.5.


## Example Use & Detailed Design
---
Please refer to the linked <a href="./docs/build/html/index.html" style="font-weight: bold; text-decoration: none;" target="_blank">Sphinx documentation</a> for example code use, and detailed design documentation.


## Change Log
---
Git change log information can be found <a href="./docs/build/html/changelog.html" style="font-weight: bold; text-decoration: none;" target="_blank">here</a>.


## Installation
---
### Linux
Any of the following options will get you there ...

- **GitHub**
```bash
sudo pip install git+https://github.com/s3dev/utils3
```

- **Local / Remote Git Repo**
```bash
sudo pip install git+file:///<repo/location>/utils3
```

- **Local Install**
```bash
cd <utils3_project_directory>
sudo pip install .
```


### Windows
Any of the following options will get you there ...

- **GitHub**
```bash
pip install git+https://github.com/s3dev/utils3
```

- **Local / Remote Git Repo**
```bash
pip install git+file:///<repo/location>/utils3
```

- **Local Install**
```bash
cd <utils3_project_directory>
pip install .
```


### Upgrading a Current Installation
To upgrade a current installation, use an install command as listed above, and append the `--upgrade` argument to the command.  
For example:

```bash
sudo pip install git+https://github.com/s3dev/utils3 --upgrade
```


## Version Check
---
To see which version of `utils3` is installed, use the `__version__` attribute from the `utils3` module.

```python
import utils3
utils3.__version__
```


## Module Help
---
```python
from utils3 import utils
help(utils)
```  
```python
from utils3 import config
help(config)
```
```python
# etc ...
```

## Troubleshooting
---
If you are installing from a local repo and do not have internet access, or the Linux (or Windows) installation is giving you trouble with **cx_Oracle**, use the `--no-deps` argument for **pip**.  This argument will ignore the dependencies (and not try to access the internet), and allow you to install each dependency yourself, *if* you require it.  

```bash
sudo pip install git+https://github.com/s3dev/utils3 --no-deps
```
