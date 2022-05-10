from django.apps import AppConfig
import pandas as pd
from joblib import load
import os
import torch
from .colorModels import MainModel, build_res_unet


class PredictionConfig(AppConfig):
    name = 'prediction'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MLMODEL_FOLDER = os.path.join(BASE_DIR, 'prediction/mlmodel/')
    MLMODEL_FILE = os.path.join(MLMODEL_FOLDER, "IRISRandomForestClassifier.joblib")
    mlmodel = load(MLMODEL_FILE)


class PredictionImageConfig(AppConfig):
    name = 'prediction'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net_G = build_res_unet(n_input=1, n_output=2, size=256)
    net_G.load_state_dict(
        torch.load("C:/DiplomaProjects/ProjectOne/backend/django_app/prediction/res18-unet.pt", map_location=device))
    mlmodel = MainModel(net_G=net_G)
    mlmodel.load_state_dict(
        torch.load(
            "C:/DiplomaProjects/ProjectOne/backend/django_app/prediction/final_model_weights.pt",
            map_location=device
        )
    )
