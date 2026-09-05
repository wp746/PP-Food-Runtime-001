import json

from pp_food_runtime.artifacts.store import ArtifactStore, sha256_file


def test_copy_image_records_hash_and_never_overwrites(tmp_path):
    source = tmp_path / "source.png"
    source.write_bytes(b"image-bytes")
    store = ArtifactStore(tmp_path / "artifacts")

    first = store.copy_image("job-1", "source", source)
    second = store.copy_image("job-1", "source", source)

    assert first.sha256 == sha256_file(source)
    assert first.path != second.path


def test_json_write_is_utf8_sorted_and_rejects_secret_fields(tmp_path):
    store = ArtifactStore(tmp_path / "artifacts")
    path = store.write_json("job-1", "facts", {"z": "椰椰西瓜冰", "a": 1})
    assert json.loads(path.read_text(encoding="utf-8")) == {"a": 1, "z": "椰椰西瓜冰"}
    assert path.read_text(encoding="utf-8").index('"a"') < path.read_text(encoding="utf-8").index('"z"')

    try:
        store.write_json("job-1", "unsafe", {"api_key": "must-not-persist"})
    except ValueError as exc:
        assert "secret" in str(exc).lower()
    else:
        raise AssertionError("secret-shaped fields must be rejected")
