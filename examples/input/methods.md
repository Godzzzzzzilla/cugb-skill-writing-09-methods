# 3 Method

## 3.1 Training setup

We train the sparse router with AdamW at a learning rate of 3e-4, a batch size of 64,
and 12 epochs with a cosine schedule. The random seed is 42. Dropout is set to 0.1 in
all layers. Training runs on a single A100 40GB for approximately 9 hours.

## 3.2 Evaluation

We evaluate on the standard split with beam width 4 and report exact match. Each
configuration is run three times and we report the mean.
