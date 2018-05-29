# ML frameworks and models serialization

## Frameworks

**Keras, Caffe2, Scikit-learn, TensorRT** ML frameworks are fully supported by 0Mind server now.

**TensorRT** can be used only with NVIDIA GPU's with serialized models from engines **caffe, tensorflow, uff, PLAN**

You can easly add support of any ML framework, that has Python 3 bindings,
using [adapters mechanism](ADAPTERS.MD).

## Model's serialization
Use your framework's functionality for serialization of the model into one file.
Optionaly you can use framework name as serialized file's extension for
simplification of 0Mind configuration and model recognition in a file system.

If target ML framework have no tools for model serialization into
single file or it has no functionality for description of model's interface, required
by 0Mind, you should do that using [framework adapters](ADAPTERS.MD) and additional structures in
serialized model files by using **helpers.serialization_helper.SerializationHelper.save_model() method**. Or you can do it manualy. For example...

### Caffe2
It serializes ML model into files: **init_net.pb**, **predict_net.pb**
and has no methods to describe model's interface, so we should do it manualy.
Create files ***input_spec.json*** and ***output_spec.json***. Describe model's
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
Optionaly you can change result file's extension to **caffe2**.
Now your model is ready for 0Mind. 
Alternatively you can use **helpers.serialization_helper.SerializationHelper.save_model()** for model preparing.

### Scikit-learn
You should use **SerializationHelper** to save model into file. For example:
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

### TensorRT
