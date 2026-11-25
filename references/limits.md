# Limits

| condition | behaviour |
|---|---|
| YAML/TOML config | treated as absent (reported), not partially parsed |
| parameter outside the fixed vocabulary | not tabulated |
| number written as a word above five | not normalised |
| two configs in the case | the first JSON object with 3+ keys wins |
| parameter stated twice with different values | two rows, one may conflict |
