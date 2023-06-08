from __future__ import annotations

from pydantic import BaseModel


class Weather(BaseModel):
    description: str
    category: str


class Wind(BaseModel):
    speed: float
    deg: float


class Forecast(BaseModel):
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    low: int
    high: int


class Location(BaseModel):
    city: str
    state: str
    country: str


class RateLimiting(BaseModel):
    unique_lookups_remaining: int
    lookup_reset_window: str


class WeatherModel(BaseModel):
    weather: Weather
    wind: Wind
    units: str
    forecast: Forecast
    location: Location
    rate_limiting: RateLimiting


data = {
    "weather": {
        "description": "broken clouds",
        "category": "Clouds"
    },
    "wind": {
        "speed": "5.75",
        "deg": 0.0
    },
    "units": "imperial",
    "forecast": {
        "temp": 74.79,
        "feels_like": 74.03,
        "pressure": 1012,
        "humidity": 44,
        "low": 68,
        "high": 80
    },
    "location": {
        "city": "Portland",
        "state": "OR",
        "country": "US"
    },
    "rate_limiting": {
        "unique_lookups_remaining": 49,
        "lookup_reset_window": "1 hour"
    }
}

report = WeatherModel(**data)

print("The weather is now:")
print(report.forecast)
