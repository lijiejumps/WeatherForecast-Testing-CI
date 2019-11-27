# Automated Unit Testing and Continuous Integration

Ryley Angus & Lin Li Jie


OpenWeatherMap API (free tier, https://openweathermap.org/guide#plans)


API Key: 55311979274630f8eba1933e5646b305

# CI/CD Configuration
image: python:3.7.


before_script:
1. python3 -m venv owmclient_venv
2. chmod +x owmclient_venv/bin/activate
3. ./owmclient_venv/bin/activate
4. pip install -r requirements.txt
 
test:
 script:
 1. chmod +x owmclient_venv/bin/activate
 2. ./owmclient_venv/bin/activate
 3. pytest -v --cov
