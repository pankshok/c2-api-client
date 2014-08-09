# C2 EC2 API Client

Simple client for sending custom requests to CROC Cloud platform.
You may send requests in parallel and specify Availability Zones.

## Requirements

* python >= 2.6
* boto

## Usage

```
miushanov@think-x220:~/Documents/projects/c2-api-client$ ./c2-ec2 --help
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
```

## Examples

```
c2-ec2 <action> <arg1> <value1> <arg2> <value2>
```

### Send simple request

```
c2-ec2 RunInstances ImageId cmi-078880A0 Description "Test instance" \
InstanceType m1.micro MaxCount 1 MinCount 1 SecurityGroup.1 test
```

### Send parallel requests

Specify option `--threads` or `-t` and number of threads to run request in parallel.

Run 3 parallel requests for create instance:
```
c2-ec2 --threads 3 RunInstances ImageId cmi-078880A0 Description "Test instance" \
InstanceType m1.micro MaxCount 1 MinCount 1 SecurityGroup.1 test
```

### Send request to specified AZ

Specify option `--azs` and `--az-field` for send request to AZ.

Run one request for create instance in specified AZ:
```
c2-ec2 --azs devel-az1 --az-field Placement.AvailabilityZone \
RunInstances ImageId cmi-078880A0 Description "Test instance" \
InstanceType m1.micro MaxCount 1 MinCount 1 SecurityGroup.1 test
```

If you specify several AZs the requests become parallel to this AZs:

Run instances in different AZs:
```
c2-ec2 --azs devel-az1,devel-az2 --az-field Placement.AvailabilityZone \
RunInstances ImageId cmi-078880A0 Description "Test instance" \
InstanceType m1.micro MaxCount 1 MinCount 1 SecurityGroup.1 test
```
