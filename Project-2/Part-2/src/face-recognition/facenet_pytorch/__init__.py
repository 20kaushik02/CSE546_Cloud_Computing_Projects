from .models.inception_resnet_v1 import InceptionResnetV1
from .models.mtcnn import MTCNN
from .models.utils.detect_face import extract_face

import warnings
warnings.filterwarnings(
    action="ignore", 
    message="This overload of nonzero is deprecated:\n\tnonzero()", 
    category=UserWarning
)