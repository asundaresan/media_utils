#!/usr/bin/env python

from media_utils.metadata import set_datetime_offset, set_datetime, get_datetime
import argparse
import datetime



def to_datetime( datetimestr ):
  """ Get datetime from datetime string
  """
  return datetime.datetime.strptime( datetimestr, "%Y-%m-%d %H:%M:%S" )




def to_timedelta( value ):
  """ Parse string to get delta time
      E.g. 7d,5h,3m,2s
  """
  delta = datetime.timedelta()
  for v in value.split( "," ):
    v = v.strip()
    if v == "":
      pass
    elif v.endswith( "d" ):
      delta = delta + datetime.timedelta( days = int( v.rstrip( "d" ) ) )
    elif v.endswith( "h" ):
      delta = delta + datetime.timedelta( hours = int( v.rstrip( "h" ) ) )
    elif v.endswith( "m" ):
      delta = delta + datetime.timedelta( minutes = int( v.rstrip( "m" ) ) )
    elif v.endswith( "s" ):
      delta = delta + datetime.timedelta( seconds = int( v.rstrip( "s" ) ) )
    else:
      raise ValueError( "cannot parse <%s>" % ( v ) )
  return delta



if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument( "images", nargs = "+", help="Get and set datetime for images" )
  parser.add_argument( "--verbose", "-v", action="count", help="Verbosity level" )
  parser.add_argument( "--increment", "-i", type = str, default = "",
    help="Increment timestamp as a CSV (E.g. 5d,7h is 5 days and 7 hours)" )
  parser.add_argument( "--decrement", "-d", type = str, default = "",
    help="Decrement timestamp as a CSV " )
  parser.add_argument( "--datetime", "-s", type = str, default = "",
      help="Set timestamp e.g. \"2014-06-03 8:21:32\"" )
  args = parser.parse_args()

  if args.increment != "" or args.decrement != "":
    try: 
      delta = to_timedelta( args.increment ) - to_timedelta( args.decrement )
    except ValueError as e:
      print( "Failed to parse increment or decrement: %s" % ( e ) )
      print( "  E.g.: 1d,2h,3m,4s" )
    else:
      print( "Incrementing datetime by %s" % delta )
      for f in args.images:
        if args.verbose > 0:
          print( "- %s" % f )
        set_datetime_offset( f, delta, verbose = args.verbose )
  elif args.datetime != "":
    try: 
      dt = to_datetime( args.datetime )
    except ValueError as e:
      print( "Failed to parse datetime string '%s': %s" % ( args.datetime, e ) )
      print( "  E.g.: 2014-06-03 21:33:59" )
    else:
      for f in args.images:
        if args.verbose > 0:
          print( "- %s" % f )
        set_datetime( f, dt, verbose = args.verbose )
  else:
    for f in args.images:
      exif = get_datetime( f, verbose = args.verbose )
      print( "%s:\n%s" % ( f, "\n".join( "  %s: %s" % ( k, v ) for k, v in exif.items() ) ) )



