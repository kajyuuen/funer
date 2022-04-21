from typing import List, Optional


def create_charid_to_tokenid(
    tokens: List[str],
    spaces: List[bool],
) -> List[Optional[int]]:
    assert len(tokens) == len(spaces)

    charid_to_tokenid = []

    for token_i, (token, space) in enumerate(zip(tokens, spaces)):
        charid_to_tokenid.extend([token_i] * len(token))
        if space:
            charid_to_tokenid.append(None)

    return charid_to_tokenid
