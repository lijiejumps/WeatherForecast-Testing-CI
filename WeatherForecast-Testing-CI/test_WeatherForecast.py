#!/usr/bin/env python3

import unittest
import requests
from unittest import mock
from WeatherForecast import OWMClient


class MockResponse:
	def __init__(self, content, statusCode):
		self.content = reqContent
		self.status_code = status_code


def mocked_requests_get(url):
		# Use the two global variables to produce a mock requests/response object
		return MockResponse(reqContent, status_code)


def mocked_json_loads(input):
		# This returns a dictionary which contains none of the required weather data
		return {"mocking": "yes"}


class OWMClientTests(unittest.TestCase):

	def setUp(self):
		self.argList = None
		self.retVals = None
		self.outputList = None
		self.name = None

	def OWMClientDemo(self):
		# Create an instance of the client, and supply it with command-line arguments
		owmTest = OWMClient(self.argList)
		argStatus = owmTest.parseArguments()
		self.assertEqual(argStatus, self.retVals[0])
		if not argStatus:
			# If the arguments were parsed without error, request the data from "OWM"
			reqStatus = owmTest.requestData()
			self.assertEqual(reqStatus, self.retVals[1])
			if not reqStatus:
				generatedList = owmTest.generateOutput()
				# Compare the generated output to the pre-defined output at this point
				self.assertEqual(len(self.outputList), len(generatedList))
				# Each line in the returned data is compared to its expected value
				# The order of the strings is deterministic
				for i in range(0, len(generatedList)):
					self.assertEqual(self.outputList[i], generatedList[i])
				owmTest.presentData()

	"""
	Each test contains the expected return values from the argument parsing and web request methods.
	If the argument parsing is expected to suceed, the web request is mocked with pre-defined data.
	The command-line arguments are also specified for each case, along with a descriptive name and the expected output.
	"""

	@mock.patch('requests.get', side_effect=mocked_requests_get)
	def test_1_celsius_city_name(self, reqMock):
		global reqContent
		reqContent = b'{"coord":{"lon":144.96,"lat":-37.81},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],"base":"stations","main":{"temp":14.67,"pressure":1015,"humidity":50,"temp_min":12.22,"temp_max":16.11},"visibility":10000,"wind":{"speed":10.3,"deg":310,"gust":17.5},"clouds":{"all":75},"dt":1571356593,"sys":{"type":1,"id":9554,"message":0.0078,"country":"AU","sunrise":1571340696,"sunset":1571387940},"timezone":39600,"id":2158177,"name":"Melbourne","cod":200}'
		global status_code
		status_code = 200

		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-temp", "celsius", "-pressure", "-cloud", "-humidity", "-wind", "-sunrise", "-sunset", "-time", "-city", "melbourne"]
		self.retVals = [0, 0]
		self.outputList = ["Current temperature: 14.67°C",
					"Forecast minimum temperature: 12.22°C",
					"Forecast maximum temperature: 16.11°C",
					"Time in Melbourne is 10:56 AM",
					"Humidity is 50%",
					"Atmospheric pressure is 1015hPa",
					"Wind speed is 10.3 metres/second from 310°",
					"Weather description: broken clouds",
					"Sunrise will be at 06:31 AM",
					"Sunset will be at 19:39 PM"]
		self.name = "Temperature units set to celsius, city is provided by name"
		self.OWMClientDemo()

	@mock.patch('requests.get', side_effect=mocked_requests_get)
	def test_2_temp_unspec_time(self, reqMock):
		global reqContent
		reqContent = b'{"coord":{"lon":-0.13,"lat":51.51},"weather":[{"id":520,"main":"Rain","description":"light intensity shower rain","icon":"09n"}],"base":"stations","main":{"temp":10.37,"pressure":1001,"humidity":87,"temp_min":8.89,"temp_max":12.22},"visibility":10000,"wind":{"speed":3.1,"deg":160},"rain":{"1h":0.25},"clouds":{"all":33},"dt":1571359420,"sys":{"type":1,"id":1414,"message":0.0104,"country":"GB","sunrise":1571380123,"sunset":1571418147},"timezone":3600,"id":2643743,"name":"London","cod":200}'
		global status_code
		status_code = 200
		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-temp", "-time", "-city", "london"]
		self.retVals = [0, 0]
		self.outputList = ["Current temperature: 10.37°C",
					"Forecast minimum temperature: 8.89°C",
					"Forecast maximum temperature: 12.22°C",
					"Time in London is 01:43 AM"]
		self.name = "Temperature output requested, but units unspecified. Only temp and time are requested for output"
		self.OWMClientDemo()

	@mock.patch('requests.get', side_effect=mocked_requests_get)
	def test_3_temp_fahrenheit_all_output(self, reqMock):
		global reqContent
		reqContent = b'{"coord":{"lon":-0.13,"lat":51.51},"weather":[{"id":520,"main":"Rain","description":"light intensity shower rain","icon":"09n"}],"base":"stations","main":{"temp":50.68,"pressure":1001,"humidity":87,"temp_min":48,"temp_max":54},"visibility":10000,"wind":{"speed":6.93,"deg":160},"rain":{"1h":0.25},"clouds":{"all":33},"dt":1571359266,"sys":{"type":1,"id":1414,"message":0.0108,"country":"GB","sunrise":1571380123,"sunset":1571418147},"timezone":3600,"id":2643743,"name":"London","cod":200}'
		global status_code
		status_code = 200
		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-temp", "fahrenheit", "-pressure", "-cloud", "-humidity", "-wind", "-sunrise", "-sunset", "-time", "-city", "london"]
		self.retVals = [0, 0]
		self.outputList = ["Current temperature: 50.68°F",
					"Forecast minimum temperature: 48°F",
					"Forecast maximum temperature: 54°F",
					"Time in London is 01:41 AM",
					"Humidity is 87%",
					"Atmospheric pressure is 1001hPa",
					"Wind speed is 6.93 miles/hour from 160°",
					"Weather description: light intensity shower rain",
					"Sunrise will be at 07:28 AM",
					"Sunset will be at 18:02 PM"]
		self.name = "Fahrenheit used for temperature units, all output options provided."
		self.OWMClientDemo()

	@mock.patch('requests.get', side_effect=mocked_requests_get)
	def test_4_loc_coords_limited_output(self, reqMock):
		global reqContent
		reqContent = b'{"coord":{"lon":145,"lat":-38},"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}],"base":"stations","main":{"temp":15.74,"pressure":1015,"humidity":47,"temp_min":13.33,"temp_max":17.78},"visibility":10000,"wind":{"speed":7.7,"deg":330,"gust":13.4},"clouds":{"all":40},"dt":1571359098,"sys":{"type":1,"id":9554,"message":0.008,"country":"AU","sunrise":1571340673,"sunset":1571387944},"timezone":39600,"id":7932652,"name":"Black Rock","cod":200}'
		global status_code
		status_code = 200
		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-pressure", "-sunrise", "-sunset", "-time", "-gc", "-38", "145"]
		self.retVals = [0, 0]
		self.outputList = ["Time in Black Rock is 11:38 AM",
					"Atmospheric pressure is 1015hPa",
					"Sunrise will be at 06:31 AM",
					"Sunset will be at 19:39 PM"]
		self.name = "Location via co-ordinates, only pressure, sunrise, and sunset are requested for output"
		self.OWMClientDemo()

	@mock.patch('requests.get', side_effect=mocked_requests_get)
	def test_5_loc_coords_unnamed_location(self, reqMock):
		global reqContent
		reqContent = b'{"coord":{"lon":-1,"lat":-1},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}],"base":"stations","main":{"temp":26.07,"pressure":1013.24,"humidity":73,"temp_min":26.07,"temp_max":26.07,"sea_level":1013.24,"grnd_level":1013.27},"wind":{"speed":4.04,"deg":232.245},"clouds":{"all":90},"dt":1571358925,"sys":{"message":0.0075,"sunrise":1571377501,"sunset":1571421186},"timezone":0,"id":0,"name":"","cod":200}'
		global status_code
		status_code = 200

		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-pressure", "-sunrise", "-sunset", "-time", "-gc", "-1", "-1"]
		self.retVals = [0, 0]
		self.outputList = ["Time at requested location is 00:35 AM",
					"Atmospheric pressure is 1013.24hPa",
					"Sunrise will be at 05:45 AM",
					"Sunset will be at 17:53 PM"]
		self.name = "Location via co-ordinates, specified location has no associated name in OWM response"
		self.OWMClientDemo()

	@mock.patch('requests.get', side_effect=mocked_requests_get)
	def test_6_loc_id(self, reqMock):
		global reqContent
		reqContent = b'{"coord":{"lon":-0.13,"lat":51.51},"weather":[{"id":522,"main":"Rain","description":"heavy intensity shower rain","icon":"09n"}],"base":"stations","main":{"temp":10.44,"pressure":1001,"humidity":87,"temp_min":8.89,"temp_max":12.22},"visibility":10000,"wind":{"speed":3.1,"deg":160},"rain":{"1h":0.25},"clouds":{"all":33},"dt":1571358781,"sys":{"type":1,"id":1414,"message":0.0116,"country":"GB","sunrise":1571380123,"sunset":1571418147},"timezone":3600,"id":2643743,"name":"London","cod":200}'
		global status_code
		status_code = 200
		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-humidity", "-cloud", "-humidity", "-time", "-cid", "2643743"]
		self.retVals = [0, 0]
		self.outputList = ["Time in London is 01:33 AM",
					"Humidity is 87%",
					"Weather description: heavy intensity shower rain"]
		self.name = "Location via cid"
		self.OWMClientDemo()

	@mock.patch('requests.get', side_effect=mocked_requests_get)
	def test_7_loc_cid_dupe_option(self, reqMock):
		global reqContent
		reqContent = b'{"coord":{"lon":-0.13,"lat":51.51},"weather":[{"id":502,"main":"Rain","description":"heavy intensity rain","icon":"10n"}],"base":"stations","main":{"temp":10.57,"pressure":1002,"humidity":87,"temp_min":9.44,"temp_max":12.22},"visibility":10000,"wind":{"speed":3.6,"deg":170},"rain":{"1h":0.51},"clouds":{"all":17},"dt":1571355246,"sys":{"type":1,"id":1414,"message":0.0094,"country":"GB","sunrise":1571380123,"sunset":1571418147},"timezone":3600,"id":2643743,"name":"London","cod":200}'
		global status_code
		status_code = 200

		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-humidity", "-cloud", "-humidity", "-time", "-cid", "2643743", "-humidity"]
		self.retVals = [0, 0]
		self.outputList = ["Time in London is 00:34 AM",
					"Humidity is 87%",
					"Weather description: heavy intensity rain"]
		self.name = "Location via cid, output option humidity is duplicated"
		self.OWMClientDemo()

	@mock.patch('requests.get', side_effect=mocked_requests_get)
	def test_8_post_code_wind_time(self, reqMock):
		global reqContent
		reqContent = b'{"coord":{"lon":-0.13,"lat":51.51},"weather":[{"id":522,"main":"Rain","description":"heavy intensity shower rain","icon":"09n"}],"base":"stations","main":{"temp":10.47,"pressure":1002,"humidity":87,"temp_min":8.89,"temp_max":12.22},"visibility":10000,"wind":{"speed":3.6,"deg":160},"rain":{"1h":0.25},"clouds":{"all":33},"dt":1571358599,"sys":{"type":1,"id":1414,"message":0.0104,"country":"GB","sunrise":1571380123,"sunset":1571418147},"timezone":3600,"id":2643743,"name":"London","cod":200}'
		global status_code
		status_code = 200

		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-wind", "-time", "-cid", "2643743"]
		self.retVals = [0, 0]
		self.outputList = ["Time in London is 01:29 AM",
					"Wind speed is 3.6 metres/second from 160°"]
		self.name = "Location via post code, only wind and time are requested"
		self.OWMClientDemo()

	def test_9_help_included_with_other_options(self):
		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-pressure", "-cloud", "-humidity", "-wind", "-sunrise", "-sunset", "-time", "-cid", "2643743", "-help"]
		self.retVals = [-2, 0]
		self.outputList = []
		self.name = "Help specified alongside actual arguments"
		self.OWMClientDemo()

	@mock.patch('requests.get', side_effect=mocked_requests_get)
	def test_10_loc_post_code(self, reqMock):
		global reqContent
		reqContent = b'{"coord":{"lon":145.12,"lat":-38.14},"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}],"base":"stations","main":{"temp":15.34,"pressure":1015,"humidity":47,"temp_min":13.33,"temp_max":16.67},"visibility":10000,"wind":{"speed":7.7,"deg":330,"gust":13.4},"clouds":{"all":40},"dt":1571358167,"sys":{"type":1,"id":9554,"message":0.01,"country":"AU","sunrise":1571340635,"sunset":1571387924},"timezone":39600,"id":0,"name":"Frankston","cod":200}'
		global status_code
		status_code = 200

		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-wind", "-sunrise", "-sunset", "-time", "-z", "3199"]
		self.retVals = [0, 0]
		self.outputList = ["Time in Frankston is 11:22 AM",
					"Wind speed is 7.7 metres/second from 330°",
					"Sunrise will be at 06:30 AM",
					"Sunset will be at 19:38 PM"]
		self.name = "Location via post code"
		self.OWMClientDemo()

	@mock.patch('requests.get', side_effect=mocked_requests_get)
	def test_11_http_error_response_object(self, reqMock):
		global reqContent
		reqContent = None
		global status_code
		status_code = 400

		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-pressure", "-cloud", "-humidity", "-wind", "-sunrise", "-sunset", "-time", "-city", "melbourne"]
		self.retVals = [0, -2]
		self.outputList = []
		self.name = "Test HTTP error response from OWM"
		self.OWMClientDemo()

	@mock.patch('requests.get', side_effect=mocked_requests_get)
	def test_12_empty_response_object(self, reqMock):
		global reqContent
		reqContent = ""
		global status_code
		status_code = 200

		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-pressure", "-cloud", "-humidity", "-wind", "-sunrise", "-sunset", "-time", "-city", "melbourne"]
		self.retVals = [0, -3]
		self.outputList = []
		self.name = "Test valid, but empty response from OWM"
		self.OWMClientDemo()

	@mock.patch('requests.get', side_effect=requests.exceptions.RequestException())
	def test_13_requests_exception(self, reqMock):
		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-pressure", "-cloud", "-humidity", "-wind", "-sunrise", "-sunset", "-time", "-city", "melbourne"]
		self.retVals = [0, -1]
		self.outputList = []
		self.name = "Test exception on request from OWM"
		self.OWMClientDemo()

	@mock.patch('requests.get', side_effect=mocked_requests_get)
	@mock.patch('json.loads', side_effect=mocked_json_loads)
	def test_14_invalid_data_dict(self, reqMock, jsonMock):
		global reqContent
		reqContent = b'{"coord":{"lon":144.96,"lat":-37.81},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}],"base":"stations","main":{"temp":14.67,"pressure":1015,"humidity":50,"temp_min":12.22,"temp_max":16.11},"visibility":10000,"wind":{"speed":10.3,"deg":310,"gust":17.5},"clouds":{"all":75},"dt":1571356817,"sys":{"type":1,"id":9554,"message":0.0106,"country":"AU","sunrise":1571340696,"sunset":1571387940},"timezone":39600,"id":2158177,"name":"Melbourne","cod":200}'
		global status_code
		status_code = 200

		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-pressure", "-cloud", "-humidity", "-wind", "-sunrise", "-sunset", "-time", "-city", "melbourne"]
		self.retVals = [0, 0]
		self.outputList = ["Error occurred whilst accessing ''dt'' in Weather data"]
		self.name = "Test JSON error whilst parsing response from OWM"
		self.OWMClientDemo()

	@mock.patch('requests.get', side_effect=mocked_requests_get)
	def test_15_invalid_data_dict(self, reqMock):
		global reqContent
		reqContent = b'{"cod":401, "message": "Invalid API key. Please see http://openweathermap.org/faq#error401 for more info."}'
		global status_code
		status_code = 401

		self.argList = ["-api", "invalid", "-pressure", "-cloud", "-humidity", "-wind", "-sunrise", "-sunset", "-time", "-city", "melbourne"]
		self.retVals = [0, -2]
		self.outputList = []
		self.name = "Test invalid API key response from OWM"
		self.OWMClientDemo()

	def test_16_no_location_specified(self):
		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-pressure", "-cloud", "-humidity", "-wind", "-sunrise", "-sunset", "-time"]
		self.retVals = [-2, -2]
		self.outputList = []
		self.name = "Test absent location in given arguments"
		self.OWMClientDemo()

	def test_17_api_switch_missing(self):
		self.argList = ["-pressure", "-cloud", "-humidity", "-wind", "-sunrise", "-sunset", "-time"]
		self.retVals = [-2, -2]
		self.outputList = []
		self.name = "Test missing api switch in provided arguments"
		self.OWMClientDemo()

	def test_18_no_output_requested(self):
		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-cid", "2643743"]
		self.retVals = [-3, 0]
		self.outputList = []
		self.name = "No output is requested"
		self.OWMClientDemo()

	def test_19_multi_loc_options(self):
		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-pressure", "-cloud", "-humidity", "-wind", "-sunrise", "-sunset", "-time", "-cid", "2643743", "-city", "melbourne"]
		self.retVals = [-1, 0]
		self.outputList = []
		self.name = "Duplicate location switches provided (cid and city)"
		self.OWMClientDemo()

	def test_20_unknown_option(self):
		self.argList = ["-api", "55311979274630f8eba1933e5646b305", "-pressure", "-cloud", "-humidity", "-wand", "-sunrise", "-sunset", "-time", "-cid", "2643743"]
		self.retVals = [-2, 0]
		self.outputList = []
		self.name = "Unknown option provided (-wand)"
		self.OWMClientDemo()


reqContent = None
status_code = 200
if __name__ == '__main__':
	unittest.main()
