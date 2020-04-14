#!/usr/bin/env python
from __future__ import print_function
import yaml
import argparse
import os
import socket
import getpass
#import yaml

if __name__=="__main__":
    user_name = getpass.getuser()
    default_image_name = '{}-project-image'.format(user_name)
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", type=str,
        help="(required) name of the image that this container is derived from", default=default_image_name)

    parser.add_argument("-c", "--container", type=str, default="{}-container".format(user_name), help="(optional) name of the container")\

    parser.add_argument("-d", "--dry_run", action='store_true', help="(optional) perform a dry_run, print the command that would have been executed but don't execute it.")

    parser.add_argument("-e", "--entrypoint", type=str, default="", help="(optional) thing to run in container")

    args = parser.parse_args()
    print("running docker container derived from image %s" %args.image)
    source_dir=os.path.join(os.getcwd(), '..')
    config_file = os.path.join(source_dir, 'config', 'docker_run_config.yaml')

    print(source_dir)

    image_name = args.image
    home_directory = '/home/' + user_name
    dense_correspondence_source_dir = os.path.join(home_directory, 'code')

    cmd = "xhost +local:root \n"
    cmd += "nvidia-docker run --runtime=nvidia"
    if args.container:
        cmd += " --name %(container_name)s " % {'container_name': args.container}
    cmd += "-e NVIDIA_DRIVER_CAPABILITIES=compute,utility "
    
    cmd += " -e DISPLAY -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix:rw "     # enable graphics 
    cmd += " -v %(source_dir)s:%(home_directory)s/code "  \
        % {'source_dir': source_dir, 'home_directory': home_directory}              # mount source
    cmd += " -v ~/.ssh:%(home_directory)s/.ssh " % {'home_directory': home_directory}   # mount ssh keys

    # uncomment below to mount your data volume
    config_yaml = yaml.load(file(config_file))
    host_name = socket.gethostname()
    cmd += " -v %s:%s/data_volume " %(config_yaml[host_name][user_name]['path_to_data_directory'], dense_correspondence_source_dir)

    # share host machine network
    cmd += " --network=host "

    cmd += " --rm " # remove the image when you exit


    if args.entrypoint and args.entrypoint != "":
        cmd += "--entrypoint=\"%(entrypoint)s\" " % {"entrypoint": args.entrypoint}
    else:
        cmd += "-it "
    cmd += args.image
    cmd_endxhost = "xhost -local:root"

    print("command = \n \n", cmd, "\n", cmd_endxhost)
    print("")

    # build the docker image
    if not args.dry_run:
        print("executing shell command")
        code = os.system(cmd)
        print("Executed with code ", code)
        os.system(cmd_endxhost)
        exit(code != 0)
    else:
        print("dry run, not executing command")
        exit(0)
