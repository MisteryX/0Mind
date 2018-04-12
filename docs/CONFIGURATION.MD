All 0Mind configuration can be described in 2 json files:
```
configs/logger.json
configs/model_pool_config.json
```

## **logger.json**
Operates with standart Python logger options, which you can find in official documentation.

## **model_pool_config.json**
It is the default configuration file,
but you can specify any using command line option *--config_file* of the **model_pool.py**

Sample configuration is:
```
{
    "id": 1,
    "host": "127.0.0.1",
    "port": 5885,
    "tasks": [
        {
           "id": 1,
           "model_type": "caffe2",
           "model_file": "ML/models/bvlc_alexnet.caffe2",
           "input_filters": {
               "data": [
                   "i_img_file_to_caffe2.ImageFileCaffe2Filter"
               ]
           },
           "output_filters": {
               "default": ["io_argmax.ArgMaxFilter"]
           }
        }
    ],
    "debug": true,
    "model_types": ["caffe2"]
}
```
Compulsory configuration attributes are:

### **id, host, port, tasks**

**id** - (integer) unique model pool identifier

**host** - (string) you can specify desirable existing localy network interface

**port** - (integer) unique service identifier for this host

**tasks** - (list of objects) list of tasks for this model pool

All other configuration parameters are not necessary and can be skipped.

### **Tasks**

It is a list of model pool tasks. This list can be empty.
In other cases you should specify **required task attributes**:

**id** - (integer) unique model identifier

**model_type** - (string) framework identifier (see ML/adapters/base_model.BaseModel.get_package_name())

**model_file** - (string) full path to model file with name and extension

**input_filters** - (dictionary) can be empty or should contain input names with filter list,
that must be applied on input data in specified order

**output_filters** - (dictionary) can be empty or should contain output names with filter list,
that must be applied on output data in specified order

### **Auxilary config params**

**model_types** - (list of strings) you can restrict the model loading in
this pool only with specified model types

**debug** - (bool) it is in charge for web server debug mode, that returns detailed info when error is occurs.
It's useful in development process