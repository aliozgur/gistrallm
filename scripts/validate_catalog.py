import json
import os
import re

CATALOG_PATH = "manifests/catalog.json"

REQUIRED_FIELDS = [
    "id",
    "displayName",
    "engine",
    "format",
    "fileName",
    "sha256"
]

SHA256_REGEX = re.compile(r"^[a-fA-F0-9]{64}$")


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def validate_model(model):
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in model:
            errors.append(f"Missing field: {field}")

    if "sha256" in model:
        if not SHA256_REGEX.match(model["sha256"]):
            errors.append("Invalid sha256 format")

    if "sizeBytes" in model:
        if model["sizeBytes"] <= 0:
            errors.append("Invalid sizeBytes")

    return errors


def main():
    if not os.path.exists(CATALOG_PATH):
        print("catalog.json not found")
        return

    catalog = load_json(CATALOG_PATH)

    models = catalog.get("models", [])

    ids = set()
    filenames = set()

    has_error = False

    for model in models:
        print(f"Validating {model.get('id')}...")

        # Validate structure
        errors = validate_model(model)

        # Duplicate checks
        if model["id"] in ids:
            errors.append("Duplicate model id")
        ids.add(model["id"])

        if model["fileName"] in filenames:
            errors.append("Duplicate filename")
        filenames.add(model["fileName"])

        if errors:
            has_error = True
            print(f"❌ {model['id']} errors:")
            for e in errors:
                print(f"   - {e}")
        else:
            print("✅ OK")

    if has_error:
        print("\nValidation failed")
        exit(1)
    else:
        print("\nAll models valid")


if __name__ == "__main__":
    main()