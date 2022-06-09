### Command line version ###
import sys
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Input for Cubit conversion script.')
parser.add_argument("abaqus_file", type=Path, help='Path to the Abaqus input file')
parser.add_argument("-p", "--cubit_path", type=Path, help="Path to Cubit executable (required if PATH does not include Cubit)", required=False)
parser.add_argument("-o", "--output", type=Path, help="Name/Location of the output file (Default is current/directory/exodus_out.exo)", required=False, default="exodus_out.exo")
parser.add_argument("-f", "--force", action='store_true', default=False,
                    help="If present, overwrite a pre-existing output files.")

# Should either add cubit to path beforehand or require input for the line below
# IMP Could add try/catch
# IMP could try to avoid importing sys
args = parser.parse_args()

# Makes sure cubit is importable
if args.cubit_path is not None:
    sys.path.append(str(args.cubit_path))

# setup output command
output_path = str(args.output)

file_ext = str(args.output).split('.')[-1]

if file_ext == ".cub":
    output_cmd = 'save as "{}"'.format(output_path)
elif file_ext in ('e', 'exo'):
    output_cmd = 'export mesh "{}"'.format(output_path)
else:
    raise ValueError('Output extension "{}" not supported'.format(file_ext))

# check for pre-existing output file
if args.force:
    output_cmd += ' overwrite'
else:
    if Path(output_path).exists:
        msg = ('The output file "{}" already exists. Use "-f" '
              'to overwrite output files.'.format(output_path))
        raise RuntimeError(msg)

### Cubit portion of the code ###
import cubit

cubit.init([])
cubit.cmd("reset")

# Need to specify geom path for this command
cubit.cmd("import abaqus mesh geometry  \"{}\" feature_angle 135.00".format(args.abaqus_file))

cubit.cmd("merge vol all")
cubit.cmd("block 1 remove vol all")

# remove all pre-existing blocks
block_ids = cubit.get_entities("block")
for block in block_ids:
    cubit.cmd("delete block {}".format(block))

# This overwrites the default "picked" group which is probably cleaner and also
# appends _<id> onto the end which avoids keywords
split_key = '.SET-MATERIAL'

group_ids = cubit.get_entities("group")
for i, group in enumerate(group_ids):
    tempName = cubit.get_entity_name("group", group)
    # skip the picked group if present
    if tempName == 'picked':
        continue
    tempString = "block {} add group {}".format(i, group)
    cubit.cmd(tempString)
    blockName = "\"" + tempName.split(split_key)[0] + "_{}\"".format(i)
    tempString = "block {} name {}".format(i,blockName)
    cubit.cmd(tempString)

cubit.cmd(output_cmd)
