from DedFs.OtherItem import ByteStrValidator, IntValidator


class DedFSFileSys:
    MBR: bytes = ByteStrValidator(512)


class DedFSFile:
    NAME_F: str = ByteStrValidator(32)
    FILE_MOD: int = IntValidator(0, 255)
    FIRST_CLUSTER: int = IntValidator(0, 65535)
    COUNT_CLUSTER: int = IntValidator(0, 255)
    FILE_SIZE: int = IntValidator(0, 4294967295)
    DATE_CREATE: int = IntValidator(0, 4294967295)
