# Week 7: CNNs and Transfer Learning

## Setup
```bash
pip install tensorflow scikit-learn matplotlib kaggle numpy
```
A GPU is strongly recommended for exercises 2 and 3. On CPU, ResNet50 fine-tuning on
~14k images can take hours. Google Colab with a GPU runtime works well.

### Dataset for exercises 2 and 3
```bash
kaggle datasets download -d puneet6060/intel-image-classification -p data --unzip
```
Keras needs `data/train/<class>/` and `data/test/<class>/`. Check the extracted folder
names; the Intel archive nests its folders, so you may need to move them, for example:
```bash
mv data/seg_train/seg_train data/train
mv data/seg_test/seg_test data/test
```
Each class should be one subfolder. If you use a different Kaggle dataset, arrange it the
same way; the code reads class names from the folders.

Exercise 1 downloads CIFAR-10 automatically.

## Files
| File | Purpose |
|---|---|
| `01_cnn_cifar10.py` | CNN from scratch on CIFAR-10, with feature map visualization |
| `image_data.py` | Shared data loading, augmentation, and pipeline helpers |
| `02_cnn_real_world.py` | Scratch CNN with augmentation, plus error analysis |
| `03_transfer_learning.py` | ResNet50 fine-tuning, compared with the scratch CNN |

Run in order: 02 must finish before 03, because 03 reads `cnn_scratch_results.json`.

## Design decisions
- **Augmentation is inside the model**, so Keras turns it off at inference time and the saved
  model applies it correctly on any new input.
- **Global average pooling instead of Flatten** cuts the parameter count a lot and reduces
  overfitting.
- **Same split and image size for both models**, so the comparison is fair. Both use seed 42.
- **Two-phase fine-tuning.** Training a randomly initialized head on top of a frozen base first
  prevents large early gradients from damaging the pretrained features. Phase 2 uses a
  learning rate 100× smaller.
- **BatchNorm stays frozen** during fine-tuning, and `training=False` keeps it in inference mode.

## Results
Fill in after running.

### Exercise 1: CIFAR-10
- Test accuracy:
- Which filters in the first block look like edges or color blobs? In the last block, do they look more object-specific?

### Exercise 2: Scratch CNN and error analysis
- Test accuracy and per-class F1:
- Top confusions (from the script output). Are they visually similar classes?
- Look at `02_worst_errors.png`. Are the high-confidence mistakes genuinely ambiguous, or mislabeled?
- Effect of augmentation: rerun with the augmentation layer removed and compare the gap between train and validation accuracy.

### Exercise 3: Transfer learning
- Test accuracy of the fine-tuned ResNet50 compared with the scratch CNN:
- How much did phase 2 add beyond phase 1?
- Trainable parameters and training time for each model:
- Where did the transfer model still fail, and does that match the scratch CNN's failures?
