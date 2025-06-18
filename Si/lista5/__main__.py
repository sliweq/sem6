import os
from pathlib import Path
import matplotlib.pyplot as plt

from tmp import generate_datasets
from train import (
    train_and_save_models_task_1,
    train_and_save_models_task_2,
    train_and_save_models_task_3,
    evaluate_on_clean_and_distorted,
    FaceVerificationMLP,
    train_and_evaluate
)
import torch

results_dir = Path("results2")
results_dir.mkdir(parents=True, exist_ok=True)

def save_plot(fig, filename):
    fig.savefig(results_dir / filename)
    plt.close(fig)

def run_task_1_and_save():
    train_sets, test_set = generate_datasets()
    results = {}

    for size, data in train_sets.items():
        acc, prec, rec, f1, cm, model = train_and_evaluate(data, test_set)
        results[size] = {"accuracy": acc, "f1": f1}
        torch.save(model, f"models/model_{size}_1.pth")

    sizes = sorted(results.keys())
    accs = [results[s]['accuracy'] for s in sizes]
    f1s = [results[s]['f1'] for s in sizes]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(sizes, accs, label='Accuracy')
    ax.plot(sizes, f1s, label='F1 Score')
    ax.set_title("Wpływ liczby par treningowych na skuteczność")
    ax.set_xlabel("Liczba par treningowych")
    ax.set_ylabel("Wartość metryki")
    ax.legend()
    ax.grid()
    save_plot(fig, "task1_training_size_effect.png")

def run_task_2_and_save():
    results = train_and_save_models_task_2()
    learning_rates = sorted(results.keys())
    accs = [results[lr]["accuracy"] for lr in learning_rates]
    f1s = [results[lr]["f1"] for lr in learning_rates]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(learning_rates, accs, marker='o', label="Accuracy")
    ax.plot(learning_rates, f1s, marker='o', label="F1 Score")
    ax.set_xscale("log")
    ax.set_xlabel("Learning Rate (log scale)")
    ax.set_ylabel("Metric Value")
    ax.set_title("Wpływ tempa uczenia na skuteczność (1000 par, 20 epok)")
    ax.legend()
    ax.grid(True)
    save_plot(fig, "task2_learning_rate_effect.png")

def run_task_3_and_save():
    results = train_and_save_models_task_3()
    epochs = sorted(results.keys())
    accs = [results[e]["accuracy"] for e in epochs]
    f1s = [results[e]["f1"] for e in epochs]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(epochs, accs, marker='o', label="Accuracy")
    ax.plot(epochs, f1s, marker='o', label="F1 Score")
    ax.set_xlabel("Liczba epok")
    ax.set_ylabel("Wartość metryki")
    ax.set_title("Wpływ liczby epok na skuteczność (1000 par, lr = 0.001)")
    ax.legend()
    ax.grid(True)
    save_plot(fig, "task3_epochs_effect.png")

def load_model_and_evaluate(model_path, test_data):
    print(f"Loading model from {model_path}")
    model = torch.load(model_path)
    evaluate_on_clean_and_distorted(model, test_data)


if __name__ == "__main__":
    print("=== Zadanie 1 ===")
    run_task_1_and_save()

    print("=== Zadanie 2 ===")
    run_task_2_and_save()

    print("=== Zadanie 3 ===")
    run_task_3_and_save()

    # print("=== Ocena modelu na czystych vs zaburzonych danych ===")
    # _, test_set = generate_datasets(train_sizes=[1000], test_size=200)
    # load_model_and_evaluate("models2/model_epochs_20.pth", test_set)
