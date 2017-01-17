from conans import ConanFile, CMake
from conans.tools import replace_in_file
import os
import shutil

class pionConan(ConanFile):
    name = "pion"
    version = "5.0.7-dev"
    url="https://github.com/splunk/pion"
    license="https://github.com/splunk/pion#license"
    generators = "cmake", "txt"
    settings = "os", "compiler", "build_type", "arch"
    requires = "Boost/1.60.0@lasote/stable", \
        "bzip2/1.0.6@lasote/stable", \
        "OpenSSL/1.0.2j@lasote/stable", \
        "zlib/1.2.9@lasote/stable";

    options = {"shared": [True, False],
               "enable_spdy": [True, False],
               "enable_tests": [True, False],
               "enable_piond": [True, False],
               "enable_helloserver": [True, False],
               "enable_allownothingservice": [True, False],
               "enable_cookieservice": [True, False],
               "enable_echoservice": [True, False],
               "enable_fileservice": [True, False],
               "enable_helloservice": [True, False],
               "enable_logservice": [True, False],
               "enable_log4cplus": [True, False],
               "enable_log4cxx": [True, False],
               "enable_log4cpp": [True, False],
               "enable_logging": [True, False]}
    default_options = "shared=False", \
        "enable_spdy=True", \
        "enable_tests=False", \
        "enable_piond=False", \
        "enable_helloserver=False", \
        "enable_allownothingservice=False", \
        "enable_cookieservice=False", \
        "enable_echoservice=False", \
        "enable_fileservice=False", \
        "enable_helloservice=False", \
        "enable_logservice=False", \
        "enable_log4cplus=False", \
        "enable_log4cxx=False", \
        "enable_log4cpp=False", \
        "enable_logging=False"

    def source(self):
        self.run("git clone --recursive https://github.com/splunk/pion.git")
        self.run("cd pion && git checkout develop")

    def build(self):
        conan_magic_lines = '''find_package(Threads REQUIRED)

# Conan.io config
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if(MSVC)
  add_definitions(-D_WIN32_WINNT=0x0501)

  if (CONAN_LINK_RUNTIME)
    set(flags
      CMAKE_C_FLAGS_DEBUG
      CMAKE_C_FLAGS_MINSIZEREL
      CMAKE_C_FLAGS_RELEASE
      CMAKE_C_FLAGS_RELWITHDEBINFO
      CMAKE_CXX_FLAGS_DEBUG
      CMAKE_CXX_FLAGS_MINSIZEREL
      CMAKE_CXX_FLAGS_RELEASE
      CMAKE_CXX_FLAGS_RELWITHDEBINFO)
    foreach(flag ${flags})
      if(${flag} MATCHES "/MD")
        string(REPLACE "/MDd " "${CONAN_LINK_RUNTIME} " ${flag} "${${flag}}")
        string(REPLACE "/MD " "${CONAN_LINK_RUNTIME} " ${flag} "${${flag}}")
      endif()
    endforeach()
  endif()
endif()
    '''
        replace_in_file("pion/CMakeLists.txt", "find_package(Threads REQUIRED)", conan_magic_lines)

        cmake = CMake(self.settings)

        cmake_options = []
        for option_name in self.options.values.fields:
            activated = getattr(self.options, option_name)
            the_option = "%s=" % option_name.upper()
            if option_name == "shared":
               the_option = "BUILD_SHARED_LIBS=ON" if activated else "BUILD_SHARED_LIBS=OFF"
            elif option_name == "enable_spdy":
               the_option = "BUILD_SPDY=ON" if activated else "BUILD_SPDY=OFF"
            elif option_name == "enable_tests":
               the_option = "BUILD_UT=ON" if activated else "BUILD_UT=OFF"
            elif option_name == "enable_piond":
               the_option = "BUILD_PIOND=ON" if activated else "BUILD_PIOND=OFF"
            elif option_name == "enable_helloserver":
               the_option = "BUILD_HELLOSERVER=ON" if activated else "BUILD_HELLOSERVER=OFF"
            elif option_name == "enable_allownothingservice":
               the_option = "BUILD_ALLOWNOTHINGSERVICE=ON" if activated else "BUILD_ALLOWNOTHINGSERVICE=OFF"
            elif option_name == "enable_cookieservice":
               the_option = "BUILD_COOKIESERVICE=ON" if activated else "BUILD_COOKIESERVICE=OFF"
            elif option_name == "enable_echoservice":
               the_option = "BUILD_ECHOSERVICE=ON" if activated else "BUILD_ECHOSERVICE=OFF"
            elif option_name == "enable_fileservice":
               the_option = "BUILD_FILESERVICE=ON" if activated else "BUILD_FILESERVICE=OFF"
            elif option_name == "enable_helloservice":
               the_option = "BUILD_HELLOSERVICE=ON" if activated else "BUILD_HELLOSERVICE=OFF"
            elif option_name == "enable_logservice":
               the_option = "BUILD_LOGSERVICE=ON" if activated else "BUILD_LOGSERVICE=OFF"
            elif option_name == "enable_log4cplus":
               the_option = "USE_LOG4CPLUS=ON" if activated else "USE_LOG4CPLUS=OFF"
            elif option_name == "enable_log4cxx":
               the_option = "USE_LOG4CXX=ON" if activated else "USE_LOG4CXX=OFF"
            elif option_name == "enable_log4cpp":
               the_option = "USE_LOG4CPP=ON" if activated else "USE_LOG4CPP=OFF"
            elif option_name == "enable_logging":
               the_option = "DISABLE_LOGGING=OFF" if activated else "DISABLE_LOGGING=ON"
            else:
               the_option += "ON" if activated else "OFF"
            cmake_options.append(the_option)

        cmake_cmd_options = " -D".join(cmake_options)

        cmake_conf_command = 'cmake %s/pion %s -DCMAKE_INSTALL_PREFIX:PATH=install -D%s' % (self.conanfile_directory, cmake.command_line, cmake_cmd_options)
        self.output.warn(cmake_conf_command)
        self.run(cmake_conf_command)

        self.run("cmake --build . --target install %s" % cmake.build_config)

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def package(self):
        self.copy("*.hpp", dst="include", src="install/include")
        self.copy("*.dll", dst="bin", src="install/bin")
        self.copy("*.lib", dst="lib", src="install/lib")
        self.copy("*.a", dst="lib", src="install/lib")
        self.copy("*.so*", dst="lib", src="install/lib")
        self.copy("*.dylib", dst="lib", src="install/lib")
        self.copy("*.*", dst="lib/cmake", src="install/lib/cmake")
        self.copy("*.*", dst="services", src="install/services")

    def package_info(self):
        self.cpp_info.libs = ["pion"]

        if not self.options.shared:
            self.cpp_info.cppflags = ["-DPION_STATIC_LINKING"]

#        if self.settings.compiler == "gcc" or self.settings.compiler == "apple-clang":
#            self.cpp_info.cppflags = ["-std=c++11"]
