# gistrallm

Minimal model-catalog repository for **Gistra** local AI.

This repository is intended to:
- publish a small machine-readable model catalog for the Gistra mobile app
- publish per-model manifests for local GGUF models
- publish checksums for download verification
- attach the actual `.gguf` files as **GitHub Release assets** instead of storing them in git history

## Repository purpose

This repository is **metadata-first**. It should not contain the large GGUF binaries in the git tree.
Store actual model files in GitHub Releases and reference them from the manifest files.

## Initial model lineup

- Qwen 2.5 1.5B Instruct — balanced default
- Gemma 3 1B IT QAT Q4_0 — smaller / faster option
- Phi-3 Mini 4K Instruct — higher-quality option

## Release asset naming

Use these exact filenames in GitHub Releases:

- `qwen2.5-1.5b-instruct-q4_k_m.gguf`
- `gemma-3-1b-it-qat-q4_0.gguf`
- `Phi-3-mini-4k-instruct-q4.gguf`

## Client integration flow

1. Download `manifests/catalog.json`
2. Read the model list
3. Let the user pick a model
4. Download the selected `.gguf` file from `downloadUrl`
5. Verify `sha256`
6. Save the file locally in the Gistra app
7. Load it through `flutter_llama`

## Updating a model manifest

When you publish a real release asset, update:
- `downloadUrl`
- `sha256`
- `sizeBytes`
- `releaseTag`

Then regenerate `checksums/SHA256SUMS.json`.

## Notes

- Some model families have special license terms. Check the original model page before redistribution.
- This repository includes example metadata only. Replace placeholder hashes and URLs before production use.
