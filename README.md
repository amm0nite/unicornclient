[![PyPI version](https://badge.fury.io/py/unicornclient.svg)](https://badge.fury.io/py/unicornclient)

# unicornclient

## Raspbian installation
```
curl https://raw.githubusercontent.com/amm0nite/unicornclient/master/install/main.sh | bash -
```
### Optional dependencies

Install with apt:
```
apt install python3-microdotphat
```
Install with pip:
```
pip3 install picamera
pip3 install yoctopuce
```
## Docker image
```
docker run amm0nite/unicornclient
```
## Development
Create virtual env
```
virtualenv venv --python=python3.9
```
Activate virtual env
```
source venv/bin/activate
```
Install requirements
```
pip3 install -r requirements.txt
```
Install pylint
```
pip3 install pylint
```
