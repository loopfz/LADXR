import patches.enemies
import patches.dungeonEntrances
import patches.startLocation


class WorldSetup:
    def __init__(self):
        self.start_house_index = 0
        self.dungeon_entrance_mapping = list(range(9))
        self.boss_mapping = list(range(9))
        self.miniboss_mapping = {
            # Main minibosses
            0: "ROLLING_BONES", 1: "HINOX", 2: "DODONGO", 3: "CUE_BALL", 4: "GHOMA", 5: "SMASHER", 6: "GRIM_CREEPER", 7: "BLAINO",
            # Color dungeon needs to be special, as always.
            "c1": "AVALAUNCH", "c2": "GIANT_BUZZ_BLOB",
            # Overworld
            "moblin_cave": "MOBLIN_KING",
        }

    def randomize(self, options, rnd):
        if options.randomstartlocation:
            self.start_house_index = rnd.randint(0, 7)
        if options.dungeonshuffle:
            rnd.shuffle(self.dungeon_entrance_mapping)
        if options.bossshuffle:
            if options.heartcontainers:
                # Color dungeon boss does not drop a heart container so we cannot shuffle him when we
                # have heart container shuffling
                self.boss_mapping = list(range(8))
            rnd.shuffle(self.boss_mapping)
            if options.heartcontainers:
                self.boss_mapping += [8]
        if options.miniboss != "default":
            values = [name for name in self.miniboss_mapping.values()]
            for key in self.miniboss_mapping.keys():
                self.miniboss_mapping[key] = rnd.choice(values)
                if options.miniboss == 'shuffle':
                    values.remove(self.miniboss_mapping[key])

    def loadFromRom(self, rom):
        self.start_house_index = patches.startLocation.readStartLocation(rom)
        self.dungeon_entrance_mapping = patches.dungeonEntrances.readEntrances(rom)
        self.boss_mapping = patches.enemies.readBossMapping(rom)
        self.miniboss_mapping = patches.enemies.readMiniBossMapping(rom)
