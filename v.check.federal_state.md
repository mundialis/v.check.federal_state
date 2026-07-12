## DESCRIPTION

*v.check.federal_state* checks in which German federal state an area of
interest is located. The vector map aoi (area of interest) has to be
given in the GRASS DB. The data for the federal states boundaries are
downloaded from the BKG. To speed up the module, the federal state
boundaries can als be given as optional input: **federal_states**. To
generate this input the module can be run once with the optinal option
**output**. The returning output-map can then be used as
**federal_states** input in following module runs (See example below).
Further the optional option **federal_state_file** can be set. With this
option the printed output (federal state of given polygon) will be
written into a file, defined by **federal_state_file**. If the polygon
is not in Germany, no file be generated.

## EXAMPLE

### Check federal state for a given polygon in Hamburg, named=poly_HH.

```sh
v.check.federal_state aoi=poly_HH
```

### Check federal state for a given polygon in Hamburg and save it in a file

```sh
v.check.federal_state aoi=poly_HH federal_state_file=poly_HH_federal_state.txt
```

### Check federal state for a given polygon in Hamburg, named 'poly_HH', and save the federal state boundaries as 'federal_states'.

```sh
v.check.federal_state aoi=poly_HH output=federal_states
```

### Save federal states data, to avoid downloading them each time calling v.check.federal_state.

First step: Run module once, to generate federal_states output

```sh
v.check.federal_state aoi=poly_HH output=federal_states
```

Second step: Next time the module can be run by giving federal_states as
input (faster, because this avoids downloading data each time running
module)

```sh
v.check.federal_state aoi=poly_HH federal_states=federal_states
```

## SEE ALSO

*[v.overlay](v.overlay.md)*

## AUTHORS

Lina Krisztian, [mundialis](https://www.mundialis.de/)
