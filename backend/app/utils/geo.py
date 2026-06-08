# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: geospatial helpers for ImmuneNet scan validation.

from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS_M = 6_371_000


def haversine_distance_m(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    rlat1 = radians(lat1)
    rlat2 = radians(lat2)

    a = sin(dlat / 2) ** 2 + cos(rlat1) * cos(rlat2) * sin(dlng / 2) ** 2
    c = 2 * asin(sqrt(a))
    return EARTH_RADIUS_M * c


def is_within_geofence(
    gps_lat: float,
    gps_lng: float,
    hub_lat: float,
    hub_lng: float,
    radius_m: float,
    gps_accuracy_m: float | None = None,
) -> tuple[bool, float]:
    distance_m = haversine_distance_m(gps_lat, gps_lng, hub_lat, hub_lng)
    accuracy_allowance = min(gps_accuracy_m, 50) if gps_accuracy_m is not None else 0
    return distance_m <= radius_m + accuracy_allowance, distance_m
