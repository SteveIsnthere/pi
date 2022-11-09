from cam.modes import *
from cam.processing_pipelines.helpers import save_image

save_image(get_highest_quality_image(), "cam/data/output.jpg")
