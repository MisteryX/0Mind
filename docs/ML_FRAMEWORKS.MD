# Machine learning frameworks

## Frameworks

**Keras, Caffe2, Scikit-learn, TensorRT** ML frameworks are fully supported by 0Mind server now.

**TensorRT** can be used only with NVIDIA GPU's with serialized models of engines **caffe, tensorflow, uff, PLAN**

You can easly add support of any ML framework, that has Python 3 bindings,
using [adapters mechanism](ADAPTERS.MD).

## Model serialization and loading
Use target ML framework functionality for serialization of model into file.
Optionaly you can use framework name as serialized file extension for
simplification of 0Mind configuration and model recognition in a file system.

If target ML framework have no tools for model serialization into
single file or it has no functionality for description of model's interface, required
by 0Mind, you can do this using [framework adapters](ADAPTERS.MD) with additional structures in
serialized model files by using **helpers.serialization_helper.SerializationHelper.save_model() method**.
Or you can use additional task parameters to load model from several files and specify model interface (inputs and outputs).

1. [Keras](#keras)
1. [Caffe2](#caffe2)
1. [SciKit learn](#scikit-learn)
1. [TensorRT](#tensorrt)
    1. [Tensoflow](#tensorflow)
    1. [Caffe](#caffe)
    1. [UFF](#uff)
    1. [PLAN](#plan)

### Keras
This great tool has all required features to serialize and distribute models,
including interface specification.

So load Keras models as usual from single file without any special params.
```
curl -d '{"model_file": "ML/models/mnist_cnn_model.keras", "id": "1", "model_type": "keras", "input_filters": {"conv2d_1_input:0": ["i_img_file_to_ns_arr.ImageFileToNormAndScaledNPArrayFilter"]}, "output_filters": {}}' -H "Content-Type:application/json" -X POST http://127.0.0.1:5885/model/load
```

### Caffe2
It serializes ML model into files: **init_net.pb**, **predict_net.pb**
and has no methods to describe model's interface, so we should do it manualy.

Caffe2 model can be loaded using request like:
```
curl -d '{"id": "2", "model_file": "ML/models/init_net.pb", "input_filters": {"data": ["i_img_file_to_caffe2.ImageFileCaffe2Filter"]}, "output_filters": {"default": ["io_argmax.ArgMaxFilter"]}, "model_type": "caffe2", "predict_net.pb": "ML/models/predict_net.pb", "inputs": [{"name": "data", "type": "uint8", "shape": [1, 3, 224, 224]}], "outputs": [{"name": "default", "type": "float64", "shape": [1, 1000]}]}' -H "Content-Type:application/json" -X POST http://127.0.0.1:5885/model/load
```
Or if you prefer to store all information about model in one file,
create files ***input_spec.json*** and ***output_spec.json***. Describe model
inputs in ***input_spec.json*** using format
```
{
  "inputs": [
    {
      "name": "data",
      "type": "uint8",
      "shape": [1, 3, 224, 224]
    }
  ]
}
```
**name** - it is the name of the model's input

**type** - type of the each tensor element

**shape** - it is the tensor shape, and the first dimension is batch size which
can be **None** (means any batch size is possible to process).

File ***output_spec.json*** has the same format:
```
{
  "outputs": [
    {
      "name": "default",
      "type": "uint8",
      "shape": [1, 1000]
    }
  ]
}
```
After that put all of this files into tar.gz archive:
```
init_net.pb
predict_net.pb
input_spec.json
output_spec.json
```
Optionaly you can change result file extension to **caffe2**.
Now your model is ready for 0Mind. 

Alternatively you can use **helpers.serialization_helper.SerializationHelper.save_model()** for model preparation.

### Scikit-learn
To load model you can use request like:
```
curl -d '{"id": "2", "model_type": "sklearn", "model_file": "ML/models/model.jbl", "input_filters": {}, "output_filters": {}, "inputs": [{"name": "data", "type": "float64", "shape": [null, 203]}], "outputs": [{"name": "data", "type": "float64", "shape": [null, 1]}] }' -H "Content-Type:application/json" -X POST http://127.0.0.1:5885/model/load
```
Or you should use **SerializationHelper** to save model into one file.
For example:
```
from helpers.serialization_helper import SerializationHelper
...
model.fit(features, results)
...
SerializationHelper.save_model(
    'sklearn',
    model,
    serialized_file_name,
    {'inputs': [{'name': 'main', 'type': 'float32', 'shape': [1, 28]}]},
    {'outputs': [{'name': 'default', 'type': 'float32', 'shape': [1, 1]}]}
)
```
and load it into 0Mind as usual.

### TensorRT
This tool has several engines with different set of params for model loading.

You should use "model_type" task param with value **tensorrt**.

Main task param, for TensorRT engine specification is **framework**.
Use exactly the same framework names as specified in TensorRT documentation.

Of cause, you still need in model interface specification, so specify it using **"inputs"** and **"outputs"** task params.

Model serialization mechanics have been described in TensorRT documentation.

#### Tensorflow
You can load tensorflow model into TensorRT engine using 0Mind with command like

```
curl -d '{"id": "2", "model_type": "tensorrt", "framework": "tf", "model_file": "/opt/tensorrt/data/mnist/lenet5_mnist_frozen.pb", "inputs": [{"name": "in", "type": "float32", "shape": [null,1,28,28]}], "outputs": [{"name": "out", "type": "uint32", "shape": [null,1]}], "input_filters": {"in": ["i_img_file_to_ns_arr.ImageFileToNormAndScaledNPArrayFilter"]}}, "output_filters": {}' -H "Content-Type:application/json" -X POST 127.0.0.1:5885/model/load
```

#### Caffe
To load caffe model, request should be like this

```
curl -d '{"id": "2", "model_type": "tensorrt", "framework": "caffe", "model_file": "mnist/mnist.caffemodel", "deployfile": "mnist/mnist.prototxt", "inputs": [{"name": "data", "type": "float32", "shape": [null,1,28,28]}], "outputs": [{"name": "prob", "type": "uint32", "shape": [null,1]}], "input_filters": {"data": ["i_img_file_to_ns_arr.ImageFileToNormAndScaledNPArrayFilter"]}}, "output_filters": {}' -H "Content-Type:application/json" -X POST 127.0.0.1:5885/model/load
```

#### UFF
Request example:
```
curl -d '{"id": "2", "model_type": "tensorrt", "framework": "uff", "model_file": "/opt/tensorrt/data/mnist/lenet5_mnist_frozen.pb", "inputs": [{"name": "in", "type": "float32", "shape": [null,1,28,28]}], "outputs": [{"name": "out", "type": "uint32", "shape": [null,1]}], "input_filters": {"in": ["i_img_file_to_ns_arr.ImageFileToNormAndScaledNPArrayFilter"]}, "output_filters": {}}' -H "Content-Type:application/json" -X POST 127.0.0.1:5885/model/load
```

#### PLAN
Request example:
```
curl -d '{"id": "2", "model_type": "tensorrt", "framework": "PLAN", "model_file": "/opt/tensorrt/data/mnist/mnist.plan", "inputs": [{"name": "in", "type": "float32", "shape": [null,1,28,28]}], "outputs": [{"name": "out", "type": "uint32", "shape": [null,1]}], "input_filters": {"in": ["i_img_file_to_ns_arr.ImageFileToNormAndScaledNPArrayFilter"]}, "output_filters": {}}' -H "Content-Type:application/json" -X POST 127.0.0.1:5885/model/load
```