from src.lab_corrector import LabCorrector
from dados_lab import DadosLab


corrector = LabCorrector(DadosLab())

corrector.make_correction()