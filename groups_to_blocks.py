### Command line version ###

import sys
import argparse

parser = argparse.ArgumentParser(description='Input for Cubit conversion script.')
# IMP naming could be better, '--' may denote optional
parser.add_argument("-g", "--geometry_path", type=str, help='Path to the Abaqus input file', required=True)
parser.add_argument("-p", "--cubit_path", help="Path to Cubit executable (required if PATH does not include Cubit)", required=False)
parser.add_argument("-o", "--output", help="Name/Location of the output file (Default is current/directory/exodus_out.exo)", required=False, nargs="exodus_out.exo")

# Should either add cubit to path beforehand or require input for the line below
# IMP Could add try/catch
# IMP could try to avoid importing sys

args = parser.parse_args()

# Makes sure cubit is importable
if args.cubit_path is not None:
    sys.path.append(str(args.cubit_path))

# Set up other input variables
geom_path = str(args.geometry_path)
output_path = str(args.geometry_path)
# This may not be necessary, TODO test whether export needs full path if it does os.cwd may be used
if output_path == "exodus_out.exo":
    pwd = True

### Cubit portion of the code ###
import cubit
cubit.init()
cubit.cmd("reset")

# Need to specify geom path for this command
cubit.cmd("import abaqus mesh geometry  \"{}\" feature_angle 135.00".format(geom_path))

entityIDList = cubit.get_entities("group")
cubit.cmd("merge vol all")
cubit.cmd("block 1 remove vol all")

# This overwrites the default "picked" group which is probably cleaner and also
# appends _<id> onto the end which avoids keywords
for i in range(2,len(entityIDList)):
    tempString = "block {} add group {}".format(i-1, i)
    cubit.cmd(tempString)
    tempName = cubit.get_entity_name("group", i)
    blockName = "\"" + tempName.split('.')[0] + "_{}\"".format(i-1)
    tempString = "block {} name {}".format(i-1,blockName)
    cubit.cmd(tempString)

cubit.cmd("export mesh \"{}\"  overwrite".format(output_path))
