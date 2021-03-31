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
* Note that setting up the dockerfile is the most important part of this setup. If your ```install_dependencies.sh``` script has errors, then the build will fail. Thus, I recommend that you first make a very minimal docker container, for instance, 

```nvidia-docker run --runtime=nvidia -it -e NVIDIA_VISIBLE_DEVICES=0 --rm -v /raid/priya/:/data nvidia/cuda:8.0-devel-ubuntu16.04 bash```
* To unpack this, it launches a container with GPU 0 visible, and mounts whatever is stored in `/raid/priya/data` on the host machine to `/data` inside the container. This is also launching from a base, bare-bones Ubuntu 16.04 image.

* Then, from inside this container, you can try installing whatever you want as you normally would. Then, using the ```history``` command gives you a full history of everything you ran. From this, you can just copy paste over the commands that worked to your ```install_dependencies.sh``` script. This way, the ```install_dependencies.sh``` script will be bug-free and you can build without problems. And now you have an easy way to back-up the project. 

### Docker Commands:
* ```docker images``` lists all the images on a host machine
* ```docker container ls``` lists all the containers on a host machine
* ```docker rm <TAG>``` removes a container with TAG
* ```docker image rm <IMAGE NAME>``` deletes an image
* Once inside a container, ```Ctrl + P + Q``` detaches from the container, without killing processes
* ```docker attach <TAG>``` re-attaches to a detached container. Note that after running this command, you need to start typing to see the bash prompt. However, if a process was running, this will just hang, so you can detach again using the above command.
* Once inside a container, ```Ctrl + A + D``` exits the container and kills any processes within
#### Common Flags/Options: (to be used with ```docker run```)
>>>>>>> 7b7694c87b158c4b81dbd7ec8705a4a85ed3849d
```docker run [OPTIONS] IMAGE [COMMAND] [ARG...]```
* ```--rm``` signals to remove the container after it is exited 
* ```--name``` names the container 
* ```-v``` mounts a host volume to a directory in the container (see ```./docker_run.py``` for an example of this)
* ```-e``` sets environment variables, for instance you may want to enable CUDA capabilities or X11/DISPLAY stuff
* ```-it``` instructs Docker to allocate a pseudo-TTY connected to the container’s stdin; creating an interactive bash shell in the container; note that this is equivalent to putting ```bash``` as your ```COMMAND``` in the docker run command

### My typical workflow 
* For any project on a remote machine, I like to use the GNU program `screen` and Docker to do all my work. Others prefer `tmux` and `virtualenv` or a host of other things, and this is just what works for me!
* `screen` is basically a way to get multiple Terminal tabs in one window; this is especially useful when you're `ssh`'d  in somewhere  and dont want to have to keep `ssh`'ing  every  time  you  need a new window
* The other really useful thing about  `screen` is that once you `ssh` to a machine, start a process by running one of your scripts, you want it to keep going and not terminate; however, if the `ssh` connection is lost, the process will be killed. To avoid this, it's best to `ssh`, create a `screen` which will start any  processes, detach from the screen, and then log out of the remote host. Thus, even though you logged out and the connection was lost, your process will keep running and you can check up on it any time by `ssh`'ing back in, and attaching to the screen. This sounds complicated but really you only need to know like 3 commands.
* Some quick setup for using `screen`:
 * Make a file at `~/.screenrc` on your remote host containing the following:
```
caption string "%?%F%{= Bk}%? %C%A %D %d-%m-%Y %{= kB} %t%= %?%F%{= Bk}%:%{= wk}%? %n "
shell -$SHELL
hardstatus alwayslastline
hardstatus string '%{= kG}[ %{G}%H %{g}][%= %{= kw}%?%-Lw%?%{r}(%{W}%n*%f%t%?(%u)%?%{r})%{w}%?%+Lw%?%?%= %{g}][%{B} %d/%m %{W}%c %{g}]'
```
* `screen` usage:
 * `screen -RD` is pretty much all you need to start up a new screen, or attach to an existing one
 * After running this, you can use `Ctrl+A+C` to get a new `screen` or virtual tab, enumerated at the bottom
 * `Ctrl A+P` and `Ctrl A+N` toggle between the previous and next screens 
 * Finally, `Ctrl A+D` detaches from the screen 
#### Putting it all together
* So, the easiest way to deal with Docker on a remote machine is first `ssh`, start a screen with `screen -RD`, then, enter your container using  `./docker_run.py`. Start any processes you want (training, etc.) and then just run `Ctrl A+D` which detaches from the `screen`, but crucially, not from the container. Now, you can safely logout of the remote machine and ensure that your training job is running inside Docker where it has all its dependencies, and also inside `screen`, so that the process will not be killed upon logout. 
* Whenever you want to run inference/check up on the job, `ssh` back in, run `screen -RD` and you will already be inside the container and able to do your development.
* Note; with this, it's possible to just work in the same Docker container for a long period of time, without having to re-make new ones or kill old ones. And, if you ever want a normal Terminal tab or want to launch a separate container, you can just get a new Terminal tab with `Ctrl+A+C` without having to kill an existing container, and re-launch a different container, etc.
