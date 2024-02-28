# San_Jose_illegal_Dumping

# Instructions

To get started we will need to build our container. To do so, access the [scr]('./src') folder as your working directory in bash and run ```docker build -t {image_name} . ``` then to run our docker container we will need to run ```winpty docker run -it {image_name} ``` note that the ```-it``` portion indicates we want to run it in interactive mode and ```winpty``` will only be needed if you're using git bash on a windows machine. You can check if a container has been built by running ```docker ps -a``` in your command line. The ```-a``` includes all containers, both active and inactive ones. 

For example, if i run ``` docker build -t test .``` and ```winpty docker run -it test ``` will create a container and run what ever is set up in the docker file. Then to see if it was successful we can run ```docker ps -a```.

The results should show something like:
|Container ID|Image|Command|Created|Status|Ports|Names|
|---------|---------|---------|---------|---------|---------|---------|
|cj39jwjcsl|test|python api_pull.py|xx seconds ago|Exited (0) 9 seconds ago||random_name24|

With that information we can check logs by running ```docker logs {name}``` name being whats under the names column. In this example, it would be ```docker logs random_name24```. Since I'm running only a python script the results will return the output of the python script. In my case it was a script to create a csv file if one didn't exist. Which verbatim looks like.

```   
/app/api_pull.py:2: DeprecationWarning:
Pyarrow will become a required dependency of pandas in the next major release of pandas (pandas 3.0),
(to allow more performant data types, such as the Arrow string type, and better interoperability with other libraries)
but was not found to be installed on your system.
If this would cause problems for you,
please provide us feedback at https://github.com/pandas-dev/pandas/issues/54466

  import pandas as pd
illegal dumping csv created

```

This is simply a warning that a feature of a library I used for my script may change in the future. Which can be ignored by specify which version of a Library I want to use, but this is essentially what logs will look like.
