# Request handlers

They are used for processing API requests from users. If you want to add some new
actions in the 0Mind API, you should implement a new request handler.
0Mind based on tornado web server functionality and implements it's handler system.
All of the request handlers in 0Mind are stored in **request_handlers** directory grouped by their speciality.

Your custom request handler should be inherited from one of these classes:
* components/base_handler.BaseHandler
* components/model_handler.ModelHandler
* tornado.web.RequestHandler (if it's so specific)

After implementation of the request handler you should attach it to your server's
application. For 0Mind see file *model_pool.py:_init_service()* method.

**Attention!** For best back compatibility don't change existing request handlers's
HTTP/JSON interface.
For example: you can add optionaly params but don't change the names and amount of obligatory.
Just the same can be said about HTTP headers.
