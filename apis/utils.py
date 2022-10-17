def validate_dict_keys(required_keys: list[str], data: dict) -> set[str]:
    # 존재하지 않는 필수 키 set을 return
    return set(required_keys) - set(data.keys())
