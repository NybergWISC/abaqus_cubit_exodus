### Command line version ###
import os

def convert_groups_to_blocks(input_file, output_file, overwrite=False):
    ### Cubit portion of the code ###
    import cubit

    cubit.init([])
    cubit.cmd("reset")

    if not overwrite and os.path.exists(output_file):
        msg = ('The output file "{}" already exists. Use "-f" '
                'to overwrite output files.'.format(output_file))
        raise RuntimeError(msg)

    # setup output patha n
    file_ext = str(output_file).split('.')[-1]

    if file_ext == ".cub":
        output_cmd = 'save as "{}"'.format(output_file)
    elif file_ext in ('e', 'exo'):
        output_cmd = 'export mesh "{}"'.format(output_file)
    else:
        raise ValueError('Output extension "{}" not supported'.format(file_ext))

    if overwrite:
        output_cmd += ' overwrite'

    # Need to specify geom path for this command
    cubit.cmd("import abaqus mesh geometry  \"{}\" feature_angle 135.00".format(input_file))

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
        group_name = cubit.get_entity_name("group", group)
        # skip the picked group if present
        if group_name == 'picked':
            continue
        # add group to block
        block_cmd = "block {} add group {}".format(i, group)
        cubit.cmd(block_cmd)
        # set the block name
        block_name = "\"" + group_name.split(split_key)[0]
        block_cmd = "block {} name {}".format(i, block_name)
        cubit.cmd(block_cmd)

    cubit.cmd(output_cmd)
