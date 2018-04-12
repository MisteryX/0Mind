# Filters
It's used for data preprocessing and postprocessing with help of classical
algorithms and programming languages. So filters are kind of adapters between
our computers and neural networks.

To use filter you should specify it's full name in the model_pool task which
can be added dynamicaly (using [/model/load](API_REQUESTS.MD#model-load) action)
or staticaly (using [configuration file](CONFIGURATION.MD)). If no output filters
specified for current model, than **o_default.DefaultFilter** will be used.

Filters can be divided into groups: input filters, output filters and both.
0Mind filters are stored in **ML/filters** project directory.
All filters should be inherited from **base_filter.BaseFilter** abstract class and
must implement all of it's abstract methods.