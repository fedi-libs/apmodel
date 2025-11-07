from datetime import datetime
from typing import Any, Dict, List, Literal, TypedDict, Union
from urllib.parse import urlparse, urlunparse
from zoneinfo import ZoneInfo

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, rsa
from multiformats import multibase, multicodec
from pydantic_core import PydanticCustomError

from apmodel.context import LDContext
from apmodel.exceptions import InvalidField


class GeneratedAliasesParams(TypedDict):
    validation_alias: str
    serialization_alias: str


def to_jld(arr_str: bool = False, any_uri: bool = False):
    def func(v: Any):
        if arr_str:
            return [v]
        if isinstance(v, datetime):
            iso_string_with_Z = v.isoformat().replace("+00:00", "Z")
            return [
                {
                    "@type": "https://www.w3.org/2001/XMLSchema#dateTime",
                    "@value": iso_string_with_Z,
                }
            ]
        elif isinstance(v, bool):
            return [
                {
                    "@type": "https://www.w3.org/2001/XMLSchema#boolean",
                    "@value": v,
                }
            ]
        elif isinstance(v, float):
            return [
                {
                    "@type": "https://www.w3.org/2001/XMLSchema#float",
                    "@value": v,
                }
            ]
        elif isinstance(
            v,
            (
                rsa.RSAPublicKey,
                ed25519.Ed25519PublicKey,
                rsa.RSAPrivateKey,
                ed25519.Ed25519PrivateKey,
            ),
        ):
            return [
                {
                    "@type": "https://w3id.org/security#multibase",
                    "@value": ser_multibase(v),
                }
            ]
        else:
            if any_uri:
                return [
                    {
                        "@type": "https://www.w3.org/2001/XMLSchema#anyURI",
                        "@value": v,
                    }
                ]
            return [{"@value": v}]

    return func


def generate_context_from_expanded(expanded_json_ld):
    context_map = {}
    uris_to_process = set()

    # 1. すべてのURIを収集
    for item in expanded_json_ld:
        # プロパティのURI
        for key in item.keys():
            if key not in ("@id", "@type", "@context"):
                # キー自体がURI
                uris_to_process.add(key)
                
                # 値がオブジェクトで、@idを持っている場合（参照URI）
                if isinstance(item[key], list):
                    for sub_item in item[key]:
                        if isinstance(sub_item, dict) and "@id" in sub_item:
                            uris_to_process.add(sub_item["@id"])

        # @type のURI
        if "@type" in item:
            for type_uri in item["@type"]:
                if "://" in type_uri: # 完全なURIのみを対象
                    uris_to_process.add(type_uri)

        # @id のURI
        if "@id" in item:
            if "://" in item["@id"]:
                uris_to_process.add(item["@id"])


    # 2. URIを解析し、ネームスペースでグループ化
    # { namespace_base: { local_name: full_uri, ... }, ... }
    namespace_groups = {}
    
    # { full_uri: term, ... } - @idのように、ネームスペース化できないURI用
    simple_terms = {}

    for uri in uris_to_process:
        parsed_uri = urlparse(uri)
        
        # フラグメント (例: #term) を持つURI
        if parsed_uri.fragment:
            namespace_base = urlunparse(parsed_uri._replace(fragment=""))
            local_name = parsed_uri.fragment
            
            # https://www.w3.org/ns/activitystreams# のように末尾が # の場合は、# を除いたものをベースとする
            if namespace_base.endswith('#'):
                namespace_base = namespace_base[:-1]
            
            # 例: namespace_base="https://www.w3.org/ns/activitystreams", local_name="Object"
            
            if namespace_base:
                if namespace_base not in namespace_groups:
                    namespace_groups[namespace_base] = {}
                namespace_groups[namespace_base][local_name] = uri
                continue
        
        # パスセグメント (例: /term) を持つURI
        elif parsed_uri.path:
            path_segments = parsed_uri.path.rstrip("/").split("/")
            local_name = path_segments[-1]
            
            # 例: http://schema.org/name の場合
            # namespace_base="http://schema.org/"
            # local_name="name"
            if len(path_segments) > 1:
                namespace_base_parts = parsed_uri.path[:-len(local_name)]
                namespace_base = urlunparse(parsed_uri._replace(path=namespace_base_parts, params="", query="", fragment=""))
                
                if namespace_base:
                    if namespace_base not in namespace_groups:
                        namespace_groups[namespace_base] = {}
                    namespace_groups[namespace_base][local_name] = uri
                    continue

        # ネームスペース化に適さないURI (例: ドメイン全体が@idになる場合など)
        term = uri.split('/')[-1].split('#')[-1] or uri # 最後のパス/フラグメントを試みる
        simple_terms[uri] = term # タームは短縮されない
        
    
    # 3. 統合された @context を構築
    
    # プレフィックスの生成とタームの定義
    prefix_counter = 1
    used_terms = set()
    
    # Activity Streamsの例に対応するため、ネームスペースでループ
    for base_uri, local_names in namespace_groups.items():
        
        # プレフィックス名の候補
        prefix_candidate = base_uri.split('/')[-1].split('#')[0].split('.')[-1].lower() or f"p{prefix_counter}"
        
        # プレフィックスが既存のタームと競合するかチェック
        prefix_term = prefix_candidate
        conflict_count = 0
        while prefix_term in used_terms:
            conflict_count += 1
            prefix_term = f"{prefix_candidate}{conflict_count}"
            
        used_terms.add(prefix_term)

        # プレフィックスの定義 (末尾に # または / をつける)
        # ネームスペースに # が含まれていれば # を、そうでなければ / をつけるのが一般的
        if base_uri.endswith('#'):
            prefix_definition = f"{base_uri}"
        elif base_uri.endswith('/'):
            prefix_definition = f"{base_uri}"
        else:
            # プレフィックスとして使うため、末尾に適切な区切り文字を追加
            if '#' in base_uri: # #ベースの場合は # をつける
                prefix_definition = f"{base_uri}#"
            else: # /ベースの場合は / をつける
                prefix_definition = f"{base_uri}/"


        context_map[prefix_term] = prefix_definition
        
        # ローカル名（ターム）の定義
        for local_name, full_uri in local_names.items():
            # URIがプレフィックス定義で完全に短縮できることを確認
            if full_uri.startswith(prefix_definition):
                # 完全に短縮できる場合は定義をスキップ (例: "as:Object" の形式になる)
                pass 
            else:
                # 短縮できない、またはプレフィックスと完全に一致しないURIは個別定義
                # このケースは非常に稀だが、安全のために残す
                term_name = local_name
                if term_name in used_terms: # プレフィックス名とローカル名が競合する場合
                    term_name = f"{prefix_term}_{local_name}"
                
                context_map[term_name] = full_uri
                used_terms.add(term_name)

        prefix_counter += 1


    # 4. ネームスペース化できなかったURIの処理
    for uri, term in simple_terms.items():
        if term in used_terms:
            term = f"item_{term}"

        context_map[term] = uri
        used_terms.add(term)


    context = {"@context": context_map}

    return context


def generate_aliases(
    suffix: str,
    schema: Literal[
        "as2", "schemaorg", "mastodon", "misskey", "security", "ldp"
    ] = "as2",
) -> GeneratedAliasesParams:
    """Generate arguments from schema name and suffix.

    Args:
        suffix (str): suffix
        schema (Literal["as2", "schemaorg", "mastodon", "misskey"]): The schema to which the suffix belongs

    Returns:
        dict: A dictionary containing arguments compatible with pydantic.
    """

    if schema == "as2":
        field_alias = f"https://www.w3.org/ns/activitystreams#{suffix}"
    elif schema == "misskey":
        field_alias = f"https://misskey-hub.net/ns#{suffix}"
    elif schema == "mastodon":
        field_alias = f"http://joinmastodon.org/ns#{suffix}"
    elif schema == "schemaorg":
        field_alias = f"http://schema.org#{suffix}"
    elif schema == "security":
        field_alias = f"https://w3id.org/security#{suffix}"
    elif schema == "ldp":
        field_alias = f"https://www.w3.org/ns/ldp#{suffix}"

    return GeneratedAliasesParams(
        validation_alias=field_alias, serialization_alias=field_alias
    )


def has_match(data: Dict[str, Any], expected_keys: List[str]) -> bool:
    """
    Checks if all expected keys are present in the data dictionary.
    """
    return set(expected_keys).issubset(data.keys())


def get_value_from_array(v: Any) -> Any:
    """
    Pydantic validator to extract a single value from a JSON-LD property.
    It handles both single values and arrays. For arrays, it iterates
    and returns the first suitable value found.
    """
    if isinstance(v, list):
        for item in v:
            if isinstance(item, dict):
                if "@value" in item:
                    value = item["@value"]
                    value_type = item.get("@type")

                    if (
                        value_type
                        == "https://www.w3.org/2001/XMLSchema#dateTime"
                    ):
                        if isinstance(value, str):
                            dt_str = value
                            if dt_str.endswith("Z"):
                                dt_str = dt_str[:-1]
                            dt = datetime.fromisoformat(dt_str)
                            if dt.tzinfo is None:
                                dt = dt.replace(tzinfo=ZoneInfo("UTC"))
                            return dt
                    elif value_type == "https://w3id.org/security#multibase":
                        decoded = multibase.decode(value)
                        codec, data = multicodec.unwrap(decoded)
                        if codec.name == "ed25519-pub":
                            try:
                                pub_key = (
                                    ed25519.Ed25519PublicKey.from_public_bytes(
                                        data
                                    )
                                )
                                if isinstance(
                                    pub_key, ed25519.Ed25519PublicKey
                                ):
                                    return pub_key
                                else:
                                    raise ValueError(
                                        "Unsupported Key: {}".format(
                                            type(pub_key)
                                        )
                                    )
                            except InvalidKey:
                                raise InvalidField(
                                    "Invalid ed25519 public key passed."
                                )
                        elif codec.name == "rsa-pub":
                            try:
                                pub_key = serialization.load_der_public_key(
                                    data
                                )
                                if isinstance(pub_key, rsa.RSAPublicKey):
                                    return pub_key
                                else:
                                    raise ValueError(
                                        "Unsupported Key: {}".format(
                                            type(pub_key)
                                        )
                                    )
                            except ValueError:
                                raise InvalidField(
                                    "Invalid rsa public key passed."
                                )
                        elif codec.name == "ed25519-priv":
                            try:
                                priv_key = ed25519.Ed25519PrivateKey.from_private_bytes(
                                    data
                                )
                                if isinstance(
                                    priv_key, ed25519.Ed25519PrivateKey
                                ):
                                    return priv_key
                                else:
                                    raise ValueError(
                                        "Unsupported Key: {}".format(
                                            type(priv_key)
                                        )
                                    )
                            except InvalidKey:
                                raise InvalidField(
                                    "Invalid ed25519 private key passed."
                                )
                        elif codec.name == "rsa-priv":
                            try:
                                priv_key = serialization.load_der_private_key(
                                    data, password=None
                                )
                                if isinstance(priv_key, rsa.RSAPrivateKey):
                                    return priv_key
                                else:
                                    raise ValueError(
                                        "Unsupported Key: {}".format(
                                            type(priv_key)
                                        )
                                    )
                            except ValueError:
                                raise InvalidField(
                                    "Invalid rsa private key passed."
                                )
                        else:
                            raise ValueError(
                                "Unsupported Codec: {}".format(codec.name)
                            )
                    return value
                elif "@id" in item:
                    value = item["@id"]
                    return value
            else:
                return item
    return v


def parse_ld_context(v: List) -> LDContext:
    if not isinstance(v, list) and not isinstance(v, str):
        raise PydanticCustomError(
            "invalid_type",
            "Input must be a list to be converted to LDContexts, got {input_type}",
            {"input_type": type(v).__name__},
        )

    return LDContext(v)


def load_pem_key(
    v: Union[
        str,
        rsa.RSAPublicKey,
        rsa.RSAPrivateKey,
        ed25519.Ed25519PrivateKey,
        ed25519.Ed25519PublicKey,
    ],
    private: bool = False,
) -> Union[
    rsa.RSAPublicKey,
    rsa.RSAPrivateKey,
    ed25519.Ed25519PrivateKey,
    ed25519.Ed25519PublicKey,
]:
    if not isinstance(v, str):
        return v
    if private:
        key = serialization.load_pem_private_key(
            v.encode("utf-8"), password=None
        )
        if not isinstance(key, (rsa.RSAPrivateKey, ed25519.Ed25519PrivateKey)):
            raise InvalidField("Unsupported private key passed.")
        return key
    else:
        key = serialization.load_pem_public_key(v.encode("utf-8"))
        if not isinstance(key, (rsa.RSAPublicKey, ed25519.Ed25519PublicKey)):
            raise InvalidField("Unsupported public key passed.")
        return key


def ser_multibase(
    v: Union[
        rsa.RSAPublicKey,
        ed25519.Ed25519PublicKey,
        rsa.RSAPrivateKey,
        ed25519.Ed25519PrivateKey,
    ],
) -> str:
    if isinstance(v, rsa.RSAPrivateKey):
        wrapped = multicodec.wrap(
            "rsa-priv",
            v.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            ),
        )
    elif isinstance(v, ed25519.Ed25519PrivateKey):
        wrapped = multicodec.wrap(
            "ed25519-priv",
            v.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption(),
            ),
        )
    elif isinstance(v, rsa.RSAPublicKey):
        wrapped = multicodec.wrap(
            "rsa-pub",
            v.public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.PKCS1,
            ),
        )
    elif isinstance(v, ed25519.Ed25519PublicKey):
        wrapped = multicodec.wrap(
            "ed25519-pub",
            v.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw,
            ),
        )
    return multibase.encode(wrapped, "base58btc")


def ser_public_key_pem(
    v: Union[rsa.RSAPublicKey, ed25519.Ed25519PublicKey],
) -> str:
    if isinstance(v, rsa.RSAPublicKey):
        return v.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")
    elif isinstance(v, ed25519.Ed25519PublicKey):
        return v.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")
