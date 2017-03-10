Media utilities for Python
==========================
This package has utilities for manipulating media files based on the metadata. 

Install the package
------------------- 

The package is based on the ``exiftool`` program. To install on Mac OS X::

  sudo port install p5-image-exiftool

To install on Ubuntu Linux::

  sudo apt-get install libimage-exiftool-perl

To install the package::

  pip install -e . --user

or for Python 3::

  pip3 install -e . --user

Usage
-----

Sort the media files according to metadata 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To list the different sources of the files::
  
  python bin/get_metadata.py <folder> -v
  
The list of "selected" media types is a sample set of phones which is used if none is specified. 
To use your own list of media types use the following (a list is available in ``data``)::

  python bin/get_metadata.py <folder> -s data/iphone6.yaml

To move the selected files based on their source::

  python bin/get_metadata.py <folder> -m

To move the complement of the selected files to the sub-folder named "complement"::

  python bin/get_metadata.py <folder> -c


  
Modify date time metadata in files 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To check the date-time of files, simply run:: 

  python bin/set_datetime.py <files>

To increment or decrement the various date-time tags in the file, use the -i or -d option respectively. The amount to be incremented or decremented is provided as a comma separated value and suffixed by d, h, m or s for day, hour, minute and second respectively.::

  python bin/set_datetime.py -i 365d,3h <files>
  python bin/set_datetime.py -d 15h,30m,0s <files>

To set the date-time to an absolute value, provide the date-time in the standard format for the datetime module.::

  python bin/set_datetime.py -s "2013-05-29 15:30:42" <files>
  
  
