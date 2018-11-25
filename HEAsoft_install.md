# HEAsoft Install #

Instructions to properly install HEAsoft, FTOOLS, and PyXspec, as required by the SPA analysis.

## During CentOS 6.10 Installation ##

Disable Kdump in order to use as much system memory as possible.

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
Next, insert the Guest Additions disc, and follow the on-screen prompts to install the Guest Additions.

Once the Guest Additions have been installed, restart the system.

## Install HEAsoft ##

Once the Guest Additions have been installed, it is now time to install HEASOFT, which includes FTOOLS and FITSIO, as well as PyXspec.

Navigate to https://heasarc.nasa.gov/lheasoft/download.html, and select the source code for CentOS architecture.
Next, select all of the General-Use FTOOLS, as well as Xspec, from the desired packages list.
After submitting the request, a `heasoft-6.25src.tar.gz` file will be ready for download. Download this file.

Now, create an `/astro` directory under `/usr/local`:
```
cd /usr/local
mkdir astro
cd astro
```

Navigate to where the downloaded `heasoft-6.25src.tar.gz` file was saved, move it to the previously created directory, and unzip it:
```
cp heasoft-6.25src.tar.gz /usr/local/astro
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

Finally, change to the build directory and configure, make and install HEAsoft (as root):
```
cd heasoft-6.25/BUILD_DIR/
./configure > config.out 2>&1
make > build.log 2>&1
make install > install.log 2>&1
export HEADAS=/usr/local/astro/heasoft-6.25/x86_64-pc-linux-gnu-lib2.12/
. $HEADAS/headas-init.sh
```
Note that the `make` command takes about 20 minutes, and `make install` takes at least 40 minutes.

Lastly, edit your `.bashrc` file to include the initialization script for HEAsoft, as a regular user:
```
gedit ~/.bashrc

[Add:]
  HEADAS=/usr/local/astro/heasoft-6.25/x86_64-pc-linux-gnu-lib2.12/
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

### Comments ###

Note that here we are using CentOS 6.10, which uses a bash shell. Further HEAsoft installation instructions can be found here:
https://heasarc.nasa.gov/lheasoft/install.html and
https://heasarc.nasa.gov/lheasoft/fedora.html for Fedora-derivative based architectures (like CentOS)

The aim of this README was to provide clear and concise installation instructions in order to get a new virtual machine up and running with the Guest Additions, as well as HEAsoft in as little time as possible.
