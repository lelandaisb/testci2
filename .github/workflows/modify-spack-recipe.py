import re
import sys
import requests
import hashlib
import os

# Modify spack recipe of the project if it exists.
# Used in CI to check if release number and cmake version are identical.
def modifySpackRecipe(recipe_path, project_name, project_version):
    try:
        readable_hash = str(sha256sum(project_name, project_version))
        print("Sha256 :", readable_hash)
        with open(recipe_path, 'r+') as fd:
            contents = fd.readlines()
            for index, line in enumerate(contents):
                # match the exact version number, i.e. version already in recipe ?
                res = re.search("^(\s*)version\(\'" + project_version + "\'", line)
                if res:
                    # just replace the sha
                    print("Version", project_version, "already in recipe, replacing sha256")
                    newline = re.sub("sha256=\'.*\'", "sha256=\'" + readable_hash + "\'", line)
                    contents[index] = newline
                    print(newline)
                    break
                else:
                    # add the version to package.py
                    res = re.search("^(\s*)version\(\'[0-9]+", line)
                    if res:
                        print("Adding version", project_version, "to Spack recipe")
                        newline = res.group(1) + "version('" + project_version + "', sha256='" + readable_hash + "')\n"
                        contents.insert(index, newline)
                        print(newline)
                        break

            fd.seek(0)
            fd.writelines(contents)
        return 0

    except Exception as e:
        print("** Error in trying to change recipe of project: " + recipe_path)
        print(e)
        return -1

def sha256sum(project_name, project_version):
    url = 'https://github.com/LIHPC-Computational-Geometry/' + project_name + '/archive/refs/tags/' + project_version + '.tar.gz'

    print("Downloading", url)
    tarball = requests.get(url, allow_redirects=True)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_name = "/tmp/" + project_name + "-" + project_version + ".tar.gz"
        with open(file_name, 'wb') as f:
            f.write(response.raw.read())
            print('File created:', file_name)
    else:
        raise Exception("Can not download: " + url)
    
    print("Computing sha256")
    readable_hash = -1
    with open(file_name,"rb") as f:
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest()

    return readable_hash

if __name__ == "__main__":
    recipe_path = sys.argv[1]
    project_name = sys.argv[2]
    project_version = sys.argv[3]
    sys.exit(modifySpackRecipe(recipe_path, project_name, project_version))
