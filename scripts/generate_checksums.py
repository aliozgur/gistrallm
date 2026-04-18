import hashlib
import os
import json

MODELS_DIR = "./models"
OUTPUT_JSON = "./checksums/SHA256SUMS.json"
OUTPUT_TXT = "./checksums/SHA256SUMS.txt"


def sha256_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def main():
    if not os.path.exists(MODELS_DIR):
        print(f"Models directory not found: {MODELS_DIR}")
        return

    checksums = {}

    for filename in os.listdir(MODELS_DIR):
        if filename.endswith(".gguf"):
            filepath = os.path.join(MODELS_DIR, filename)
            print(f"Processing {filename}...")
            hash_value = sha256_file(filepath)
            checksums[filename] = hash_value

    # Write JSON
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(checksums, f, indent=2)

    # Write TXT
    os.makedirs(os.path.dirname(OUTPUT_TXT), exist_ok=True)
    with open(OUTPUT_TXT, "w") as f:
        for filename, hash_value in checksums.items():
            f.write(f"{hash_value}  {filename}\n")

    print("\nDone.")
    print(f"JSON: {OUTPUT_JSON}")
    print(f"TXT : {OUTPUT_TXT}")


if __name__ == "__main__":
    main()