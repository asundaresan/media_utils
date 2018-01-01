#!/usr/bin/env python

import sys
import argparse
import yaml
import json
import logging 

from media_utils import metadata, conf

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( "folder", help="Search folder" )
    parser.add_argument( "--verbosity", "-v", action="count", default = 0, help="Verbosity level" )
    parser.add_argument( "--source", "-s", default = "", help="Data file containing metadata to filter" )
    parser.add_argument( "--move", "-m", action="store_true", help="Move selected files to folder" )
    parser.add_argument( "--move-complement", "-c", action="store_true", help="Move complement of selected files to folder" )
    args = parser.parse_args()
    print( "Searching for files in: %s" % args.folder )
    
    # set logging level 
    console_level = logging.WARN if args.verbosity == 0 else logging.INFO if args.verbosity == 1 else logging.DEBUG
    logging.basicConfig( level = console_level, format = '[%(levelname)s] %(message)s' )

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
    logging.debug( "\n".join( "- %s: %s" % ( k, json.dumps( v ) ) for k, v in select.items() ) )

    metadata.process_folder( args.folder, select = select.values(), move = args.move,
        move_complement = args.move_complement, verbose = args.verbosity )

