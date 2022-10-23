# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).
The format is based on [Keep a Changelog](http://keepachangelog.com/)

## [Unreleased]
- Added this changelog

## [1.1.0] - 2022-10-11

The main thrust of this version was to refactor the monolithic `HexDumper`
code into an abstract base class `Dumper` with three subclasses corresponding
to their output type:
- `HexDumper` - for the normal hex dump
- `CDumper` - for the C include style dump
- `PostscriptDumper` - for Postscript output (plain hex strings)

This was very useful because there are many command line options
and the three output types were all woven into one method.

### Added
- Added new context manager `SaveDirectory` so that unit tests can `cwd`
- Updated subprocess calls to use `check=True, text=True`

### Changed
- Refactored common code in unit tests into `runxxd` method
- Refactored `HexDumper` into base class and three subclasses for different output types

### Bug fixes
- Issue #27: Reverse use on -ps file causes error
- Issue #36: -b option is not working 

## [1.0.0] - 2022-09-24

Initial development of `pxxd`.  This is a port of the `xxd` utility that ships
with [vim](https://www.vim.org/), developed by Juergen Weigert in 1990.  I converted
the C code to Python at a functional level and added 77 unit tests.

[Unreleased]: https://github.com/philhanna/xxd/compare/1.1.0..HEAD
[1.1.0]: https://github.com/philhanna/xxd/compare/1.0.0..1.1.0
[1.0.0]: https://github.com/philhanna/xxd/compare/2cc47..1.1.0
