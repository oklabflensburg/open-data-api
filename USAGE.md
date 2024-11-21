# API - Usage Examples


## Overview

This guide provides examples of how to retrieve energy unit and administrative area data using the OK Lab Flensburg API. The examples use the `wget` command for simplicity. Replace the placeholder values (e.g., `unit_id`, `municipality_key`, or `municipality_name`) with your desired input.


---


## Combustion Units

Retrieve Details of a Specific Combustion Unit

```sh
wget https://api.oklabflensburg.de/energy/v1/unit/combustion/id?unit_id=SEE951839779134
```

Retrieve All Combustion Units in a Municipality

```sh
wget https://api.oklabflensburg.de/energy/v1/unit/combustion/key?municipality_key=01002000
```


---


## Solar Units

Retrieve Details of a Specific Solar Unit

```sh
wget https://api.oklabflensburg.de/energy/v1/unit/solar/id?unit_id=SEE987254504556
```

Retrieve All Solar Units in a Municipality

```sh
wget https://api.oklabflensburg.de/energy/v1/unit/solar/key?municipality_key=01059113
```


---


## Wind Turbine Units


Retrieve Details of a Specific Wind Turbine Unit

```sh
wget https://api.oklabflensburg.de/energy/v1/unit/wind/id?unit_id=SEE959176892240
```


Retrieve All Wind Turbine Units in a Municipality

```sh
wget https://api.oklabflensburg.de/energy/v1/unit/wind/key?municipality_key=01059113
```


---


## Biomass Units

Retrieve Details of a Specific Biomass Unit

```sh
wget https://api.oklabflensburg.de/energy/v1/unit/biomass/id?unit_id=SEE902321614457
```


Retrieve All Biomass Units in a Municipality

```sh
wget https://api.oklabflensburg.de/energy/v1/unit/biomass/key?municipality_key=01001000
```


---


## Nuclear Units

Retrieve Details of a Specific Nuclear Unit

```sh
wget https://api.oklabflensburg.de/energy/v1/unit/nuclear/id?unit_id=SEE951462745445
```

Retrieve All Nuclear Units in a Municipality

```sh
wget https://api.oklabflensburg.de/energy/v1/unit/nuclear/key?municipality_key=01061018
```


---


## Water Units

Retrieve Details of a Specific Water Unit

```sh
wget https://api.oklabflensburg.de/energy/v1/unit/water/id?unit_id=SEE993329981764
```

Retrieve All Water Units in a Municipality

```sh
wget https://api.oklabflensburg.de/energy/v1/unit/water/key?municipality_key=01001000
```


---


## Administrative Data

Retrieve Municipality Information

```sh
wget https://api.oklabflensburg.de/administrative/v1/municipality?municipality_name=flensburg
```


---


## Notes

- Replace `unit_id` with the 15-digit registration number of the unit you are querying.
- Replace `municipality_key` (AGS) with the official municipality key of your area of interest.
- Replace `municipality_name` with the name of the desired municipality.