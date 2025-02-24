import os.path as path

import jpype.imports
# import java.nio.file as file
jpype.startJVM(classpath=[path.join("assets", 'amidst-v4-5-beta3.jar')])
mc = jpype.JPackage("amidst")
inst = mc.mojangapi.file.MinecraftInstallation.newLocalMinecraftInstallation()
versions = list(inst.readInstalledVersionsAsLauncherProfiles())
# TODO add cli version support
prof = next(filter(lambda version: version.getVersionId() == '1.15.2', versions))
mc_interface = mc.mojangapi.minecraftinterface.MinecraftInterfaces.fromLocalProfile(prof)
builder = mc.mojangapi.world.WorldBuilder.createSilentPlayerless()


import numpy as np
import database
from itertools import count
from io import BytesIO
import hard_filter

width = 1400
height = 650

for i in count():
    seed = mc.mojangapi.world.WorldSeed.random()
    world_type = mc.mojangapi.world.WorldType.DEFAULT
    gen_opts = ""
    opts = mc.mojangapi.world.WorldOptions(seed, world_type, gen_opts)
    world = builder.from_(mc_interface, opts)
    biome_oracle = world.getBiomeDataOracle()
    
    
    def biome_val(x, y):
        return np.uint8(int(biome_oracle.getBiomeAt(x, y, True).getId()))
    
    
    biome_data = np.fromfunction(np.vectorize(biome_val), (width, height), dtype=np.int64)
    
    if not hard_filter.should_filter(biome_data):
        bin_data = None
        with BytesIO() as tmp_file:
            np.save(tmp_file, biome_data)
            bin_data = tmp_file.getvalue()
        world = database.World.create(seed=seed.getLong(), biome_data=bin_data)
    
    print(i, seed.getLong())
