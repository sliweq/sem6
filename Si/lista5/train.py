from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import os
from tmp import generate_datasets
import matplotlib.pyplot as plt
from modify_photos import apply_distortions
import random

mtcnn = MTCNN(image_size=160, margin=20)
facenet = InceptionResnetV1(pretrained='vggface2').eval()
img_dir = "img_align_celeba"

def get_embedding(image_path, distorted=False):
    img = Image.open(image_path).convert('RGB')
    if distorted:
        img = apply_distortions(img)
    face = mtcnn(img)
    if face is None:
        raise ValueError(f"No face detected in {image_path}")
    embedding = facenet(face.unsqueeze(0))
    return embedding.detach()

# Function to compare two images and get the absolute difference vector
def get_diff_vector(img1_path, img2_path, distorted=False):
    emb1 = get_embedding(img1_path, distorted)
    emb2 = get_embedding(img2_path, distorted)
    return torch.abs(emb1 - emb2)

# Define the MLP model that takes the difference between two embeddings
class FaceVerificationMLP(nn.Module):
    def __init__(self, input_dim=512):
        super(FaceVerificationMLP, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 2)  # Output: [same_person_prob, different_person_prob]
        )

    def forward(self, x):
        return self.model(x)


def train_and_evaluate(train_data, test_data, lr=0.001, epochs=20,distorted = False):
    X_train, y_train = [], []
    for img1, img2, label in train_data:
        if distorted:
            distorted = random.random() < 0.5
        try:
            diff = get_diff_vector(os.path.join(img_dir, img1), os.path.join(img_dir, img2), distorted)
            X_train.append(diff.squeeze(0))
            y_train.append(label)
        except:
            continue

    X_train = torch.stack(X_train)
    y_train = torch.tensor(y_train)

    model = FaceVerificationMLP()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()

    X_test, y_test = [], []
    for img1, img2, label in test_data:
        try:
            diff = get_diff_vector(os.path.join(img_dir, img1), os.path.join(img_dir, img2))
            X_test.append(diff.squeeze(0))
            y_test.append(label)
        except:
            continue

    X_test = torch.stack(X_test)
    y_test = torch.tensor(y_test)

    model.eval()
    with torch.no_grad():
        outputs = model(X_test)
        _, predicted = torch.max(outputs, 1)

    acc = accuracy_score(y_test, predicted)
    prec = precision_score(y_test, predicted)
    rec = recall_score(y_test, predicted)
    f1 = f1_score(y_test, predicted)
    cm = confusion_matrix(y_test, predicted)

    return acc, prec, rec, f1, cm, model

def train_and_save_models_task_1():

    train_sets, test_set = generate_datasets()

    results = {}
    for size, data in train_sets.items():
        acc, prec, rec, f1, cm, model = train_and_evaluate(data, test_set)
        results[size] = {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1": f1,
            "confusion_matrix": cm
        }
        print(f"\nTrain size: {size}")
        print(f"Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}")
        print(f"Confusion Matrix:\n{cm}")
        torch.save(model,f"models2/model_{size}_1.pth")


    sizes = sorted(results.keys())
    accuracies = [results[s]['accuracy'] for s in sizes]
    f1_scores = [results[s]['f1'] for s in sizes]
    return results 

    # plt.figure(figsize=(10, 5))
    # plt.plot(sizes, accuracies, label='Accuracy')
    # plt.plot(sizes, f1_scores, label='F1 Score')
    # plt.xlabel('Liczba par treningowych')
    # plt.ylabel('Wartość metryki')
    # plt.title('Wpływ liczby par treningowych na skuteczność')
    # plt.legend()
    # plt.grid()
    # plt.show()

def train_and_save_models_task_2():
    learning_rates = [0.00001, 0.0001, 0.001, 0.01, 0.1]
    train_sizes = [1000]
    test_size = 200

    train_sets, test_set = generate_datasets(train_sizes=train_sizes, test_size=test_size)
    train_data = train_sets[1000]

    results = {}

    for lr in learning_rates:
        print(f"\nTraining with learning rate: {lr}")
        acc, prec, rec, f1, cm, model = train_and_evaluate(train_data, test_set, lr=lr, epochs=20)
        results[lr] = {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1": f1,
            "confusion_matrix": cm
        }
        print(f"Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}")
        print(f"Confusion Matrix:\n{cm}")
        torch.save(model, f"models2/model_lr_{lr:.0e}.pth")  

    accs = [results[lr]["accuracy"] for lr in learning_rates]
    f1s = [results[lr]["f1"] for lr in learning_rates]

    # import matplotlib.pyplot as plt
    # plt.figure(figsize=(10, 5))
    # plt.plot(learning_rates, accs, marker='o', label="Accuracy")
    # plt.plot(learning_rates, f1s, marker='o', label="F1 Score")
    # plt.xscale("log")
    # plt.xlabel("Learning Rate (log scale)")
    # plt.ylabel("Metric Value")
    # plt.title("Wpływ tempa uczenia na skuteczność (1000 par, 20 epok)")
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    return results

def train_and_save_models_task_3():
    train_sizes = [1000]
    test_size = 200
    epoch_counts = [1, 5, 10, 20, 50]  
    learning_rate = 0.001 

    train_sets, test_set = generate_datasets(train_sizes=train_sizes, test_size=test_size)
    train_data = train_sets[1000]

    results = {}

    for epochs in epoch_counts:
        print(f"\nTraining with {epochs} epochs")
        acc, prec, rec, f1, cm, model = train_and_evaluate(train_data, test_set, lr=learning_rate, epochs=epochs)
        results[epochs] = {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1": f1,
            "confusion_matrix": cm
        }
        print(f"Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}")
        print(f"Confusion Matrix:\n{cm}")
        torch.save(model, f"models2/model_epochs_{epochs}.pth")

    accs = [results[e]["accuracy"] for e in epoch_counts]
    f1s = [results[e]["f1"] for e in epoch_counts]

    # import matplotlib.pyplot as plt
    # plt.figure(figsize=(10, 5))
    # plt.plot(epoch_counts, accs, marker='o', label="Accuracy")
    # plt.plot(epoch_counts, f1s, marker='o', label="F1 Score")
    # plt.xlabel("Liczba epok")
    # plt.ylabel("Wartość metryki")
    # plt.title("Wpływ liczby epok na skuteczność (1000 par, lr = 0.001)")
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    return results

def evaluate_on_clean_and_distorted(model, test_data):
    X_clean, X_distorted, y_true = [], [], []

    for img1, img2, label in test_data:
        try:
            clean_diff = get_diff_vector(os.path.join(img_dir, img1), os.path.join(img_dir, img2))
            distorted_diff = get_diff_vector(
                os.path.join(img_dir, img1), os.path.join(img_dir, img2),
                distorted=True
            )
            X_clean.append(clean_diff.squeeze(0))
            X_distorted.append(distorted_diff.squeeze(0))
            y_true.append(label)
        except:
            continue

    X_clean = torch.stack(X_clean)
    X_distorted = torch.stack(X_distorted)
    y_true = torch.tensor(y_true)

    model.eval()
    with torch.no_grad():
        pred_clean = torch.argmax(model(X_clean), dim=1)
        pred_distorted = torch.argmax(model(X_distorted), dim=1)

    print("===> Czyste dane:")
    print(f"Accuracy: {accuracy_score(y_true, pred_clean):.4f}, F1: {f1_score(y_true, pred_clean):.4f}")
    print("===> Zaburzone dane:")
    print(f"Accuracy: {accuracy_score(y_true, pred_distorted):.4f}, F1: {f1_score(y_true, pred_distorted):.4f}")

if __name__ == "__main__":
    pass