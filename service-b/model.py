import os
import torch
import torch.nn as nn
import numpy as np
import joblib
from collections import deque

class MultivariateAutoencoder(nn.Module):
    def __init__(self):
        super(MultivariateAutoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(20, 10),
            nn.LeakyReLU(0.2),
            nn.Linear(10, 4)
        )
        self.decoder = nn.Sequential(
            nn.Linear(4, 10),
            nn.LeakyReLU(0.2),
            nn.Linear(10, 20)
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

class AnomalyDetector:
    def __init__(self, model_path='model/autoencoder_weights.pth', scaler_path='model/feature_scaler.pkl', threshold=0.5):
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            raise FileNotFoundError("Poids ou Scaler introuvables. Vérifiez le dossier 'model/'.")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.scaler = joblib.load(scaler_path)
        self.model = MultivariateAutoencoder().to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval() 
        self.threshold = threshold
        self.sequence_buffer = deque(maxlen=10)

    def predict(self, cpu_usage: float, disk_bytes: float):
        raw_data = np.array([[cpu_usage, disk_bytes]])
        scaled_data = self.scaler.transform(raw_data)[0] 
        self.sequence_buffer.append(scaled_data)
        if len(self.sequence_buffer) < 10:
            return False, 0.0
  
        sequence_array = np.array(self.sequence_buffer).flatten()
        
        input_tensor = torch.tensor(sequence_array, dtype=torch.float32).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            reconstructed = self.model(input_tensor)
            
        mse_loss = torch.mean((input_tensor - reconstructed) ** 2).item()
        is_anomaly = mse_loss > self.threshold
        
        return is_anomaly, float(mse_loss)
    