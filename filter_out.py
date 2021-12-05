from io import BytesIO

import numpy as np

import hard_filter
from database import World

for world in World.select().where(World.biome_data.is_null(False)):
    arr = np.load(BytesIO(world.biome_data))
    if hard_filter.should_filter(arr):
        world.delete_instance()
