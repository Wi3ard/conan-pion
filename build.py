from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(args="--build missing")
    builder.add_common_builds(shared_option_name="pion:shared")
    builder.run()
