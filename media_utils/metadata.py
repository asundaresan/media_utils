# File to get metadata from files

import os
import pickle
import subprocess
import json 
import yaml
from datetime import datetime
from .exiftool import exiftool, exiftool_set, exiftool_get


def get_datetime_tags( ):
  return [ "createdate", "modifydate", "trackcreatedate", "trackmodifydate", "mediacreatedate", "mediamodifydate" ]



def strptime( datetimestr ):
  """ Get datetime from EXIF date value
  """
  try:
    dt = datetime.strptime( datetimestr, "%Y:%m:%d %H:%M:%S" )
  except ValueError as e:
    raise ValueError( e )
  return dt



def get_datetime( filename, verbose = 0 ):
  tags = get_datetime_tags()
  tag_value_dict = {}
  for tag in tags:
    exif = exiftool_get( filename, [tag] )
    if len( exif.keys() ) == 1:
      for key, val in exif.items():
        try:
          dt = strptime( val )
          tag_value_dict.update( {tag:dt} )
        except ValueError as e:
          print( "Error reading %s: %s" % ( filename, e ) )
    else:
      print( "Warning! %s did not have tag %s" % ( filename, tag ) )
  return tag_value_dict



def set_datetime( filename, dt, verbose = 0 ):
  """ set date 
  """
  val2 = dt.strftime( "%Y:%m:%d %H:%M:%S" )
  tag_value_dict = { tag: val2 for tag in get_datetime_tags() }
  if verbose > 1:
    print( "  setting all dates: %s" % ( val2 ) )
  exiftool_set( filename, tag_value_dict )



def set_datetime_offset( filename, delta, verbose = 0 ):
  """ set date offset 
  """
  tag_value_dict = get_datetime( filename )
  tag_value_dict2 = {}
  for key, val in tag_value_dict.items():
    val2 = val + delta
    tag_value_dict2.update( { key: val2.strftime( "%Y:%m:%d %H:%M:%S" ) } )
    if verbose > 1:
      print( "  setting %s: %s to %s" % ( key, val, val2 ) )
  exiftool_set( filename, tag_value_dict2 )



def translate( exif, keymap ):
  for k, v in keymap.items():
    if k in exif.keys() and v not in exif.keys():
      exif[v] = exif[k]
  return exif



def get_metadata( filename, koi, verbose = 0 ):
  exif = exiftool( filename, verbose = verbose )
  keymap = {"Camera Model Name": "Model"}
  exif2 = translate( exif, keymap )
  exif3 = { k:v for k,v in exif2.items() if k in koi }
  if verbose > 2:
    print( "\n".join( "  %s:%s" % (k,v) for k, v in exif3.items() ) )
  return exif3



def is_match( exif_list, exif, verbose = 0 ):
  """ exif_list is a list of dicts (exifs)
      exif is a dict (exif )
      return True if exif matches all (key, value) pairs in any one item in exif_list 
  """
  exif_keys = [k.lower() for k in exif.keys()]
  for e in exif_list:
    checks = list( e[k].lower() == exif[k].lower() if k.lower() in exif_keys else False for k in e.keys() )
    if verbose > 2:
      print( "%s == %s: %s %s" % ( json.dumps( exif ), json.dumps( e ), all( checks ), checks ) )
    if all( checks ):
      return True 
  return False



def exif_to_string( exif, keys = ["File Type", "Make", "Model", "Image Size"] ):
  keystr = "_".join( exif[k] for k in keys if k in exif.keys() )
  return keystr.replace( " ", "" )



def move_to_subfolder( files, subfolder, verbose = 0 ):
  """ Copy files to subfolder in their respective folders,
      i.e. f is copied to dirname( f )/subfolder/basename( f )
  """
  if verbose > 1:
    print( "Moving %d files to %s" % ( len( files ), subfolder ) )
  for src in files:
    folder = "%s/%s" % ( os.path.dirname( src ), subfolder )
    dst = "%s/%s" % ( folder, os.path.basename( src ) )
    if not os.path.exists( folder ):
      print( "Making directory: %s" % folder )
      os.makedirs( folder )
    if os.path.exists( src ) and not os.path.exists( dst ):
      os.rename( src, dst )
      if verbose > 1:
        print( "%s -> %s" % ( src, dst ) )


def process_folder( root_folder, select = [], move = False, move_complement = False, recurse = False, verbose = 0 ):
  """ Get info of all image files in the folder 
  """
  koi = ["Make", "Model", "Image Size", "File Type" ]
  root_folder = os.path.abspath( root_folder )
  db = dict()
  found = 0
  for f in os.listdir( root_folder ):
    filename = os.path.join( root_folder, f )
    if os.path.isfile( filename ):
      exif = get_metadata( filename, koi, verbose = verbose )
      if len( exif.keys() ) > 0:
        found += 1
        key = json.dumps( exif )
        if not key in db.keys():
          db[key] = { "exif": exif, "files": list() }
        db[key]["files"].append( filename )
      else:
        if verbose > 0:
          print( "Ignoring %s" % filename )
  empty = json.dumps( {} )
  ignored = 0 if empty not in db.keys() else len( db[empty]["files"] )
  print( "Found %d files, ignored %d (%d classes)" % ( found, ignored, len( db ) ) )

  ns_files = 0
  ns_categories = 0
  for key, val in db.items():
    exif = val["exif"]
    files = val["files"]
    selected = is_match( select, exif )
    if selected:
      if move:
        subfolder = exif_to_string( exif )
        move_to_subfolder( files, subfolder, verbose )
        print( "m %s (%d files -> %s)" % ( key, len( files ), subfolder ) )
      else:
        print( "* %s (%d files)" % ( key, len( files ) ) )
    else:
      ns_files += len( files )
      ns_categories += 1
      if move_complement:
        subfolder = "complement"
        move_to_subfolder( files, subfolder, verbose )
        print( "c %s (%d files -> %s)" % ( key, len( files ), subfolder ) )
      else:
        if verbose > 0:
          print( "  %s (%d files)" % ( key, len( files ) ) )
          if verbose > 1:
            print( "\n".join( "    %s" % os.path.basename( f ) for f in files ) )

  print( "  Other (%d categories, %d files)\n--" % ( ns_categories, ns_files ) )

