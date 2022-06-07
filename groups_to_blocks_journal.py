### JOURNAL VERSION TO RUN THROUGH CUBIT ### 

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

# cubit.cmd("export mesh \"{}/exportedMesh.exo\"  overwrite".format(os.getcwd()))
