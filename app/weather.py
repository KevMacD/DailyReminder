import requests
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

# -----------------------------
# Helpers (internal)
# -----------------------------
def _req(d: Dict[str, Any], key: str) -> Any:
    if key not in d:
        raise KeyError(f"Missing required key: {key!r}")
    return d[key]

def _int_range(name: str, value: int, lo: int, hi: int) -> int:
    if not (lo <= value <= hi):
        raise ValueError(f"{name} out of range: {value} (expected {lo}..{hi})")
    return value

# -----------------------------
# Dataclasses
# -----------------------------
@dataclass
class CurrentWeather:
    dt: int
    temp: float
    weather: List[Dict[str, Any]]  # contains description, icon, etc.

    @property
    def dt_utc(self) -> datetime:
        return datetime.fromtimestamp(self.dt, tz=timezone.utc)

    def temp_c(self) -> float:
        return self.temp

    def temp_f(self) -> float:
        return self.temp * 9/5 + 32

    @property
    def description(self) -> str:
        if self.weather and "description" in self.weather[0]:
            return self.weather[0]["description"]
        return ""

@dataclass
class DailyForecast:
    dt: int
    temp: Dict[str, float]  # contains 'min', 'max', etc.
    weather: List[Dict[str, Any]]

    @property
    def dt_utc(self) -> datetime:
        return datetime.fromtimestamp(self.dt, tz=timezone.utc)

    @property
    def temp_max_c(self) -> float:
        return self.temp.get("max", 0.0)

    @property
    def temp_min_c(self) -> float:
        return self.temp.get("min", 0.0)

    @property
    def temp_max_f(self) -> float:
        return self.temp_max_c * 9/5 + 32

    @property
    def temp_min_f(self) -> float:
        return self.temp_min_c * 9/5 + 32

    @property
    def description(self) -> str:
        if self.weather and "description" in self.weather[0]:
            return self.weather[0]["description"]
        return ""

@dataclass
class OpenWeatherMapResponse:
    lat: float
    lon: float
    timezone: str
    timezone_offset_sec: int
    current: "CurrentWeather"
    daily: List[DailyForecast]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "OpenWeatherMapResponse":
        tz_off = int(_req(d, "timezone_offset"))
        _int_range("timezone_offset", tz_off, -14 * 3600, 14 * 3600)

        current_data = _req(d, "current")
        current = CurrentWeather(
            dt=int(_req(current_data, "dt")),
            temp=float(_req(current_data, "temp")),
            weather=current_data.get("weather", [])
        )

        daily_list = []
        for day in d.get("daily", []):
            daily_list.append(
                DailyForecast(
                    dt=int(_req(day, "dt")),
                    temp=_req(day, "temp"),
                    weather=day.get("weather", [])
                )
            )

        return cls(
            lat=float(_req(d, "lat")),
            lon=float(_req(d, "lon")),
            timezone=str(_req(d, "timezone")),
            timezone_offset_sec=tz_off,
            current=current,
            daily=daily_list
        )

    def to_local(self, dt_utc: datetime) -> datetime:
        """Convert UTC datetime to local time using timezone_offset_sec."""
        return dt_utc + timedelta(seconds=self.timezone_offset_sec)

    @property
    def current_local_time(self) -> datetime:
        return self.to_local(self.current.dt_utc)

# -----------------------------
# API call
# -----------------------------
def get_weather(lat: float, lon: float, api_key: str,
                exclude: Optional[str] = None, units: str = "standard") -> Dict[str, Any]:
    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": units
    }
    if exclude:
        params["exclude"] = exclude

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
