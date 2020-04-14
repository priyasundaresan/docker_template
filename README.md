## Minimal Docker Template for a New Project

### Steps to Setup:
* Fork this repository if you're starting a project from scratch, (or just copy over the files manually if you've already set up a project repository)
* ```cd docker```
* Edit ```project.dockerfile``` with whatever dependencies you need for your project (I have included a few as a minimal working example)
* Build a docker image based on the docker file using ```./docker_build.py```. This will create an image that by default is called ```username-default-image```, but you can change this in the script as desired. If multiple people will be working off of this image, it's best to name it something not username-specific.
* Edit ```config/docker_run.yaml``` to include a directory for data that you would like to mount inside your container (optional, but you'll probably need to do this if you're going to do any sort of training)
* Run the image with ```./docker_run.py```, which starts a container called ```username-container```, which you can also change in the script as needed. You likely will want to use some kind of unique identifier like a username + project name in the container name to prevent conflicts if multiple people are trying to run the a container based off the same image. This can also be changed in the script.

### Workflow/Development:
* The nice part about this setup is that to back up an image, which can often be multiple gigabytes, you just need to back up the dockerfile! And for multiple people planning to use the same image, it makes things easier because if one person installs something in the image, they can just re-build the image and push the dockerfile so that others can re-build the image with the updated dependencies, or if it is on the same machine, they can just re-run the container based on the image to reflect the changes.
* Note that setting up the dockerfile is the most important part of this setup. If your ```install_dependencies.sh``` script has errors, then the build will fail. Thus, I recommend that you first make a very minimal docker container, for instance, ```nvidia-docker run --runtime=nvidia -it -e NVIDIA_VISIBLE_DEVICES=0 --rm -v /raid/priya/:/data nvidia/cuda:8.0-devel-ubuntu16.04 bash```. Then, from inside this container, you can try installing whatever you want as you normally would. Then, using the ```history``` command gives you a full history of everything you ran. From this, you can just copy paste over the commands that worked to your ```install_dependencies.sh``` script. This way, the ```install_dependencies.sh``` script will be bug-free and you can build without problems. And now you have an easy way to back-up the project. 

### Docker Commands:
* ```docker images``` lists all the images on a host machine
* ```docker container ls``` lists all the containers on a host machine
* ```docker rm <TAG>``` removes a container with TAG
* ```docker image rm <IMAGE NAME>``` deletes an image
* Once inside a container, ```Ctrl + P + Q``` detaches from the container, without killing processes
* ```docker attach <TAG>``` re-attaches to a detached container. Note that after running this command, you need to start typing to see the bash prompt. However, if a process was running, this will just hang, so you can detach again using the above command.
* Once inside a container, ```Ctrl + A + D``` exits the container and kills any processes within
#### Common Flags/Options: (to be used with ```docker run```
```docker run [OPTIONS] IMAGE [COMMAND] [ARG...]```
* ```--rm``` signals to remove the container after it is exited 
* ```--name``` names the container 
* ```-v``` mounts a host volume to a directory in the container (see ```./docker_run.py``` for an example of this)
* ```-e``` sets environment variables, for instance you may want to enable CUDA capabilities or X11/DISPLAY stuff
* ```-it``` instructs Docker to allocate a pseudo-TTY connected to the container’s stdin; creating an interactive bash shell in the container; note that this is equivalent to putting ```bash``` as your ```COMMAND``` in the docker run command
