# C2 EC2 API Client

Simple command-line utility for sending custom requests to CROC Cloud platform.
You may send requests in parallel and specify Availability Zones.

**Warning: this utility is not intended for automation cases.
Use https://github.com/C2Devel/boto.git and python scripts instead.**

## Requirements

* python >= 2.6
* boto

## Usage

    $ c2-ec2 --help
    usage: c2-ec2 [-h] [-t threads] [--azs AZ,[AZ,[...]]] [--az-field AZ_FIELD]
                  action [parameters [parameters ...]]

    positional arguments:
      action                The action that you want to perform.
      parameters            Any parameters for the action. Parameters specified by
                            parameter key and parameter value separated by space.

    optional arguments:
      -h, --help            show this help message and exit
      -t threads, --threads threads
                            Number of threads to perform request.
      --azs AZ,[AZ,[...]]   Comma-separated list of AZs.
      --az-field AZ_FIELD   EC2 AZ request field. Default: 'AvailabilityZone'

## Examples

1. Common syntax:

    ```
    c2-ec2 <action> <arg1> <value1> <arg2> <value2>
    ```

1. Send simple request

    ```
    c2-ec2 RunInstances ImageId cmi-078880A0 Description "Test instance" \
    InstanceType m1.small MaxCount 1 MinCount 1 SecurityGroup.1 test
    ```

1. To send requests to specified AZ add options `--azs` and `--az-field`.
  1. Run one request to create instance in specified AZ:

    ```
    c2-ec2 --azs ru-msk-comp1 --az-field Placement.AvailabilityZone \
    RunInstances ImageId cmi-078880A0 Description "Test instance" \
    InstanceType m1.small MaxCount 1 MinCount 1 SecurityGroup.1 test
    ```

  1. Specifing several AZs in CLI will cause parallel requests to these AZs (running instances in different AZs):

    ```
    c2-ec2 --azs ru-msk-comp1,ru-msk-vol51 --az-field Placement.AvailabilityZone \
    RunInstances ImageId cmi-078880A0 Description "Test instance" \
    InstanceType m1.small MaxCount 1 MinCount 1 SecurityGroup.1 test
    ```
