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


class GemTypeChoices(models.TextChoices):
    APATITE = 'apatite', 'APATITE'
    WHITE_HOWLITE = 'white_howlite', 'WHITE HOWLITE'
    GREEN_AVENTURINE = 'green_aventurine', 'GREEN AVENTURINE'
    KYANITE = 'kyanite', 'KYANITE'
    CORUNDUM = 'corundum', 'CORUNDUM'
    PREHNITE = 'prehnite', 'PREHNITE'
    RHYOLITE = 'rhyolite', 'RHYOLITE'
    RED_JADEITE = 'red_jadeite', 'RED JADEITE'
    BLACK_TOURMALINE = 'black_tourmaline', 'BLACK TOURMALINE'
    STRAWBERRY_QUARTZ = 'strawberry_quartz', 'STRAWBERRY QUARTZ'
    JASPER = 'jasper', 'JASPER'
    AVENTURINE = 'aventurine', 'AVENTURINE'
    AMETHYST = 'amethyst', 'AMETHYST'
    AGATE = 'agate', 'AGATE'
    GARNET = 'garnet', 'GARNET'
    JADEITE = 'jadeite', 'JADEITE'
    CATS_EYE = 'cats_eye', 'CAT\'S EYE'
    MOONSTONE = 'moonstone', 'MOONSTONE'
    MALACHITE = 'malachite', 'MALACHITE'
    MOSS_AGATE = 'moss_agate', 'MOSS AGATE'
    ONYX = 'onyx', 'ONYX'
    PERIDOT = 'peridot', 'PERIDOT'
    ROSE_QUARTZ = 'rose_quartz', 'ROSE QUARTZ'
    SAPPHIRE = 'sapphire', 'SAPPHIRE'
    MOTHER_OF_PEARL = 'mother_of_pearl', 'MOTHER OF PEARL'
    TURQUOISE = 'turquoise', 'TURQUOISE'
    UNAKITE = 'unakite', 'UNAKITE'
    HEMATITE = 'hematite', 'HEMATITE'
    HOWLITE = 'howlite', 'HOWLITE'
    CHERRY_QUARTZ = 'cherry_quartz', 'CHERRY QUARTZ'


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


class JewelMetalChoices(models.TextChoices):
    MEDICAL_STEEL_316L = 'medical_steel_316l', 'MEDICAL_STEEL_316L'
    STAINLESS_STEEL = 'stainless_steel', 'STAINLESS_STEEL'
    SILVER = 'silver', 'SILVER'
    GOLD = 'gold', 'GOLD'
    PLATINUM = 'platinum', 'PLATINUM'

class JewelMaterialChoices(models.TextChoices):
    EPOXY = 'epoxy', 'EPOXY'
    WOOD = 'wood', 'WOOD'
    ENAMEL = 'enamel', 'ENAMEL'
    LEATHER = 'leather', 'LEATHER'
    GLASS_BEADS = 'glass_beads', 'GLASS_BEADS'
    JAPANESE_TOHO_BEADS = 'japanese_toho_beads', 'JAPANESE_TOHO_BEAD'
