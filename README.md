[![Build status](https://ci.appveyor.com/api/projects/status/f98r7ox30217stun/branch/master?svg=true)](https://ci.appveyor.com/project/Wi3ard/conan-pion/branch/master)
[![Build Status](https://travis-ci.org/Wi3ard/conan-pion.svg?branch=master)](https://travis-ci.org/Wi3ard/conan-pion)

# conan-pion

[Conan.io](https://conan.io) package for [pion](https://github.com/splunk/pion) library

The packages generated with this **conanfile** can be found in [conan.io](https://www.conan.io/source/pion/5.0.7-dev/Wi3ard/stable).

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py

## Upload packages to server

    $ conan upload pion/5.0.7-dev@Wi3ard/stable --all

## Reuse the packages

### Basic setup

    $ conan install pion/5.0.7-dev@Wi3ard/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    pion/5.0.7-dev@Wi3ard/stable

    [options]
    pion:shared=True # False
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
