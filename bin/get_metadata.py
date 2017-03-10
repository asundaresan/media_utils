#!/usr/bin/env python

import sys
import argparse
import yaml
import json

from media_utils import metadata, conf

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( "folder", help="Search folder" )
    parser.add_argument( "--verbose", "-v", action="count", default = 0, help="Verbosity level" )
    parser.add_argument( "--source", "-s", default = "", help="Data file containing metadata to filter" )
    parser.add_argument( "--move", "-m", action="store_true", help="Move selected files to folder" )
    parser.add_argument( "--move-complement", "-c", action="store_true", help="Move complement of selected files to folder" )
    args = parser.parse_args()
    print( "Searching for files in: %s" % args.folder )
    print( "args: %s" % args )
    print( "args.verbose: %d" % args.verbose )
    
    select = {}
    if args.source:
      try:
        with open( args.source, "r" ) as f:
          select = yaml.load( f )
      except:
        print( "Failed to load sources from %s: %s" % ( args.source ) )
      else:
        print( "Loaded sources from %s (%d types)" % ( args.source, len( select ) ) )
    else:
      select = yaml.load( conf.data )
    if args.verbose > 0:
      print( "\n".join( "- %s: %s" % ( k, json.dumps( v ) ) for k, v in select.items() ) )

    metadata.process_folder( args.folder, select = select.values(), move = args.move,
        move_complement = args.move_complement, verbose = args.verbose )

