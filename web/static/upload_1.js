function ViewModel() {
    var self = this;     
    this.files=  ko.observableArray([]);
    this.imageExists = ko.observable(false);
    this.imageSave = ko.observable(true);
    this.media = ko.observableArray([]);

    this.fileSelect= function (elemet,event) {
        var files =  event.target.files;// FileList object

        // Loop through the FileList and render image files as thumbnails.
        for (var i = 0, f; f = files[i]; i++) {

          // Only process image files.
          if (!f.type.match('image.*')) {
            continue;
          }          

          var reader = new FileReader();

          // Closure to capture the file information.
          reader.onload = (function(theFile) {
              return function(e) {                             
                  self.files.push(new FileModel(escape(theFile.name),e.target.result));
              };                            
          })(f);
          // Read in the image file as a data URL.
          reader.readAsDataURL(f);
        }
    };

    this.removeImage = function() {
	// remove latest image in array
	$.ajax({
            url: '/image_delete',
            type: 'POST',
            contentType: false,
            processData: false,

            success: function(data) {
                alert(data["result"])
                self.imageExists(false);
                self.imageSave(true);

                self.media.removeAll();
            },
            error: function() {
                alert(data["result"])
                self.imageExists(true);
                self.imageSave(false);

            }
	    })
	}

//////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////


    this.text_detect = function() {
    // remove latest image in array
    $.ajax({
            url: '/text_detect',
            type: 'POST',
            contentType: false,
            processData: false,

            success: function(data) {
                alert(data["result"])
                self.imageExists(true);
                self.imageSave(true);

            },
            error: function() {
                alert(data["result"])
                self.imageExists(true);
                self.imageSave(false);

            }
        })
    }

    this.get_text_detect = function() {
    // get preprocessed image
    $.ajax({
            url: '/get_text_detect',
            type: 'GET',
            contentType: false,
            processData: false,

            success: function(data) {
                alert(data["result"])
                self.imageExists(true);
                self.imageSave(true);

            },
            error: function() {
                alert("Getting Preprocessing NOT OK")
                self.imageExists(true);
                self.imageSave(false);

            }
        })
    
    }

//////////////////////////////////////////////////////////////////////////////////

this.text_recognize = function() {
    // remove latest image in array
    $.ajax({
            url: '/text_recognize',
            type: 'POST',
            contentType: false,
            processData: false,

            success: function(data) {
                alert(data["result"])
                self.imageExists(true);
                self.imageSave(true);


            },
            error: function() {
                alert(data["result"])
                self.imageExists(true);
                self.imageSave(false);

            }
        })
    }

    this.get_text_recognize = function() {
    // get sharpening image
    $.ajax({
            url: '/get_text_recognize',
            type: 'GET',
            contentType: false,
            processData: false,

            success: function(data) {
                alert("Getting Sharp is OK")
                self.imageExists(true);
                self.imageSave(true);

            },
            error: function() {
                alert("Getting Sharp is NOT OK")
                self.imageExists(true);
                self.imageSave(false);

            }
        })
    
    }

//////////////////////////////////////////////////////////////////////////////////

this.text_preprocess = function() {
    // remove latest image in array
    $.ajax({
            url: '/text_preprocess',
            type: 'POST',
            contentType: false,
            processData: false,

            success: function(data) {
                alert(data["result"])
                self.imageExists(true);
                self.imageSave(true);


            },
            error: function() {
                alert(data["result"])
                self.imageExists(true);
                self.imageSave(false);

            }
        })
    }

    this.get_text_preprocess = function() {
    // get edge image
    $.ajax({
            url: '/get_text_preprocess',
            type: 'GET',
            contentType: false,
            processData: false,

            success: function(data) {
                alert(data["result"])
                self.imageExists(true);
                self.imageSave(true);

            },
            error: function() {
                alert(data["result"])
                self.imageExists(true);
                self.imageSave(false);

            }
        })
    
    }


//////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////// 
	this.saveImage = function() {

		var formData = new FormData();

		jQuery.each(jQuery('#imageUpload')[0].files, function(i,file)
		{
		    formData.append('file',file)
		});

		$.ajax({
            url: '/image_app',
            type: 'POST',
            contentType: false,
            data: formData,
            processData: false,

            success: function(data) {
                alert(data["result"])
                self.imageExists(true);
                self.imageSave(false);

                base = "static/image/"
                self.media.push({media_url: base.concat(data["filename"])});
            },
            error: function() {
                alert("yokh yaa")
                alert(data["result"])
                self.imageExists(false);
                self.imageSave(true);
            }
	    })


		
	};
};

var FileModel= function (name, src) {
    var self = this;
    this.name = name;
    this.src= src ;
};

ko.applyBindings(new ViewModel());

