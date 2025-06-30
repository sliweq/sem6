import os
from pathlib import Path
import matplotlib.pyplot as plt

from task4 import train_with_scheduler_and_early_stopping
from tmp import generate_datasets
from train import (
    train_and_save_models_task_1,
    train_and_save_models_task_2,
    train_and_save_models_task_3,
    evaluate_on_clean_and_distorted,
    FaceVerificationMLP,
    train_and_evaluate,
    train_with_blur_task5
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
        torch.save(model, f"models2/model_{size}_1.pth")

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

def run_task_4():
    train_sizes = [100, 1000]
    learning_rates = [0.0001, 0.001, 0.01]
    epoch_counts = [10, 20, 50]
    patience = 3

    train_sets, test_set = generate_datasets(train_sizes=train_sizes, test_size=200)
    results = {}

    for size in train_sizes:
        train_data = train_sets[size]
        for lr in learning_rates:
            for epochs in epoch_counts:
                print(f"Training size={size}, lr={lr}, epochs={epochs}")
                acc, prec, rec, f1, cm, model = train_with_scheduler_and_early_stopping(
                    train_data, test_set, lr=lr, epochs=epochs, patience=patience)
                results[(size, lr, epochs)] = {
                    "accuracy": acc, "precision": prec, "recall": rec, "f1": f1, "confusion_matrix": cm
                }
    return results

def run_task_5_with_mitigation(prob):
    train_sizes = [1000]
    test_size = 200
    train_sets, test_set = generate_datasets(train_sizes=train_sizes, test_size=test_size)
    train_data = train_sets[1000]
    print("Training with distorted augmentation...")
    model = train_with_blur_task5(train_data, test_set, lr=0.001, epochs=50, distortion_prob=prob)


if __name__ == "__main__":
    print("=== Zadanie 1 ===")
    run_task_1_and_save()

    print("=== Zadanie 2 ===")
    run_task_2_and_save()

    print("=== Zadanie 3 ===")
    run_task_3_and_save()

    
    # print("=== Zadanie 4 ===")
    # run_task_4()

    print("=== Zadanie 5 ===")
    run_task_5_with_mitigation(0.5)
    # print("=== Zadanie 5 ===")
    # run_task_5_with_mitigation(0.2)
    # print("=== Zadanie 5 ===")
    # run_task_5_with_mitigation(0.05)