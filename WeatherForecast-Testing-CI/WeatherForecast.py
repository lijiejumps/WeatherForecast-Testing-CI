#!/usr/bin/env python3
import argparse
import json
import requests

from datetime import datetime

"""
API Key:	55311979274630f8eba1933e5646b305
Units:		Options are either units=metric (Celsius) or units=imperial (Fahrenheit)
		API default temperature format is Kelvin

Supported arguments:
	-api : API Key - String
	-city : City Name - String
	-cid : City ID - Number
	-gc : Geographic coordinates
	-z : Zip code - Alphanumeric - If no country code is specified, US is assumed
	-temp : Celsius or Fahrenheit (Default is Celsius) - Optional
	-time : Display local time for the requested location - No value provided - Optional
	-pressure : No value provided - Optional
	-cloud : No value provided - Optional
	-humidity : No value provided - Optional
	-wind : No value provided - Optional
	-sunset : No value provided - Optional
	-sunrise : No value provided - Optional
	-help : Display a help message (ignores all other options)
Notes:
	api must be provided.
	Exactly one of city, cid, gc or z must be provided.
	At least one of temp, time, pressure, cloud, humidity, wind, sunrise, sunset must be provided.
	If the help switch is passed, it trumps all other switches
"""


class OWMArgumentParser(argparse.ArgumentParser):

	def error(self, message):
		self.print_help()


class OWMClient:

	def __init__(self, argList=None):
		self.argList = argList
		self.args = None
		self.apiData = None

	def parseArguments(self):
		parser = OWMArgumentParser(description='OpenWeatherMap API Client', allow_abbrev=False)
		# api switch is always required
		parser.add_argument('--api', '-api', required=True, type=str, help='OpenWeatherMap API Key')

		parser.add_argument('--time', '-time', action='store_true', help='Display local time for the requested location')
		parser.add_argument('--temp', '-temp', type=str.lower, const="celsius", nargs='?', choices=['celsius', 'fahrenheit'], help='Temperature units (Celsius or Fahrenheit). Celsius is the default')
		parser.add_argument('--pressure', '-pressure', action='store_true', help='Display pressure information')
		parser.add_argument('--cloud', '-cloud', action='store_true', help='Display cloud cover information')
		parser.add_argument('--humidity', '-humidity', action='store_true', help='Display humidity information')
		parser.add_argument('--wind', '-wind', action='store_true', help='Display wind-speed information')
		parser.add_argument('--sunrise', '-sunrise', action='store_true', help='Display sunrise time')
		parser.add_argument('--sunset', '-sunset', action='store_true', help='Display sunset time')
		parser.add_argument('-help', action='store_true', help='Display program usage information')

		# This group is mutually exclusive as only one of the switches may be passed
		locationGroup = parser.add_mutually_exclusive_group(required=True)
		locationGroup.add_argument('--city', '-city', type=str, help='City name', metavar='<City Name>')
		locationGroup.add_argument('--cid', '-cid', type=int, help='OpenWeatherMap City ID', metavar='<OpenWeatherMap City ID>')
		locationGroup.add_argument('--gc', '-gc', action='store', nargs=2, help='Geographic co-ordinates (two space seperated numbers). Eg: ... -gc -38 145 ...', metavar=('<Latitude>', '<Longitude>'))
		locationGroup.add_argument('--z','-z', type=str, help='ZIP/Postal Code', metavar='<ZIP/Postal Code>')

		self.unknownArgs = []
		try:
			# argList is None when the client is directly run by the user
				# In this case, parse_args() will read the arguments from sys.argv
			if self.argList is not None:
				self.args, self.unknownArgs = parser.parse_known_args(self.argList)
			else:
				self.args, self.unknownArgs = parser.parse_known_args()
		except Exception:
			return -1

		# If any unrecognised arguments were provided, alert the user.
		if len(self.unknownArgs) > 0:
			parser.print_help()
			for unsupportedArg in self.unknownArgs:
				print("Error: Unknown argument: {0}".format(unsupportedArg))
			return -2

		# If "-help" was specified, ignore all other options
		if self.args.help is not False:
			parser.print_help()
			return -2

		# Only one of these switches may be provided
			# This is necessary as argparse doesn't seem to directly
			# support making one member of a mutually-exclusive group required
		if self.args.city is None and self.args.cid is None and self.args.gc is None and self.args.z is None:
			print("Error: A location must be specified")
			return -2

		# Check if any information has been requested for output
		if not (self.args.temp or self.args.time or self.args.pressure or self.args.cloud or self.args.humidity or self.args.wind or self.args.sunrise or self.args.sunset):
			print("No output requested.\nAt least one of -temp, -time, -pressure, -cloud, -humidity, -wind, -sunrise or -sunset must be provided")
			return -3
		# Zero is only returned if the arguments are legitimate
		return 0

	def requestData(self):
		# Request creation
		apiURL = None
		if self.args.city is not None:
			tempCity = self.args.city.replace(" ", "+")
			apiURL = "https://api.openweathermap.org/data/2.5/weather?q={0}&APPID={1}".format(tempCity, self.args.api)
		elif self.args.cid is not None:
			apiURL = "https://api.openweathermap.org/data/2.5/weather?id={0}&APPID={1}".format(self.args.cid, self.args.api)
		elif self.args.gc is not None:
			# Check the bounds for lat/lon
			latitude = self.args.gc[0]
			longitude = self.args.gc[1]
			apiURL = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&APPID={2}".format(latitude, longitude, self.args.api)
		elif self.args.z is not None:
			# The country code is hard coded to "Australia"
			apiURL = "https://api.openweathermap.org/data/2.5/weather?zip={0},au&APPID={1}".format(self.args.z, self.args.api)

		# The system of units should be specified, or else Kelvin is used for temperature
		if self.args.temp is None or self.args.temp == "celsius":
			apiURL += "&units=metric"
		elif self.args.temp == "fahrenheit":
			apiURL += "&units=imperial"

		apiReq = None

		# Request submission
		try:
			apiReq = requests.get(apiURL)
		except requests.exceptions.RequestException:
			print("Error occurred whilst connecting to OpenWeather service")
			return -1

		if apiReq.status_code != requests.codes.ok:
			# All errors are caught, but 401 can lead to a more descriptive error message
			if apiReq.status_code == 401:
				print("Authentication error - Please ensure your API key is valid")
			else:
				print("HTTP Error {0} occurred whilst retrieving data from OpenWeather service".format(apiReq.status_code))
			return -2

		try:
			self.apiData = json.loads(apiReq.content)
		except json.JSONDecodeError:
			# This should only occur if the response data is malformed
			print("Error: Invalid or empty response from OpenWeatherMap")
			return -3
		return 0

	def generateOutput(self):
		# Valid response processing
		# generateOutput returns a list of strings which can be printed to stdout via the displayData method
		outputList = []
		try:
			# Unlike the other switches, temp will be None if it is not provided
			if self.args.temp is not None:
				degreeSymbol = "C"
				if self.args.temp == "fahrenheit":
					degreeSymbol = "F"
				outputList.append("Current temperature: {0}°{1}".format(self.apiData["main"]["temp"], degreeSymbol))
				outputList.append("Forecast minimum temperature: {0}°{1}".format(self.apiData["main"]["temp_min"], degreeSymbol))
				outputList.append("Forecast maximum temperature: {0}°{1}".format(self.apiData["main"]["temp_max"], degreeSymbol))
			# The returned timestamp must be adjusted before being formatted for output
			if self.args.time is not False:
				locationTime = datetime.utcfromtimestamp(int(self.apiData["dt"]) + int(self.apiData["timezone"])).strftime("%H:%M %p")
				locationName = self.apiData["name"]
				# Not all locations have an associated name in OWM (particularly random co-ordinates in the ocean)
				if locationName != "":
					outputList.append("Time in {0} is {1}".format(locationName, locationTime))
				else:
					outputList.append("Time at requested location is {0}".format(locationTime))
			if self.args.humidity is not False:
				outputList.append("Humidity is {0}%".format(self.apiData["main"]["humidity"]))
			if self.args.pressure is not False:
				outputList.append("Atmospheric pressure is {0}hPa".format(self.apiData["main"]["pressure"]))
			if self.args.wind is not False:
				# The requested system of units affects the returned data for both temperature and wind speed
				if self.args.temp == "fahrenheit":
					outputList.append("Wind speed is {0} miles/hour from {1}°".format(self.apiData["wind"]["speed"], self.apiData["wind"]["deg"]))
				else:
					outputList.append("Wind speed is {0} metres/second from {1}°".format(self.apiData["wind"]["speed"], self.apiData["wind"]["deg"]))
			if self.args.cloud is not False:
				if len(self.apiData["weather"]) > 0:
					outputList.append("Weather description: {0}".format(self.apiData["weather"][0]["description"]))
			if self.args.sunrise is not False:
				sunriseTime = datetime.utcfromtimestamp(int(self.apiData["sys"]["sunrise"]) + int(self.apiData["timezone"])).strftime("%H:%M %p")
				outputList.append("Sunrise will be at {0}".format(sunriseTime))
			if self.args.sunset is not False:
				sunsetTime = datetime.utcfromtimestamp(int(self.apiData["sys"]["sunset"]) + int(self.apiData["timezone"])).strftime("%H:%M %p")
				outputList.append("Sunset will be at {0}".format(sunsetTime))
		except KeyError as err:
			outputList = ["Error occurred whilst accessing '{0}' in Weather data".format(err)]
		self.outputList = outputList
		return outputList

	def presentData(self):
		# presentData prints the generated output to the user
		self.generateOutput()
		for outputLine in self.outputList:
			print(outputLine)


if __name__ == "__main__":
	owmTest = OWMClient()
	argStatus = owmTest.parseArguments()
	if not argStatus:
		reqStatus = owmTest.requestData()
		if not reqStatus:
			owmTest.presentData()
