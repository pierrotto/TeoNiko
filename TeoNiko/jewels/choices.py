from django.db import models


class JewelCategoryChoices(models.TextChoices):

    EARRINGS = "earrings", "EARRINGS"
    BRACELET = "bracelet", "BRACELET"
    RING = "ring", "RING"
    NECKLACE = "necklace", "NECKLACE"
    PENDANT = "pendant", "PENDANT"
    CHAIN = "chain", "CHAIN"
    TROUSERS_CHAIN = "trousers_chain", "TROUSERS_CHAIN"
    BODY_CHAIN = "body_chain", "BODY_CHAIN"
    EYEGLASS_CORD = "eyeglass", "EYEGLASS_CORD"
    ANKLET = "anklet", "ANKLET"
    BEADED_NECKLACE = "beaded_necklace", "BEADED_NECKLACE"
    BELT = "belt", "BELT"
    HAIRPIN = "heart_pin", "HAIRPIN"
    KEYCHAIN = "keychain", "KEYCHAIN"
    BROOCH = "brooch", "BROOCH"
    BOOKMARK = "bookmark", "BOOKMARK"
    OTHER = "other", "OTHER"


class GemShapeChoices(models.TextChoices):
    SQUARE = 'square', 'SQUARE'
    RECTANGLE = 'rectangle', 'RECTANGLE'
    CIRCLE = 'circle', 'CIRCLE'
    OVAL = 'oval', 'OVAL'
    OTHER = 'other', 'OTHER'


class GemColorChoices(models.TextChoices):
    GREEN = 'green', 'GREEN'
    DARK_GREEN = 'dark green', 'DARK GREEN'
    LIGHT_GREEN = 'light green', 'LIGHT GREEN'
    RED = 'red', 'RED'
    DARK_RED = 'dark red', 'DARK RED'
    CHERRY = 'cherry', 'CHERRY'
    WHITE = 'white', 'WHITE'
    GRAY = 'gray', 'GRAY'
    GRAPHITE_GRAY = 'graphite_gray', 'GRAPHITE_GRAY'
    YELLOW = 'yellow', 'YELLOW'
    GOLDEN = 'golden', 'GOLDEN'
    COFFEE = 'coffee', 'COFFEE'
    BROWN = 'brown', 'BROWN'
    BLACK = 'black', 'BLACK'
    LIGHT_BROWN = 'light_brown', 'LIGHT_BROWN'
    PURPLE = 'purple', 'PURPLE'
    MULTICOLOR = 'multicolor', 'MULTICOLOR'
    ORANGE = 'orange', 'ORANGE'
    ROSE = 'rose', 'ROSE'
    BLUE = 'blue', 'BLUE'
    LIGHT_BLUE = 'light_blue', 'LIGHT_BLUE'
    DARK_BLUE = 'dark_blue', 'DARK_BLUE'
    STEEL_SILVER = 'steel_silver', 'STEEL_SILVER'
    OTHER = 'other', 'OTHER'

