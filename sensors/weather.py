from log_conf import LoggerManager
import requests
import operator
from sensors.base import GenericSensorClass


class WeatherUndergroundSensor(GenericSensorClass):

    def __init__(self, api_key, zip):

        self.data = 0

        self.zipcode = zip
        self.apikey = api_key
        super(WeatherUndergroundSensor, self).__init__()

    def read(self):
        """
        read - Read data from the sensor

        :return: resulting JSON of the data after the call was made
        """
        # Execute any method in the base class prior to this method
        super(WeatherUndergroundSensor,self).read()

        base_url = "http://api.wunderground.com:80/api/{}".format(self.apikey)
        endpoint = "/conditions/q/{}.json".format(self.zipcode)

        url = base_url + endpoint

        if self._log:
            LoggerManager.logger.debug("API Call to: " + url)

        r = requests.get(url)

        json_string = r.json()

        if self._log:
            LoggerManager.logger.debug("requests Return Status Code: "+str(r.status_code))

        self.data = json_string['current_observation']['temp_f']

        if self._log:
            LoggerManager.logger.debug("Sensor read #"+ str(self._totalcount) + " Data returned: "+str(self.data))

        return self.data

    def compare(self, value, op_type):
        """
        This method will compare the retrieved sensor data with the value.
        If the value is less that data then this data returns true otherwise
        will be false.

        :param value: int value to compare against
               op_type: type of operator used to compare the values
        :return: bool result of comparison
        """

        ops = {'>': operator.gt,
               '<': operator.lt,
               '>=': operator.ge,
               '<=': operator.le,
               '=': operator.eq}

        if self._log:
            LoggerManager.logger.debug("Comparing {} with {} using operator '{}'".format(self.data, value, op_type))

        if ops[op_type](self.data,value) :
            self._sensorcount += 1
            return True
        else:
            return False
