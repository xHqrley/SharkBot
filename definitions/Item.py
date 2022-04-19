from definitions import Rarity, Collection, SharkErrors

class Item():
    
    def __init__(self, itemData):
        self.id, self.name, self.description = itemData[0:3]
        self.rarity = Rarity.get(itemData[3])
        try:
            self.imageUrl = itemData[4]
        except IndexError:
            self.imageUrl = None

    def generate_embed(self):
        embed = discord.Embed()
        embed.title = self.name
        embed.color = self.rarity.colour
        embed.description = self.description
        embed.set_footer(text = f"{self.rarity.name} | {self.id}")
        if self.imageUrl != None:
            embed.set_thumbnail(url=self.imageUrl)

        return embed

items = []

def get(search):
    search = search.upper()
    for item in items:
        if item.id == search:
            return item
    raise SharkErrors.ItemNotFoundError(search)

def search(search):
    search = search.lower()
    for item in items:
        if search == item.name.lower() or search == item.id.lower():
            return item
    raise SharkErrors.ItemNotFoundError(search)