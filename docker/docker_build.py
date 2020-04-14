#!/usr/bin/env python
from __future__ import print_function

import argparse
import os
import getpass

if __name__=="__main__":
	print("building docker container . . . ")
	user_name = getpass.getuser()
	default_image_name = user_name + "-project-image"

	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--image", type=str,
		help="name for the newly created docker image", default=default_image_name)

	parser.add_argument("-d", "--dry_run", action='store_true', help="(optional) perform a dry_run, print the command that would have been executed but don't execute it.")

        args = parser.parse_args()
	print("building docker image named ", args.image)
	cmd = "docker build "
	cmd += " -t %s -f project.dockerfile ." % args.image
	
	print("command = \n \n", cmd)
	print("")

	# build the docker image
	if not args.dry_run:
		print("executing shell command")
		os.system(cmd)
	else:
		print("dry run, not executing command")
