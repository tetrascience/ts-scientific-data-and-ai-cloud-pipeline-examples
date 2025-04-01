# R Exec Task Script <!-- omit in toc -->

## Version <!-- omit in toc -->

v0.1.0

## Table of Contents <!-- omit in toc -->

- [Summary](#summary)
- [Usage](#usage)
  - [R Packages](#r-packages)
- [Output](#output)
- [Changelog](#changelog)
  - [v0.1.0](#v010)

## Summary

Function to allow pipelines to run arbitrary R script.

## Usage

The R-exec task script allows an R script to be specified as a pipeline configuration parameter.
The contents of the file body that triggered the pipeline will be available to reference within the R
script in the `input_data` variable of the Global Environment. 

For example, if a .csv file triggered the pipeline, it can be referenced in the R script as follows:
```
byte_string <- rawToChar(input_data)
csv_data <- read.csv(textConnection(byte_string))
```

Note: Runtime performance has not been optimized for large input files (>10MB).

### R Packages

Some common packages are built into this task's image and are available for use.
They are:

| Package Name     | Version          |
| ---------------- | ---------------- |
| `askpass` | 1.2.1 |
| `backports` | 1.5.0 |
| `base` | 4.2.2 |
| `base64enc` | 0.1-3 |
| `bit` | 4.5.0.1 |
| `bit64` | 4.6.0-1 |
| `blob` | 1.2.4 |
| `boot` | 1.3-28.1 |
| `broom` | 1.0.7 |
| `bslib` | 0.8.0 |
| `cachem` | 1.1.0 |
| `callr` | 3.7.6 |
| `cellranger` | 1.1.0 |
| `class` | 7.3-21 |
| `cli` | 3.6.3 |
| `clipr` | 0.8.0 |
| `cluster` | 2.1.4 |
| `codetools` | 0.2-19 |
| `colorspace` | 2.1-1 |
| `compiler` | 4.2.2 |
| `conflicted` | 1.2.0 |
| `cpp11` | 0.5.1 |
| `crayon` | 1.5.3 |
| `data.table` | 1.16.4 |
| `datasets` | 4.2.2 |
| `DBI` | 1.2.3 |
| `dbplyr` | 2.5.0 |
| `digest` | 0.6.37 |
| `doParallel` | 1.0.17 |
| `dplyr` | 1.1.4 |
| `dtplyr` | 1.3.1 |
| `evaluate` | 1.0.3 |
| `fansi` | 1.0.6 |
| `farver` | 2.1.2 |
| `fastmap` | 1.2.0 |
| `fontawesome` | 0.5.3 |
| `forcats` | 1.0.0 |
| `foreach` | 1.5.2 |
| `foreign` | 0.8-84 |
| `fs` | 1.6.5 |
| `generics` | 0.1.3 |
| `ggplot2` | 3.5.1 |
| `glue` | 1.8.0 |
| `graphics` | 4.2.2 |
| `grDevices` | 4.2.2 |
| `grid` | 4.2.2 |
| `gtable` | 0.3.6 |
| `haven` | 2.5.4 |
| `highr` | 0.11 |
| `hms` | 1.1.3 |
| `htmltools` | 0.5.8.1 |
| `isoband` | 0.2.7 |
| `iterators` | 1.0.14 |
| `jquerylib` | 0.1.4 |
| `jsonlite` | 1.8.9 |
| `KernSmooth` | 2.23-20 |
| `knitr` | 1.49 |
| `labeling` | 0.4.3 |
| `lattice` | 0.20-45 |
| `lifecycle` | 1.0.4 |
| `lubridate` | 1.9.4 |
| `magrittr` | 2.0.3 |
| `MASS` | 7.3-58.2 |
| `Matrix` | 1.5-3 |
| `memoise` | 2.0.1 |
| `methods` | 4.2.2 |
| `mgcv` | 1.8-41 |
| `mime` | 0.12 |
| `modelr` | 0.1.11 |
| `munsell` | 0.5.1 |
| `nlme` | 3.1-162 |
| `nnet` | 7.3-18 |
| `parallel` | 4.2.2 |
| `pillar` | 1.10.1 |
| `pkgconfig` | 2.0.3 |
| `prettyunits` | 1.2.0 |
| `processx` | 3.8.5 |
| `progress` | 1.2.3 |
| `ps` | 1.8.1 |
| `purrr` | 1.0.2 |
| `R6` | 2.5.1 |
| `rappdirs` | 0.3.3 |
| `RColorBrewer` | 1.1-3 |
| `readr` | 2.1.5 |
| `readxl` | 1.4.3 |
| `rematch` | 2.0.0 |
| `reprex` | 2.1.1 |
| `rlang` | 1.1.5 |
| `rmarkdown` | 2.29 |
| `rpart` | 4.1.19 |
| `rstudioapi` | 0.17.1 |
| `sass` | 0.4.9 |
| `scales` | 1.3.0 |
| `spatial` | 7.3-16 |
| `splines` | 4.2.2 |
| `stats` | 4.2.2 |
| `stats4` | 4.2.2 |
| `stringi` | 1.8.4 |
| `stringr` | 1.5.1 |
| `survival` | 3.5-3 |
| `sys` | 3.4.3 |
| `tcltk` | 4.2.2 |
| `tibble` | 3.2.1 |
| `tictoc` | 1.2.1 |
| `tidyr` | 1.3.1 |
| `tidyselect` | 1.2.1 |
| `timechange` | 0.3.0 |
| `tinytex` | 0.54 |
| `tools` | 4.2.2 |
| `tzdb` | 0.4.0 |
| `utf8` | 1.2.4 |
| `utils` | 4.2.2 |
| `uuid` | 1.2-1 |
| `vctrs` | 0.6.5 |
| `viridisLite` | 0.4.2 |
| `vroom` | 1.6.5 |
| `withr` | 3.0.2 |
| `xfun` | 0.50 |
| `yaml` | 2.3.10 |
| `zoo` | 1.8-12 |

They can be imported in the normal way.
For example:

```
library(rlang)
```

## Output

The task outputs any contents of the data returned by the R script. The output of the R script must
have the following format:
```
return_list = list(file1_content, file2_content) # content objects (e.g., file1_content and file2_content)
names(return_list) = c("file1.png", "file2.png") # must be ByteVector
return(return_list)
```

## Changelog

### v0.1.0

- Initial version
