# ML frameworks and models serialization

## Frameworks

Supported ML frameworks: keras, caffe2.

You can easly add support for any ML framework, that has Python bindings,
using [adapters mechanism](ADAPTERS.MD).

## Model's serialization
Use your framework's functionality for serialization of the model into one file.
Optionaly you can use framework name as serialized file's extension for
simplification of 0Mind configuration and model recognition in a file system.

If target ML framework does not have tools for model's serialization into
single file or it has no functionality for description of model's interface, required
by 0Mind, you should do that using [framework adapters](ADAPTERS.MD) and additional structures in
serialized model files. For example...

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