# 3 Method

## 3.1 Training setup

We train the sparse router with AdamW at a learning rate of 3e-4, a batch size of 64,
and 12 epochs with a cosine schedule. The random seed is 42. Dropout is set to 0.1 in
all layers. Training runs on a single A100 40GB for approximately 9 hours.

## 3.2 Evaluation

We evaluate on the standard split with beam width 4 and report exact match. Each
configuration is run three times and we report the mean.

## Parameter provenance

| parameter | in text | in config | status |
|---|---|---|---|
| learning_rate | 3e-4 | 0.0003 | matched |
| batch_size | 64 | 64 | matched |
| epochs | 12 | 12 | matched |
| optimizer | AdamW | AdamW | matched |
| schedule | cosine | cosine | matched |
| hardware | A100 | A100 40GB | matched |
| beam_width | 4 | 4 | matched |
| repeats | three | 3 | matched |
| dataset | standard split | standard split | matched |
| wall_clock_hours | 9 | 9 | matched |

## Reproduction checklist

| item | status | found in |
|---|---|---|
| the exact code revision | unknown | — |
| pinned dependency versions | unknown | — |
| the hardware the numbers came from | present | method text, config |
| random seeds and repetition count | present | method text, config |
| which split was used | present | method text, config |
| the hyperparameters | present | method text, config |
| how long a run takes | present | method text, config |
| the metric and its definition | present | method text, config |
