import os


# =============================================================================
# PROJECT'S ORGANIZATION
# =============================================================================
PROJECT_BASE = '.'

#===============================================================================
# PROJECT'S PARAMETERS
#===============================================================================
FONT = os.path.join(PROJECT_BASE, 'basic', 'Aller_Bd.ttf')

TIME_FM = '-%Y%m%d-%H%M%S'

#===============================================================================
# PROJECT'S MODELS
#===============================================================================
MODEL_DIR = 'openvino'
CAR_DET_XML = os.path.join(MODEL_DIR, 'person-vehicle-bike-detection-crossroad-0078.xml')
CAR_DET_BIN = os.path.join(MODEL_DIR, 'person-vehicle-bike-detection-crossroad-0078.bin')
