from django.utils.translation import pgettext_lazy


class CategoryName:
    """The type that we expect to render the advert category as."""

    TANKS = "Tanks"
    HEALS = "Heals"
    DD = "DD"
    TRADERS = "Traders"
    GUILDMASTER = "Guildmaster"
    QUESTGIVER = "Questgiver"
    BLACKSMITH = "Blacksmith"
    LEATHERWORKER = "Leatherworker"
    POTION = "Potion Master"
    SPELLMASTER = "Spellmaster"

    CHOICES = [
        (TANKS, pgettext_lazy("Category name", "Tanks")),
        (HEALS, pgettext_lazy("Category name", "Heals")),
        (DD, pgettext_lazy("Category name", "DD")),
        (TRADERS, pgettext_lazy("Category name", "Traders")),
        (GUILDMASTER, pgettext_lazy("Category name", "Guildmaster")),
        (QUESTGIVER, pgettext_lazy("Category name", "Questgiver")),
        (BLACKSMITH, pgettext_lazy("Category name", "Blacksmith")),
        (LEATHERWORKER, pgettext_lazy("Category name", "Leatherworker")),
        (POTION, pgettext_lazy("Category name", "Potion Master")),
        (SPELLMASTER, pgettext_lazy("Category name", "Spellmaster")),
    ]