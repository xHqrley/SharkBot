from definitions import SharkErrors

class Rarity():
    
    def __init__(self, name, colour, iconName, sellPrice):
        self.name = name
        self.colour = colour
        self.iconName = iconName
        self.sellPrice = sellPrice

common = Rarity("Common", 0x979c9f, "common_item", 5)
uncommon = Rarity("Uncommon", "uncommon_item", 0x2ecc71, 10)
rare = Rarity("Rare", 0x6fa8dc, "rare_item", 20)
legendary = Rarity("Legendary", 0x71368a, "legendary_item", 50)
exotic = Rarity("Exotic", 0xf1c40f, "exotic_item", 150)
mythic = Rarity("Mythic", 0xe74c3c, "mythic_item", 500)

rarities = [common, uncommon, rare, legendary, exotic, mythic]

def get(search):
    search = search.capitalize()
    for rarity in rarities:
        if rarity.name == search:
            return rarity
    raise SharkErrors.RarityNotFoundError(search)