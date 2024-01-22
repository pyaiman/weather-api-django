# weather-api-django
Django exercise to get data from weather API

By passing the name of a city it will return the data in json format.
#
# Endpoints
# user

|Endpoint                            | Resource                      | Authentication required |
|------------------------------------|-------------------------------|-------------------------|
|`/api/user/users/`                  | Retrieve list of users        |                         |
|`/api/user/users/<int:pk>/ `        | Retrieve a single user        |                         |
|`/api/user/users/<int:pk>/update/`  | Update a single user          |                         |
|`/api/user/users/<int:pk>/delete/`  | Delete a single user          |       X                 |
|`/api/user/create/`                 | Create a user                 |                         |
|`/api/user/token/`                  | Create authentication token   |                         |

#### Payload example for the creation of a user:
```json
{
    "email": "test@test.com",
    "password": "pass@123",
    "name": "Test Name"
}

```
#### Payload example for the creation of a token:
```json
{
    "email": "test@test.com",
    "password": "pass@123",
}
```

# weather-api
|Endpoint                              | Resource                      | Authentication required |
|--------------------------------------|-------------------------------|-------------------------|
|`/api/weather-api/weather-api-key/`   | Retrieve OpenWeather keys     |      X                  |
|`/api/weather-api/create/`            | Save an OpenWeather key       |      X                  |
|`/api/weather-api/weather/<str:city>` | Retrieve data for the weather |                         |

#### Payload example to save a OpenWeather key:
```json
{
    "weather_api_key": "weather-api-key"
}
```
Will return the following information about the queried city:

Field | Content | 
--- | --- | 
min | Minimum temperature in degrees Celsius. |
max | Maximum temperature in degrees Celsius. | 
feels_like | Feels like temperature in degrees Celsius. | 
city_name | Queried city's name. | 
country | Queried city's country code in the ISO 3166-1 alpha 3 format. | 


#

## Usage

To use the application you will need your own api key provided by the Open Weather API. You can get it [here](https://home.openweathermap.org/api_keys).

To retrieve data from the OpenWeather API follow this steps:

1. Create a new user on `/api/user/create/`
2. Create a token for the user on `/api/user/token/`
3. Save the OpenWeather Key from the OpenWeather site `/api/weather-api/create/`
4. Make a request `/api/weather-api/weather/`