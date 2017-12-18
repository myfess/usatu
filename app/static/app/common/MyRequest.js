function MyRequest(url, post, handler)
{
	this.req = null;
	this.url = url;
	this.post = post;
	this.handler = handler;
}



MyRequest.prototype.Execute = function()
{
	if(window.XMLHttpRequest)
	{
		this.req = new XMLHttpRequest();
        }
        else if(window.ActiveXObject)
        {
        	this.req = new ActiveXObject("Microsoft.XMLHTTP");
        }

       	if(this.req)
	{
        	var loader = this;
        	this.req.onreadystatechange = function()
        	{
			var READY_STATE_UNINITIALIZED = 0;
			var READY_STATE_LOADING = 1;
			var READY_STATE_LOADED = 2;
			var READY_STATE_INTERACTIVE = 3;
			var READY_STATE_COMPLETE = 4;

	
			var ready = loader.req.readyState;
			var data = null;

			if(ready == READY_STATE_COMPLETE)
			{
				data = loader.req.responseText;
				loader.handler(data);
        		}
        	}

        	this.req.open("POST", this.url, true);
        	this.req.send(this.post);
        }	
}
