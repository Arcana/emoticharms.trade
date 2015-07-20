# emoticharms.trade

Code behind emoticharms.trade to enable trading of Emoticharm packs at TI5

## Installation

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
npm install && npm install -g webpack
webpack
```

## Usage

### Development

```
source env/bin/activate
webpack --watch
python manager.py runserver
```
