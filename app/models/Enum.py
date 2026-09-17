from enum import Enum

class Language(str, Enum):
    HUNGARIAN = "Hungarian"
    GERMAN = "German"
    ENHLISH = "English"


class Category(str, Enum):
    LAW = "Law"
    ECONOMY = "Economy"
    WAR = "War"

