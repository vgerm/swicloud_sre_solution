# Solution for SWI Cloud SRE Interview task

## Author

Vladimir Germanov

## Description

This solution works with Python 2.7 and 3.6. It requires appoptics-metrics py package

### How to run it manually via python

- Create python venv

```bash
# For Python 2
$ virtualenv venv/py2
# For Python 3
$ python3 -m venv venv/py3
```

- Activate python venv

```bash
# For Python 2
$ source venv/py2/bin/activate
# For Python 3
$ source venv/py3/bin/activate
```

- Install required py packages

```bash
# Install python pkgs
$ pip install -r requirements.txt
```

- Run the solution

```bash
# Showing help
$ python app/app.py -h
usage: app.py [-h] [-t TOKEN] [--version] [FILE [FILE ...]]

Solution for SolarWinds Cloud SRE Interview Task, v0.1

positional arguments:
  FILE                  file to read, if empty, stdin is used

optional arguments:
  -h, --help            show this help message and exit
  -t TOKEN, --api_token TOKEN
                        api authentication token, if empty, default is used
  --version             show programs version number and exit

Copyright 2019, Vladimir Germanov, MIT (see LICENSE or
https://opensource.org/licenses/MIT)

# Generate data
$ python timesink.py data.json > /path/to/metrics.json

# Upload metrics
$ python app/app.py /path/to/metrics.json
```

- Check dashboard [https://my.appoptics.com/s/public/zlh14ff2h](https://my.appoptics.com/s/public/zlh14ff2h)

### How to run it via Docker

- Build docker images

```bash
$ bash build_docker_images.sh
$ docker images
REPOSITORY                    TAG                 IMAGE ID            CREATED             SIZE
swicloud_sre_solution_py3.6   v0.1                01b16e992449        37 seconds ago      74.4MB
<none>                        <none>              fcfc0c9582b2        39 seconds ago      79.5MB
swicloud_sre_solution_py2.7   v0.1                3578eba9bc8e        44 seconds ago      58.3MB
```

- Run docker container

```bash
# Run docker container
# swicloud_sre_solution_py3.6:v0.1
$ docker run --rm swicloud_sre_solution_py3.6:v0.1
usage: app.py [-h] [-t TOKEN] [--version] [FILE [FILE ...]]

Solution for SolarWinds Cloud SRE Interview Task, v0.1

positional arguments:
  FILE                  file to read, if empty, stdin is used

optional arguments:
  -h, --help            show this help message and exit
  -t TOKEN, --api_token TOKEN
                        api authentication token, if empty, default is used
  --version             show programs version number and exit

# swicloud_sre_solution_py2.7:v0.1
$ docker run --rm swicloud_sre_solution_py2.7:v0.1
usage: app.py [-h] [-t TOKEN] [--version] [FILE [FILE ...]]

Solution for SolarWinds Cloud SRE Interview Task, v0.1

positional arguments:
  FILE                  file to read, if empty, stdin is used

optional arguments:
  -h, --help            show this help message and exit
  -t TOKEN, --api_token TOKEN
                        api authentication token, if empty, default is used
  --version             show programs version number and exit

# Generate random data
$ python timesink.py data.json > ./metrics.json

# Upload metrics via docker container
docker run -v $PWD:/data --rm swicloud_sre_solution_py3.6:v0.1 /data/metrics.json
docker run -v $PWD:/data --rm swicloud_sre_solution_py2.7:v0.1 /data/metrics.json
```

- Check dashboard [https://my.appoptics.com/s/public/zlh14ff2h](https://my.appoptics.com/s/public/zlh14ff2h)
