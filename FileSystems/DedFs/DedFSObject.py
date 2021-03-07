class DedFSFileSys:
    BYTE_IN_SECTOR: int = 0
    SECTOR_IN_CLUSTER: int = 0
    MAGIC_NUMBER: str = ''
    COUNT_CLUSTER: int = 0


class DedFSFile:
    NAME_F: str = ''
    FILE_MOD: int = 0
    FIRST_CLUSTER: int = 0
    COUNT_CLUSTER: int = 0
    FILE_SIZE: int = 0
    DATE_CREATE: int = 0
