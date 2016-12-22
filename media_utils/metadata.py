# Get information about the media 
# 

import os
import pickle
import subprocess
import json 
import yaml


def run_command( command ):
  p = subprocess.Popen( command,
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT )
  return iter(p.stdout.readline, b'')


def get_video_metadata( filename, verbose = 0 ):
  """ Get meta-data by parsing exiftool (from libimage-exiftool-perl)
  """
  if verbose > 2:
    print( "processing %s" % filename )
  cmd = "exiftool %s" % filename

  exif = {}
  for line in run_command( cmd.split() ):
    if ":" in line:
      data = line.split( ":" )
      key = data[0].strip()
      val = data[1].strip()
      exif.update( { key: val } )
  return exif



def translate( exif, keymap ):
  for k, v in keymap.iteritems():
    #print( "  translating %s -> %s: %s" % ( k, v, k in exif.keys() ) )
    if k in exif.keys() and v not in exif.keys():
      exif[v] = exif[k]
      #print( "    %s: %s" % ( v, exif[v] ) )
  return exif



def get_metadata( filename, koi, verbose = 0, video_extensions = ["MOV"], image_extensions = ["JPG", "JPEG"] ):
  exif = get_video_metadata( filename, verbose = verbose )
  keymap = {"Camera Model Name": "Model"}
  exif2 = translate( exif, keymap )
  exif3 = { k:v for k,v in exif2.iteritems() if k in koi }
  if verbose > 2:
    print( "\n".join( "  %s:%s" % (k,v) for k, v in exif3.iteritems() ) )
  return exif3



#def get_metadata( filename, koi, verbose = 0, video_extensions = ["MOV"], image_extensions = ["JPG", "JPEG"] ):
#  name, extension = os.path.splitext( filename )
#  filetype = extension.upper().lstrip( "." )
#  exif = {}
#  if filetype in video_extensions:
#    exif = get_video_metadata( filename, koi, verbose = verbose )
#  elif filetype in image_extensions:
#    exif = get_image_info( filename, koi, verbose = verbose )
#  
#  exif.update( {"Type": filetype } )
#  return exif
#
#
#def get_image_info( filename, koi, verbose = 0 ):
#  try:
#    im = ImageFile.Image.open( filename )
#  except:
#    return {}
#  try:
#    exif = { ExifTags.TAGS[k]: v for k, v in im._getexif().items() if k in ExifTags.TAGS }
#  except:
#    exif = {}
#  size = list( im.size )
#  size.sort
#  exif["Size"] = "x".join( "%d" % x for x in size )
#  exif.update( { k:"" for k in koi if k not in exif.keys() } )
#  if len( koi ) > 0:
#    exif2 = { k:exif[k] for k in koi if k in exif.keys() }
#    return exif2
#  return exif



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
        if verbose > 1:
          print( "Ignoring %s" % filename )
  empty = json.dumps( {} )
  ignored = 0 if empty not in db.keys() else len( db[empty]["files"] )
  print( "Found %d files, ignored %d (%d classes)" % ( found, ignored, len( db ) ) )

  ns_files = 0
  ns_categories = 0
  for key, val in db.iteritems():
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

import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( "folder", help="Search folder" )
    parser.add_argument( "--repickle", "-R", action="store_true", help="Force rewrite of pickle files" )
    parser.add_argument( "--verbose", "-v", action="count", help="Verbosity level" )
    parser.add_argument( "--source", "-s", default = "sources.yaml", help="Move selected files to folder" )
    parser.add_argument( "--move", "-m", action="store_true", help="Move selected files to folder" )
    parser.add_argument( "--move-complement", "-c", action="store_true", help="Move complement of selected files to folder" )
    args = parser.parse_args()
    print( "Searching for files in: %s" % args.folder )
    
    select = {}
    try:
      with open( args.source, "r" ) as f:
        select = yaml.load( f )
    except:
      print( "Failed to load sources from %s: %s" % ( args.source ) )
    else:
      print( "Loaded sources from %s (%d types)" % ( args.source, len( select ) ) )
      if args.verbose > 0:
        print( "\n".join( "- %s: %s" % ( k, json.dumps( v ) ) for k, v in select.iteritems() ) )


    process_folder( args.folder, select = select.values(), move = args.move,
        move_complement = args.move_complement, verbose = args.verbose )
