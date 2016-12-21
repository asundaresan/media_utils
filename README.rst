Media utilities for Python
==========================
This package has utilities for listing the metadata of image and video data. 

Install the package
------------------- 
To install the package::

  pip install -e . --user

Usage
-----

Sort the media files according to metadata 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To list the different sources of the files::
  
  python metadata.py /path/to/media -v
  
The sources.yaml file is read by default to get a list of "selected" media types. 

To move the selected files based on their source::

  python metadata.py /path/to/media -m

To move the complement of the selected files to the sub-folder named "complement"::

  python metadata.py /path/to/media -m
  

Modify date time metadata in files 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
At this moment, this needs GExiv2.

You can check to see the date-time, increment or decrement date-time metadata in the image files::

  python bin/set_time.py <files>
  python bin/set_time.py -i 365d <files>
  python bin/set_time.py -d 15h <files>

  
