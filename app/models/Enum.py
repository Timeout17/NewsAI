from enum import Enum

class Language(str, Enum):
    HUNGARIAN = "Hungarian"
    GERMAN = "German"
    ENHLISH = "English"


class Category(str, Enum):
    GENERAL = "General"
    WORLD = "World"
    NATION = "Nation"
    BUSINESS = "Business"
    TECHNOLOGY = "Technology"
    ENTErRTAINMENT = "Entertainment"
    SPORTS = "Sports"
    SCIENCE = "Science"
    HEALTH = "Health"