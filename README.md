#JSON-LD Wrapper for WeatherUnderground

##Installation
* Obtain an API key from Wunderground.com
* Setup a virtualenv and install the requirements from `requirements.txt`
* Copy `config.ini.template` to `config.ini` and set the API key appropriately
* Run `export FLASK_APP=wrapper.py` and `flask run --host 0.0.0.0`

##Usage
###Get compated JSON-LD
`http://host/weather/country/city/`
e.g. `http://host/weather/Germany/Karlsruhe/`

###Get expanded JSON-LD
`http://host/weather/country/city/expand`
e.g. `http://host/weather/Germany/Karlsruhe/expand`