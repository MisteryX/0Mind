# Framework adapters
They are used for standartization of any machine learning framework's functionality.
All adapters of 0Mind are stored in **ML/adapters** project directory and everyone
should be inherited from **base_model.BaseModel** class.
To add support of any ML framework should be enough to realize new adapter and append **ML/model_factory.ModelFactory.__file_extension_to_model_map** dictionary.

If target ML framework doesn't have enough functionality for typical 0Mind usage,
you should implement it using extra files in model archive and adapter methods.
In this case you should inherit new adapter class from **base_incomplete_model.BaseIncompleteModel**.

For example see *caffe2_model* or *sklearn_model* and read article about [ML_FRAMEWORKS](ML_FRAMEWORKS.MD).