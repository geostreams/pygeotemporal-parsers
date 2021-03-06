# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased

### Changed
- Made Hourly-Related print statements dependent upon an optional flag
  [IMLCZO-273](https://opensource.ncsa.illinois.edu/jira/browse/IMLCZO-273)

### Fixed
- Add missing variable import in `create_header` function in `contact_files.py`
  [IMLCZO-272](https://opensource.ncsa.illinois.edu/jira/browse/IMLCZO-267)

## [1.0.0] - 2019-05-24

### Added
- Great Lakes Environmental Database(Glenda) parser
  [GLM-110](https://opensource.ncsa.illinois.edu/jira/browse/GLM-110)
- Great Lakes Fish Monitoring and Surveillance Program Parser
  [GLM-112](https://opensource.ncsa.illinois.edu/jira/browse/GLM-112)
- Great Lakes Monitoring/ Great Lakes to the Gulf USGS Parser
  [GLM-77](https://opensource.ncsa.illinois.edu/jira/browse/GLM-77)
- IMLCZO general workflow scripts
  [IMLCZO-217](https://opensource.ncsa.illinois.edu/jira/browse/IMLCZO-217)
- Added IMLCZO Mahomet Ingestion style of script
  [IMLCZO-228](https://opensource.ncsa.illinois.edu/jira/browse/IMLCZO-228)
- Added Combination Script for get-concat-parse-upload
  [IMLCZO-233](https://opensource.ncsa.illinois.edu/jira/browse/IMLCZO-233)
- Added Combination Script for get-convert-concat-parse-upload
  [IMLCZO-236](https://opensource.ncsa.illinois.edu/jira/browse/IMLCZO-236)
- Convert a provided JSON Data file to a CSV File
  [IMLCZO-263](https://opensource.ncsa.illinois.edu/jira/browse/IMLCZO-263)
- Add Scripts for Hourly Parsing of Datapoints
  [IMLCZO-267](https://opensource.ncsa.illinois.edu/jira/browse/IMLCZO-267)
- Add updated parsers for USGS, IWQIS, and GREON
  [GLGVO-671](https://opensource.ncsa.illinois.edu/jira/browse/GLGVO-671)  

### Removed
- Removed huc_finder and dependencies
  [GEOD-1105](https://opensource.ncsa.illinois.edu/jira/browse/GEOD-1105)
