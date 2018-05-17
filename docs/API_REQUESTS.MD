# 0Mind API

This REST API based on HTTP protocol with JSON data container.

$HOST - configuration variable "host"

$PORT - configuration variable "port"

Available HTTP actions are:

1. [http://$HOST:$PORT/info](#info)
1. [http://$HOST:$PORT/info/system](#info-system)
1. [http://$HOST:$PORT/model/list](#model-list)
1. [http://$HOST:$PORT/model/info](#model-info)
1. [http://$HOST:$PORT/model/load](#model-load)
1. [http://$HOST:$PORT/model/drop](#model-drop)
1. [http://$HOST:$PORT/model/predict](#model-predict)
1. [http://$HOST:$PORT/command/stop](#command-stop)

## INFO
URL: http://$HOST:$PORT/info

METHODS: GET, POST

HEADERS: None

PARAMS: None

RESULT: Returns core information about 0Mind skill server instance,
for example
```
curl http://127.0.0.1:5885/info

{"service": "ModelPool", "id": 1, "options": {"model_types": ["keras"], "debug": false}}
```

## INFO-SYSTEM
URL: http://$HOST:$PORT/info/system

METHODS: GET, POST

HEADERS: None

PARAMS: None

RESULT: Returns system information about 0Mind skill server's environment, for example
```
curl http://127.0.0.1:5885/info/system

{"id": 1, "cpu_usage": 1.3, "memory": {"total": 8271306752, "available": 2798899200, "percent": 66.2, "used": 4734496768, "free": 1093509120, "active": 4851269632, "inactive": 1893675008, "buffers": 310255616, "cached": 2133045248, "shared": 426766336}, "python": [3, 6, 4, "final", 0]}
```

## MODEL-LIST
URL: http://$HOST:$PORT/model/list

METHODS: GET, POST

HEADERS: None | Content-Type: application/json

PARAMS: None | JSON:check_sum (string)

RESULT: Returns list of loaded models in this 0Mind instance, for example
```
curl http://127.0.0.1:5885/model/list

{"id": 1, "check_sum": "35dba5d75538a9bbe0b4da4422759a0e", "models": [1]}
```

## MODEL-INFO
URL: http://$HOST:$PORT/model/info

METHODS: GET, POST

HEADERS: None

PARAMS: HTTP:id (integer)

RESULT: Returns model's information with specified identifier, for example
```
curl http://127.0.0.1:5885/model/info?id=1

{"inputs": {"0": {"name": "data", "type": "float32", "shape": [1, 3, 224, 224]}}, "outputs": {"0": {"name": "default", "type": "float32", "shape": [1, 1000]}}, "tool": "keras"}
```

## MODEL-LOAD
URL: http://$HOST:$PORT/model/load

METHODS: POST

HEADERS: Content-Type: application/json

PARAMS: JSON:(id, model_file, model_type, input_filters, output_filters)

RESULT: Loads model into the pool. Returns model's loading statistics or error if fails, for example
```
curl -d '{"id": 2, "output_filters": {}, "model_file": "ML/models/bvlc_googlenet.keras", "input_filters": {"data": ["i_img_file_to_caffe2.ImageFileCaffe2Filter"]}, "model_type": "keras"}' -H "Content-Type:application/json" -X POST http://127.0.0.1:5885/model/load

{"result": true, "load_time": 0.910876989364624, "memory_consumed": 84680704, "model_id": 2}
```

## MODEL-DROP
URL: http://$HOST:$PORT/model/drop

METHODS: GET, POST

HEADERS: None

PARAMS: HTTP:id (integer)

RESULT: Loads model into the pool. Returns model's loading statistics or error if fails, for example
```
curl http://127.0.0.1:5885/model/drop?id=2

{"result": true, "unload_time": 0.003221750259399414, "memory_released": 69054464, "model_id": 2}
```

## MODEL-PREDICT
URL: http://$HOST:$PORT/model/predict

METHODS: POST

HEADERS: Content-Type: application/json

PARAMS: HTTP:id (integer), JSON:object

RESULT: Model inference result with applied filters. Input JSON data depends on the model's interface and input filters.
JSON data should be dictionary with model's inputs names as keys and values formatted according to the interface of the model or input filter.
Example:
```
curl -d '{"data": [{"image_file": "samples/flower.jpg"}]}' -H "Content-Type:application/json" -X POST http://127.0.0.1:5885/model/predict?id=1

{"result": {"default": 985}, "model_time": 0.9423518180847168}
```
We got prediction from model with id=1, input name "data" and output name "default". This model has input filter "data": \["i_img_file_to_caffe2.ImageFileCaffe2Filter"\],
so we specify batch data as {"image_file": "samples/flower.jpg"} for using filter, that transforms picture on disk to normalized and scaled tensor.
Result of the model inference is the dictionary with model output names as keys and values formatted according to model's output or output filter interface.
This model has output filter "default": \["io_argmax.ArgMaxFilter"\], so we got filter output - image class identifier.

## COMMAND-STOP
URL: http://$HOST:$PORT/command/stop

METHODS: POST

HEADERS: Content-Type: application/json

PARAMS: JSON:pool_id

RESULT: Stops the 0Mind skill server instance and releases all resourses. 0Mind instance can't be resumed.
```
curl -d '{"pool_id": 1}' -H "Content-Type:application/json" -X POST http://127.0.0.1:5885/command/stop

{"result": "accepted", "id": 1}
```