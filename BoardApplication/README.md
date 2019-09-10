# QDN Facial Expression Recognition with Keras library

This application demonstrates to train a Keras model (.hdf5) for Facial Expression Recognition and convert it to Snapdragon supported model (.dlc). This process involves two steps:
1. Convert a trained keras model with tensorflow backend to Tensorflow Graph (.pb)
2. Convert the obtained Tensorflow graph (.pb) to SNPE model (.dlc)
 
To develop this application we make use of Snapdragon mobile platforms(HDK 835) and Qualcomm's Neural Processing SDK.
## Recommended setup for model training
### Hardware prerequisite

1. Intel i5 or greater
2. NVIDIA 10 series or greater (only for training on GPU)
3. RAM 16 GB or more

### System software requirements
1. Ubuntu 14.04 LTS or greater
2. CUDA (only for training on GPU)
3. CuDNN (only for training on GPU)
4. Python 2/3

## Installing dependencies

- Execute the following commands for installing the dependencies,

```bash
# Run this command from the <PROJECT_ROOT_DIR>
$ sudo pip install -r BoardApplication/dependencies/requirement.txt
```

## Converting Keras model to single Tensorflow .pb file

1. To start with, we should train a keras model for Facial Expression Recognition. For this, we have followed below repository which demonstrated various architectures for facial emotion classification.
https://github.com/oarriaga/face_classification
2. A sample keras model (.hdf5) for emotion classification which is trained on [fer2013](https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/data) dataset for 10k epochs has been used to convert into Tensorflow graph (.pb).
3. Refer the path '${PROJECT_ROOT_DIR}/BoardApplication/models/trained_keras_models' for trained fer model in keras where ${PROJECT_ROOT_DIR} is the project root directory
4. By running the script '${PROJECT_ROOT_DIR}/BoardApplication/src/hdf5_to_pb.py' with following arguments(optional) we can convert the Keras model into single Tensorflow .pb file.
    - --input_dir [path to trained keras model]
    - --output_dir [path for converted tensorflow model]
    - --graph_name [name of the tensorflow graph with .pb extension]
    ```bash
    # Run this command from the <PROJECT_ROOT_DIR>
    $ python BoardApplication/src/hdf5_to_pb.py --input_dir BoardApplication/models/trained_keras_models/simple_CNN.530-0.65.hdf5 --output_dir BoardApplication/models/converted_tensorflow_models --graph_name tf_model.pb
    ```
    If the arguments are not provided, then the default values are considered.
5. The converted Tensorflow model is saved in the folder '${PROJECT_ROOT_DIR}/BoardApplication/models/converted_tensorflow_models'



## Converting Tensoflow .pb file to .dlc

Prerequisites: Neural Processing SDK setup. Use the instructions from the below link to make the setup,

https://developer.qualcomm.com/software/qualcomm-neural-processing-sdk/getting-started

- Initialize the environmental variables of Neural Processing SDK with tensorflow.
    
- Once you have the .pb file which is generated during training, convert it into Neural Processing SDK's .dlc format using the 'snpe-tensorflow-to-dlc' tool by running the below command from the project's root directory:
```bash
$ snpe-tensorflow-to-dlc --graph BoardApplication/models/converted_tensorflow_models/tf_model.pb -i image_array_input 1,48,48,1 --out_node predictions/Softmax --dlc BoardApplication/models/converted_dlc_models/fer.dlc
```
- Finally the converted dlc file will be saved in '${PROJECT_ROOT_DIR}/BoardApplication/models/converted_dlc_models folder'.

