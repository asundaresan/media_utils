Media utilities for Python
==========================
This package has utilities for listing the metadata of image and video data. 

Install the package
------------------- 

Note that the package relies on the ``exif_tool`` program. To install on Mac OS X::

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

  python bin/get_metadata.py <folder> -i data/iphone6.yaml

To move the selected files based on their source::

  python bin/get_metadata.py <folder> -m

To move the complement of the selected files to the sub-folder named "complement"::

  python bin/get_metadata.py <folder> -c


  
Modify date time metadata in files 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
At this moment, this needs GExiv2 and works only in Ubuntu Linux.::

  sudo apt-get install gir1.2-gexiv2-0.10

You can check to see the date-time, increment or decrement date-time metadata in the image files::

  python bin/set_time.py <files>
  python bin/set_time.py -i 365d <files>
  python bin/set_time.py -d 15h <files>

  
