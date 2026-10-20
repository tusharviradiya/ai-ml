# Week 5: Neural Networks from Scratch

| File | Exercise |
|---|---|
| `01_perceptron.py` | Single perceptron learning AND and OR |
| `02_neural_net_from_scratch.py` | 2-4-1 network with manual backprop, trained on XOR |
| `03_activation_optimizer_exploration.py` | Activation and optimizer sweep, with loss curves |
| `04_keras_model.py` | Same XOR network rebuilt in Keras |

Requirements: `pip install numpy matplotlib tensorflow`

## Notes

### Forward propagation
Each layer computes a linear transform followed by a nonlinearity. For a
2-4-1 net: `z1 = X·W1 + b1`, `a1 = σ(z1)`, `z2 = a1·W2 + b2`, `a2 = σ(z2)`.
The hidden layer lets the network build a nonlinear decision boundary; a
single perceptron cannot represent XOR.

### Backward propagation
Backprop applies the chain rule from the loss back through each layer. With
sigmoid output and binary cross-entropy the output gradient simplifies to
`dz2 = (a2 - y) / N`. Each earlier layer then multiplies by the downstream
weights and by the local activation derivative (for sigmoid, `a(1 - a)`).
Weight gradients are `aᵀ·dz`, and bias gradients are the sum of `dz`.

### Activation and optimizer observations
Fill these in after running `03_activation_optimizer_exploration.py`:

- **Activations:** Which one converged fastest? Did sigmoid show slower
  learning from saturation? Did ReLU ever get stuck with dead units?
- **Optimizers:** How did plain SGD compare to momentum and Adam at their
  learning rates? Did Adam converge faster, and was it more sensitive to lr?
- **Caveat:** The learning rates were tuned per optimizer, so the comparison
  is fair only in terms of loss curves, not raw step size.

## Pushing to GitHub

```bash
git add week-5/
git commit -m "Week 5: neural networks from scratch and Keras"
git push origin main
```
