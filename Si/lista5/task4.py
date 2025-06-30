import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import torch
from torch.optim import lr_scheduler
import torch.nn as nn
from train import get_diff_vector
from train import FaceVerificationMLP

img_dir = "img_align_celeba"

def grid_search_parameters(train_data, test_data, 
                           train_sizes=[100, 1000], 
                           learning_rates=[0.0001, 0.001], 
                           epoch_counts=[10, 20], 
                           use_scheduler=False, 
                           use_early_stopping=False, 
                           patience=5):
    """
    Grid search over training size, learning rate, and epoch count.
    Optionally uses learning rate scheduler and early stopping.
    """
    results = {}
    for size in train_sizes:
        # Subsample train_data if needed
        data_subset = train_data[:size]
        for lr in learning_rates:
            for epochs in epoch_counts:
                print(f"Training with size={size}, lr={lr}, epochs={epochs}")
                acc, prec, rec, f1, cm, model = train_with_scheduler_and_early_stopping(
                    data_subset, test_data, lr, epochs, 
                    use_scheduler=use_scheduler, 
                    use_early_stopping=use_early_stopping, 
                    patience=patience
                )
                results[(size, lr, epochs)] = {
                    "accuracy": acc,
                    "precision": prec,
                    "recall": rec,
                    "f1": f1,
                    "confusion_matrix": cm
                }
    return results

class EarlyStopping:
    def __init__(self, patience=7, min_delta=0):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
        self.early_stop = False

    def __call__(self, val_loss):
        if self.best_loss is None or val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True

def train_with_scheduler_and_early_stopping(
    train_data, test_data, lr=0.001, epochs=20, 
    use_scheduler=False, use_early_stopping=False, patience=5):
    X_train, y_train = [], []
    for img1, img2, label in train_data:
        try:
            diff = get_diff_vector(os.path.join(img_dir, img1), os.path.join(img_dir, img2))
            X_train.append(diff.squeeze(0))
            y_train.append(label)
        except:
            continue
    X_train = torch.stack(X_train)
    y_train = torch.tensor(y_train)
    model = FaceVerificationMLP()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    if use_scheduler:
        scheduler = lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=2, factor=0.5)
    if use_early_stopping:
        early_stopper = EarlyStopping(patience=patience)
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()
        # Validation
        X_val, y_val = [], []
        for img1, img2, label in test_data:
            try:
                diff = get_diff_vector(os.path.join(img_dir, img1), os.path.join(img_dir, img2))
                X_val.append(diff.squeeze(0))
                y_val.append(label)
            except:
                continue
        X_val = torch.stack(X_val)
        y_val = torch.tensor(y_val)
        model.eval()
        with torch.no_grad():
            val_outputs = model(X_val)
            val_loss = criterion(val_outputs, y_val).item()
        if use_scheduler:
            scheduler.step(val_loss)
        if use_early_stopping:
            early_stopper(val_loss)
            if early_stopper.early_stop:
                print(f"Early stopping at epoch {epoch+1}")
                break
    # Final evaluation
    model.eval()
    with torch.no_grad():
        outputs = model(X_val)
        _, predicted = torch.max(outputs, 1)
    acc = accuracy_score(y_val, predicted)
    prec = precision_score(y_val, predicted)
    rec = recall_score(y_val, predicted)
    f1 = f1_score(y_val, predicted)
    cm = confusion_matrix(y_val, predicted)
    return acc, prec, rec, f1, cm, model
