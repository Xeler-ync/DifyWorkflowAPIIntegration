import enum
from typing import Union


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


def normalize_repo_type(input_type: Union[str, RepositoryType]) -> str:
    """
    将输入的字符串或枚举值统一转换为字符串

    Args:
        input_type: 可以是字符串或RepositoryType枚举值

    Returns:
        str: 转换后的字符串

    Raises:
        ValueError: 当输入既不是有效的字符串也不是有效的枚举值时
    """
    if isinstance(input_type, str):
        # 验证字符串是否是有效的枚举值
        try:
            RepositoryType(input_type)  # 这会抛出ValueError如果字符串无效
            return input_type
        except ValueError:
            raise ValueError(f"Invalid repository type string: {input_type}")

    elif isinstance(input_type, RepositoryType):
        return input_type.value

    else:
        raise ValueError(
            f"Input must be either string or RepositoryType enum, got {type(input_type)}"
        )
