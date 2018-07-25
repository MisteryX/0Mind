# Quick start guide

## 1. Install 0Mind
[Installation of 0Mind](INSTALLATION.MD)

## 2. Configure 0Mind

Change default [configuration](CONFIGURATION.MD) file **configs/model_pool_config.json**
and specify real location of your prepared model for example:
```
{
    "id": 1,
    "host": "127.0.0.1",
    "port": 5885,
    "tasks": [
        {
            "id": 1,
            "model_type": "caffe2",
            "model_file": "ML/models/init_net.pb",
            "predict_net.pb": "ML/models/predict_net.pb", 
            "inputs": [{"name": "data", "type": "uint8", "shape": [1, 3, 224, 224]}], 
            "outputs": [{"name": "default", "type": "float64", "shape": [1, 1000]}],
            "input_filters": {
                "data": ["i_img_file_to_caffe2.ImageFileCaffe2Filter"]
            },
            "output_filters": {
                "default": ["io_argmax.ArgMaxFilter"]
            }
        }
    ]
}

```

## 3. Run 0Mind skill server
```
python3 model_pool.py
```

## 4. Get prediction from 0Mind
```
curl -d '{"data": [{"image_file": "samples/flower.jpg"}]}' -H "Content-Type:application/json" -X POST http://127.0.0.1:5885/model/predict?id=1

```
Result should be something like this
```
{"result": {"default": 985}, "model_time": 0.9423518180847168}
```
