# Sprint 1 -- Multi-Seed Phase II Baseline: Variance Memo

Seeds run: [0, 1, 2, 3, 4] (n=5)
Runtime per seed: mean 229.0 min, range [90.1, 526.6] min

## baseline
- top1_acc: mean=0.4353 std=0.1073 median=0.4326  <-- std > 3pp
- balanced_acc: mean=0.4353 std=0.1073 median=0.4326  <-- std > 3pp
- head_f1: mean=0.4754 std=0.1090 median=0.4742  <-- std > 3pp
- mid_f1: mean=0.4381 std=0.1073 median=0.4326  <-- std > 3pp
- tail_f1: mean=0.3328 std=0.1303 median=0.3314  <-- std > 3pp
- head_tail_f1_gap: mean=0.1426 std=0.0252 median=0.1474
- worst_class_f1: mean=0.0185 std=0.0414 median=0.0000  <-- std > 3pp
- worst_class_acc: mean=0.0100 std=0.0224 median=0.0000

## rebal
- top1_acc: mean=0.4997 std=0.1330 median=0.5953  <-- std > 3pp
- balanced_acc: mean=0.4997 std=0.1330 median=0.5953  <-- std > 3pp
- head_f1: mean=0.5144 std=0.1363 median=0.6111  <-- std > 3pp
- mid_f1: mean=0.4885 std=0.1477 median=0.5934  <-- std > 3pp
- tail_f1: mean=0.4730 std=0.1370 median=0.5688  <-- std > 3pp
- head_tail_f1_gap: mean=0.0415 std=0.0046 median=0.0393
- worst_class_f1: mean=0.1333 std=0.1154 median=0.1818  <-- std > 3pp
- worst_class_acc: mean=0.0920 std=0.0844 median=0.1100  <-- std > 3pp

## rebal_crt
- top1_acc: mean=0.5327 std=0.0878 median=0.5942  <-- std > 3pp
- balanced_acc: mean=0.5327 std=0.0878 median=0.5942  <-- std > 3pp
- head_f1: mean=0.5434 std=0.0979 median=0.6068  <-- std > 3pp
- mid_f1: mean=0.5303 std=0.0965 median=0.5917  <-- std > 3pp
- tail_f1: mean=0.5112 std=0.0839 median=0.5674  <-- std > 3pp
- head_tail_f1_gap: mean=0.0322 std=0.0156 median=0.0337
- worst_class_f1: mean=0.1565 std=0.0934 median=0.2137  <-- std > 3pp
- worst_class_acc: mean=0.1140 std=0.0754 median=0.1400  <-- std > 3pp

## Variance assessment
The following metrics exceed the 3pp across-seed std threshold from the sprint brief, which would weaken the equity claim if it holds up under inspection:
- baseline.top1_acc: std=0.1073
- baseline.balanced_acc: std=0.1073
- baseline.head_f1: std=0.1090
- baseline.mid_f1: std=0.1073
- baseline.tail_f1: std=0.1303
- baseline.worst_class_f1: std=0.0414
- rebal.top1_acc: std=0.1330
- rebal.balanced_acc: std=0.1330
- rebal.head_f1: std=0.1363
- rebal.mid_f1: std=0.1477
- rebal.tail_f1: std=0.1370
- rebal.worst_class_f1: std=0.1154
- rebal.worst_class_acc: std=0.0844
- rebal_crt.top1_acc: std=0.0878
- rebal_crt.balanced_acc: std=0.0878
- rebal_crt.head_f1: std=0.0979
- rebal_crt.mid_f1: std=0.0965
- rebal_crt.tail_f1: std=0.0839
- rebal_crt.worst_class_f1: std=0.0934
- rebal_crt.worst_class_acc: std=0.0754

Suggested follow-ups per the sprint brief's mitigation:
- Compare per-seed run.log cGAN g/d loss curves for outlier seeds -- large divergence would point to cGAN seed-dependence rather than the classifier itself.
- Re-run the highest-variance seed with a tuned gradient-clipping schedule (e.g. warmup clipnorm) and compare against its original run.
- Report the median (above) alongside the mean when presenting Table 3, as medians are less sensitive to any single outlier seed.
