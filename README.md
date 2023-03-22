# KIOS Virtual City


## Table of Contents
**[Introduction](#introduction)**<br>
**[Installation](#installation)**<br>
**[Start-Stop](#Start-Stop)**<br>
**[Usage](#usage)**<br>
**[Troubleshooting](#troubleshooting)**<br>
**[Compatibility](#compatibility)**<br>

## Introduction

KIOS BaSP acts as the backend of Critical Infrastructure Systems simulators and testbeds.

![Image of KIOS Integrated Platform](KIOSIntegratedPlatform.jpg?raw=true)

## Installation

- Install [Docker](https://www.docker.com/) on your machine (If Docker cannot start with the error message `Cannot enable Hyper-V service` you have to enable Hyper-V (VTx) in system BIOS)
- Get the latest [Tag](https://github.com/KIOS-Research/KIOS-Virtual-City) from this repository
- Open Git Bash, got into `epanet` directory and run the following command `dos2unix.exe entrypoint.sh` 
- Open cmd/terminal, change directory to `KIOS-Virtual-City` directory and run the following command `docker-compose up -d --build --remove-orphans`
- Once the installation is finished, the KIOS Virtual City will be accessible from `http://localhost:8000/api`

- Note: To `STOP` AND `DELETE` the docker container use `docker-compose down --rmi local -v --remove-orphans` (you should do this action after you have FINISHED with all your experiments, and you want to delete all the data generated).  If you run this command you should re-build the container in order to use it, using `docker-compose up -d --build --remove-orphans`

&uparrow; [Back to top](#table-of-contents)

## Start-Stop

- After you have successfull installed Docker and KIOS Virtual City you can start/stop the container using the following two commands from within `KIOS-Virtual-City` directory
- Start: `docker-compose up`
- Stop: `docker-compose down`

&uparrow; [Back to top](#table-of-contents)

## Usage

Directories `MATLAB API Library` and `Python API Library` provide the appropriate libraries for REST API communication between BaSP and external tools.  Please refer to the documentation of the two libraries for further details.

For custom tools, the API documentation is provided on `http://localhost:8000/api/documentation/` after you run the docker containers.

The default login credentials for Grafana are:
`username:admin`
`password:admin`

&uparrow; [Back to top](#table-of-contents)

## Troubleshooting

If the API is not responding,
- Check if the containers are still running using the command `docker container ls`
- Stop and Restart the containers using the commands `docker-compose down -v` and `docker-compose up -d`
- **Use with extra Caution** Stop the containers using the command `docker-compose down -v`, fully delete all the images/containers using the command `docker-clear.bat`, and recreate the relevant containers using the command `docker-compose up -d --build`

&uparrow; [Back to top](#table-of-contents)

## Compatibility

KIOS Virtual City runs using [Docker](https://www.docker.com/), and can be executed on Linux, macOS and Windows.

&uparrow; [Back to top](#table-of-contents)

## Simple Scenario

After you have performed the installation as described in the [Installation](#installation), you should visit `http://localhost:8000/api/` in order to start using the platform.

In order to load `ltown` into the system, visit `http://localhost:8000/api/water/load/` and type `ltown` in the File field and then press POST.

You should then go to `http://localhost:8000/api/water/start/` in order to start the experiment.  Use a Startdate and an Enddate, give a proper experiment name and provide a proper Sensors input.  The sensors input should be a JSON formated string. See the example provided [example](exampleFiles/).

As soon as the experiment is executed, a Grafana dashboard URL will be given for fast representation of the data generated.  You can download or further manipulate the date using the appropriate API endpoints.  API documentation is provided at `http://localhost:8000/api/documentation/` on your machine.

You can also access the API using the provided `MATLAB API Library` and the `Python API Library`.  These are initial versions and will be extended based on user needs.