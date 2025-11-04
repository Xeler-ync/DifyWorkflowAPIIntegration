import enum


class RepositoryType(enum.Enum):
    ArchitectureAndDesignStyle = "ArchitectureAndDesignStyle"
    DiningAndEntertainmentFacilities = "DiningAndEntertainmentFacilities"
    HistoryAndBackgroundStory = "HistoryAndBackgroundStory"
    HotelOverviewAndCoreIdentity = "HotelOverviewAndCoreIdentity"
    RoomAndSuiteTypes = "RoomAndSuiteTypes"
    ServicesAndUniqueExperiences = "ServicesAndUniqueExperiences"
    TransportationAndLocation = "TransportationAndLocation"


# 从值获取枚举项
def get_enum_item_from_value(value):
    for item in RepositoryType:
        if item.value == value:
            return item
    return None
