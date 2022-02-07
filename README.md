# NZ COVID-19 Locations of Interest
## About
Pulls NZ COVID-19 Locations of Interest from the Health Ministry's single JSON API endpoint here:
https://api.integration.covid19.health.nz/locations/v1/current-locations-of-interest

Aims to provide multiple views of the data by having new endpoints.

## License
Copyright &copy; 2022 Jared Daniel Recomendable.  
Licensed under the Apache License 2.0


## Usage
Endpoints are accessible from `/api/<version>/`.

The current `<version>` of the API is `v0`.

To interact with the server, one can make HTTP GET and POST requests to the following endpoints:
* `/`
* `/addresses`
* `/cities`
* `/exposure-types`
* `/location-names`
* `/suburbs`

To list all entries of locations of interest from the API (e.g. the `addresses` of all locations of interest, or all
`cities` with at least one location of interest), the user should send a HTTP GET request to the respective endpoint.

To filter for specific entries of locations of interest instead, the user should send a HTTP POST request to the
respective endpoint with a corresponding JSON body specifying the filters.

As an example, to obtain the list of all suburbs with locations of interest using `v0` of the API, the developer should
make a HTTP GET request to:
```
http://localhost:8080/api/v0/suburbs
```
The above example assumes that the server is hosted on the local machine, and is configured to be accessible from port
`8080`.

More details are shown below.

### Endpoints
#### `/`
TODO

#### `/addresses`
TODO

#### `/cities`
TODO

#### `/exposure-types`
TODO

#### `/location-names`
TODO

#### `/suburbs`
TODO

### Filtering Entries
As mentioned above, to obtain filtered lists of entries, the user should send a HTTP POST request to the respective
endpoint with a corresponding JSON body as part of the request.

TODO
