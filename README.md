
# utils v6.1.3
---
The **utils** package is a centralised library of commonly used utilities.  These utilities include database connection classes, colourmaps, config file (JSON) loading, program event logging, error reporting, console user interface, etc.

Change log information is included in each module's header.


## PACKAGE CONFIGURATION
---
Verion 6 of the utils package features the addition of the `database` class module, which includes intuitive database access wrappers for MySQL, Oracle, SQLite and SQL Server databases.

Outlined below is the current package configuration, with classes listed in **bold**.

- utils
   + config
      + loadconfig()
   + database
      + **Database()**
         + **MySQL()**
         + **Oracle()**
         + **SQLite()**
         + **SQLServer()**
   + log
      + **Log()**
         + write()
         + write_blank_line()
   + get_datafiles
      + get_datafiles()
   + progressbar
       + **ProgressBar()**
          + update_progress()
   + registry
      + **Registry()**
         + various Win registry access methods and functions
   + reporterror
      + reporterror()
   + user_interface
      + **UserInterface()**
         + various console output and error printing methods
      + **PrintBanner()**
   + utils
      + clean_df()
      + dbconn_mysql()
      + dbconn_oracle()
      + dbconn_sql()
      + dbconn_sqlite()
      + direxists()
      + fileexists()
      + format_exif_date()
      + get_os()
      + getcolormap()
      + getdrivername()
      + getsitepackages()
      + json_read()
      + json_write()
      + listcolormaps()
      + ping()
      + rgb2hex()
      + testimport()
      + unidecode()


## INSTALLATION
---
### LINUX
Any of the following options will get you there ...

- **GitHub**
```bash
sudo pip install git+https://github.com/s3dev/utils
```

- **Local / Remote Git Repo**
```bash
sudo pip install git+file:///<repo/location>/utils
```

- **Local Install**
```bash
cd <utils_project_directory>
sudo pip install .
```


### WINDOWS
Any of the following options will get you there ...

- **GitHub**
```bash
pip install git+https://github.com/s3dev/utils
```

- **Local / Remote Git Repo**
```bash
pip install git+file:///<repo/location>/utils
```

- **Local Install**
```bash
cd <utils_project_directory>
pip install .
```


### UPGRADING A CURRENT INSTALLATION
To upgrade a current installation, use an install command as listed above, and append the `--upgrade` argument to the command.  
For example:

```bash
sudo pip install git+https://github.com/s3dev/utils --upgrade
```


## PACKAGE HELP
---
```python
import utils.utils as utils
help(utils)
```  
```python
import utils.config as config
help(config)
```  
```python
from utils.get_datafiles import get_datafiles
help(get_datafiles)
```  
```python
import utils.log as log
help(log)
```  
```python
import utils.progressbar as progressbar
help(progressbar.ProgressBar)
```  
```python
import utils.reporterror as reporterror
help(reporterror)
```  
```python
import utils.user_interface as ui
help(ui)
```  


## TROUBLESHOOTING
---
If you are installing from a local repo and do not have internet access, or the Linux (or Windows) installation is giving you trouble with **cx_Oracle**, use the `--no-deps` argument for **pip**.  This argument will ignore the dependencies (and not try to access the internet), and allow you to install each dependency yourself, *if* you require it.  

```bash
sudo pip install git+https://github.com/s3dev/utils --no-deps
```
