# HEAsoft and CIAO Install #

Instructions to properly install CIAO, Astropy, photutils, as required for the CAS analysis, as well as GSL, WCSlib, HEAsoft, FTOOLS, and PyXspec, as required by the SPA analysis.

## During CentOS 6.10 Installation ##

Choose the 'Minimal Desktop' group from the install options when using the full DVD iso.

Disable Kdump in order to use as much system memory as possible.

Note that CentOS 6.10 uses a bash shell.

## Install Guest Additions ##

First, connect to the internet on the guest OS. Next, as root: 
```
yum -y update
yum -y install kernel-devel
yum -y update
```
To then ensure the correct compilers are available (again as root):
```
yum -y install gcc gcc-c++ gcc-gfortran
```
An optional restart may be required here.

Next, insert the Guest Additions disc, and follow the on-screen prompts to install the Guest Additions.

Once the Guest Additions have been installed, restart the system.

## Install CIAO, Astropy, SciPy, photutils ##

CIAO must be installed in order to reduce the *Chandra* data.

First create a software (`soft/`) directory in the user level directory (ie. `/home/user/`):
```
mkdir soft
```

Download the `ciao-install` installation script from http://cxc.harvard.edu/ciao/download/ and follow the instructions at http://cxc.harvard.edu/ciao/threads/ciao_install_tool/index.html#install to properly install CIAO into the software directory. Additionally, make sure to create a CIAO alias in the `.bashrc` file once the installation has completed, as mentioned on the instructions page.
```
gedit ~/.bashrc

[Add:]
  alias ciao="source /home/user/soft/ciao-4.11/bin/ciao.bash"
```
Then save and close `.bashrc`.

Now reload the `.bashrc` file, as user:
```
source ~/.bashrc
```

To install Astropy and photutils (an affiliated package of Astropy) follow the instructions at http://cxc.harvard.edu/ciao/scripting/index.html#install to first freeze the Python packages that come included with CIAO. This disables updates for these packages when installing new packages with `pip3` (which comes with CIAO).

In the terminal:
```
ciao
pip3 freeze > $ASCDS_INSTALL/constraints.txt
pip3 install -c $ASCDS_INSTALL/constraints.txt 'astropy<3.1' scipy pyyaml sip PyQt5
```

After Astropy (and SciPy) have successfully been installed, photutils can now be installed to perform photometry (required by the [concen_calc.py](/reduction/concen_calc.py) script). General installation instructions for photutils can be found at https://photutils.readthedocs.io/en/stable/install.html.

In the terminal:
```
pip3 install -c $ASCDS_INSTALL/constraints.txt --no-deps photutils
```

At this point the reduction of *Chandra* data can be completed, and the CAS analysis can be completed. What remains is to download and install the required software for the SPA analysis.

## Install GSL, WCSlib, HEAsoft ##

Before installing HEAsoft itself, we must install required dependencies of the SPA analysis. These include the GNU Scientific Library (GSL) and WCSlib.

The GNU Scientific Library (GSL) can be downloaded directly from ftp://ftp.gnu.org/gnu/gsl/gsl-2.5.tar.gz, with information about this package available at https://www.gnu.org/software/gsl/.

In the terminal, at the user level directory, move the downloaded `gsl-2.5.tar.gz` file to the software directory, unzip it, configure, build and install it, as root:
```
mv Downloads/gsl-2.5.tar.gz soft
cd soft
gunzip -c gsl-2.5.tar.gz | tar xf -
cd gsl-2.5
./configure > config.out 2>&1
make > build.log 2>&1
make install > install.log 2>&1
```

WCSTools (which includes WCSlib) can be downloaded directly from ftp://cfa-ftp.harvard.edu/pub/gsc/WCSTools/wcstools-3.9.5.tar.gz, with information about this package available at http://tdc-www.harvard.edu/software/wcstools/.

In the terminal, at the user level directory, move the downloaded `wcstools-3.9.5.tar.gz` file to the software directory, unzip it, and install it:
```
mv Downloads/wcstools-3.9.5.tar.gz soft
cd soft
gunzip -c wcstools-3.9.5.tar.gz | tar xf -
cd wcstools-3.9.5
make all
```

We can now install HEASOFT, which includes FTOOLS (and FITSIO), as well as Xspec (and PyXspec), as required by the SPA analysis.

Navigate to https://heasarc.nasa.gov/lheasoft/download.html, and select the source code for CentOS architecture.
Next, select Xspec and whatever dependencies it automatically includes (ie. HEASPtools and HEAGen) from the desired packages list.
After submitting the request, a `heasoft-6.26src.tar.gz` file will be ready for download. Download and save this file.

For further HEAsoft installation instructions, refer to https://heasarc.nasa.gov/lheasoft/install.html and https://heasarc.nasa.gov/lheasoft/fedora.html for Fedora-derivative based architectures (like CentOS).

Now navigate to the user level directory once again and move the `heasoft-6.26src.tar.gz` file to the software directory and unzip it:
```
mv Downloads/heasoft-6.26src.tar.gz soft
gunzip -c heasoft-6.25src.tar.gz | tar xf -
```

Now install required prerequisite packages as root:
```
yum -y install ncurses-devel libcurl-devel libXt-devel python-devel redhat-rpm-config
```

Export required compilers as root:
```
export CC=/usr/bin/gcc
export CXX=/usr/bin/g++
export FC=/usr/bin/gfortran
export PERL=/usr/bin/perl
export PYTHON=/usr/bin/python
```

Finally, change to the build directory and configure, build and install HEAsoft (as root):
```
cd heasoft-6.26/BUILD_DIR/
./configure > config.out 2>&1
make > build.log 2>&1
make install > install.log 2>&1
export HEADAS=/home/user/soft/heasoft-6.26/x86_64-pc-linux-gnu-libc2.12/
. $HEADAS/headas-init.sh
```
Note that the `make` command takes about 20 minutes, and `make install` takes at least 40 minutes.

Lastly, edit your `.bashrc` file to include the initialization script for HEAsoft, as a regular user:
```
gedit ~/.bashrc

[Add:]
  HEADAS=/home/user/soft/heasoft-6.26/x86_64-pc-linux-gnu-libc2.12/
  export HEADAS
  alias heainit=". $HEADAS/headas-init.sh"
```
Then save and close `.bashrc`.

Now reload the `.bashrc` file, as user:
```
source ~/.bashrc
```

To test if PyXspec was properly installed, as user:
```
python
>>> import xspec
```

If everything worked, you should receive no error messages with the last command.

## Install the SPA analysis code ##

Finally, the SPA code itself can be installed. The code can be downloaded directly from http://www.slac.stanford.edu/~amantz/work/morph14/morph.tar, with information regarding the code, installation, and usage available at https://sites.google.com/site/adambmantz/work/morph14.

In the terminal, at the user level directory, move the downloaded `morph.tar` file to the software directory, unzip it, and install it, as user:
```
mv Downloads/morph.tar soft
cd soft
mkdir morph
tar -xf morph.tar -C morph
```

Now move into the `morph/` directory and open the included `Makefile` and edit lines 4-7 to be:
```
INCLUDE = -I$(HEADAS)/include -I/usr/local/include -I/home/user/soft/wcstools-3.9.5/libwcs

LIBS = -lgsl -lgslcblas -L/usr/local/lib -L$(HEADAS)/lib -lcfitsio
WCSLIB = /home/user/soft/wcstools-3.9.5/libwcs/libwcs.a
```
Then save and close the `Makefile`.

Lastly, build the software as user:
```
make
```

You should now have a `morphology.exe` executable, which can be used to perform the SPA analysis.

### Comments ###

The aim of this README was to provide clear and concise installation instructions in order to get a new virtual machine up and running with the Guest Additions, as well as CIAO and HEAsoft in as little time as possible.
