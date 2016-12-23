#!/usr/bin/env python

import argparse
from datetime import datetime, timedelta
import subprocess

def exiftool( filename, options = None, verbose = 0 ):
  cmd = "exiftool %s %s" % ( filename, "" if options == None else options  )
  if 1:
    print( cmd )
  output = str( subprocess.check_output( cmd.split() ).decode( "ascii" ) )
  exif = {}
  for line in output.splitlines():
    data = line.split( ":" )
    if len( data ) > 2:
      key = data[0].strip()
      val = ":".join( d for d in data[1:] ).strip()
      exif.update( { key: val } )
      if verbose > 2:
        print( "  %s:%s" % ( key, val ) )
  return exif


def exiftool_get( filename, tags = {}, verbose = 0 ):
  options = " ".join( "-%s" % t for t in tags )
  exif = exiftool( filename, options = options, verbose = verbose )
  return exif


def exiftool_set( filename, tagval = {}, verbose = 0 ):
  cmd = ["exiftool", filename] + list( "-%s=%s" % ( tag, val ) for ( tag, val ) in tagval.items() )
  print( "cmd: %s" % cmd )
  output = str( subprocess.check_output( cmd ).decode( "ascii" ) )
  print( "output: %s" % output )


def get_datetime( filename, tags = { "createdate", "modifydate" } ):
  for tag in tags:
    exif = exiftool_get( filename, [tag] )
    exif2 = {}
    for key, val in exif.items():
      try:
        val2 = strptime( val )
        exif2.update( {tag:val2} )
      except ValueError as e:
        print( "Error reading %s: %s" % ( filename, e ) )
  return exif2


def strptime( datetimestr ):
  try:
    dt = datetime.strptime( datetimestr, "%Y:%m:%d %H:%M:%S" )
  except:
    raise ValueError( "Failed to convert [%s]" % datetimestr )
  return dt



def set_datetime( filename, exif ):
  exif2 = { key: val.strftime( "%Y:%m:%d\ %H:%M:%S" ) for key, val in exif.items() }
  print( "\n".join( "%s: writing %s" % ( key, val ) for key, val in exif2.items() ) )
  exiftool_set( filename, exif2 )



def set_date_offset( filename, delta, verbose = 0 ):
  exif = get_datetime( filename )
  for key, val in exif.items():
    val2 = val + delta
    exif[key] = val2
    print( "Setting datetime for %s: %s to %s" % ( filename, val, val2 ) )
  set_datetime( filename, exif )


def get_timedelta( value ):
  delta = timedelta()
  for v in value.split( "," ):
    v = v.strip()
    if v.endswith( "d" ):
      delta = delta + timedelta( days = int( v.rstrip( "d" ) ) )
    elif v.endswith( "h" ):
      delta = delta + timedelta( hours = int( v.rstrip( "h" ) ) )
  return delta


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument( "images", nargs = "+", help="Images to modify" )
  parser.add_argument( "--verbose", "-v", action="count", help="Verbosity level" )
  parser.add_argument( "--increment", "-i", type = str, default = "",
    help="Increment timestamp as a CSV (E.g. 5d,7h is 5 days and 7 hours)" )
  parser.add_argument( "--decrement", "-d", type = str, default = "",
    help="Decrement timestamp as a CSV " )
  parser.add_argument( "--datetime", "-s", type = str, default = "",
    help="Set timestamp e.g. \"2014-06-03 8:21\"" )
  args = parser.parse_args()

  if args.increment != "" or args.decrement != "":
    delta = get_timedelta( args.increment ) - get_timedelta( args.decrement )
    for f in args.images:
      set_date_offset( f, delta )
  elif args.datetime != "":
    try: 
      dt = datetime.strptime( arg.datetime, "%Y-%m-%d %H:%M" )
    except:
      print( "Failed to parse datetime string: %s" % args.datetime )
      print( "  E.g.: 2014-06-03 21:33" )
    finally:
      for f in args.images:
        set_datetime( f, dt )
  else:
    for f in args.images:
      exif = get_datetime( f )
      print( "%s:\n%s" % ( f, "\n".join( "  %s:%s" % ( k, v ) for k, v in exif.items() ) ) )



