import re
import sys

def modifySpackRecipe(recipe_path, version, sha256):
    try:
        with open(recipe_path, 'r+') as fd:
            contents = fd.readlines()
            for index, line in enumerate(contents):
                res = re.search("^(\s*)version\(\'[0-9]+", line)
                if res:
                    print("Match line", index, ":", line, "--", res.group(1), "--")
                    contents.insert(index, res.group(1) + "version('" + version + "', sha256='" + sha256 + "')\n")
                    break

            fd.seek(0)
            fd.writelines(contents)
        return 0
    except Exception as e:
        print("** Error in changing recipe: " + recipe_path)
        print(e)
        return -1

if __name__ == "__main__":
    recipe_path = sys.argv[1]
    version = sys.argv[2]
    sha256 = sys.argv[3]
    sys.exit(modifySpackRecipe(recipe_path, version, sha256))
