# Urban Bikeway Obstacle Detection using Smartphone

The "Untitled Application" is a system that uses depth perception and information from a handlebar-mounted smartphone's sensors to detect and classify obstacles on urban bikeways. It employs machine learning algorithms and is measured based on the 3 feet rule of bike safety. The study will evaluate the system's accuracy using at least 10,000 training images captured during actual bike rides in the urban city of Berlin. The system will only cover ground objects.

## Notebooks

* `01_data_exploration.ipynb`: This notebook explores the characteristics of the collected data, evaluates the quality of depth maps, and takes note of the relevant properties for the model training.
* `02_data_preparation.ipynb`: This notebook provides a complete preprocessing pipeline for images, including image processing techniques and data augmentation, to ensure the images are of consistent quality and suitable for training a machine learning model. It also implements label encoding for binary classification tasks (0 for no obstacle, 1 for obstacle)
* `03_model_playground.ipynb`: This notebook is intended as a playground to test out different models with the data prepared from the previous notebook.
