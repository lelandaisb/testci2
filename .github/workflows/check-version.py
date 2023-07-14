import re
import sys
import os

# If it exists a file 'source_path/cmake/version.cmake', 
# check if the cmake version is equal to the expected argument.
# Used in CI to check if release number and cmake version are identical.
#
# Return false if release number and cmake version are different
# true otherwise (if equal or if file does not exist, not a cmake project).
def checkVersion(source_path, expected):
    actual = getCmakeVersion(source_path)
    if (actual == ''):
        print('No file named cmake/version.cmake')
    else:
        print('Expected version', expected, ', actual', actual)
        if (actual != expected):
            return -1
    return 0

def getCmakeVersion(project_path):
    path = project_path + '/cmake/version.cmake'
    version = ''
    if (os.path.exists(path)):
        with open(path) as f:
            line = ' '.join(f.readlines())
            major = re.search("_MAJOR_VERSION \"([0-9]+)\"", line)
            minor = re.search("_MINOR_VERSION \"([0-9]+)\"", line)
            release = re.search("_RELEASE_VERSION \"([0-9]+)\"", line)
            version = major.group(1) + "." + minor.group(1) + "." + release.group(1)
    return version


if __name__ == "__main__":
    project_path = sys.argv[1]
    expected_version = sys.argv[2]
    sys.exit(checkVersion(project_path, expected_version))
