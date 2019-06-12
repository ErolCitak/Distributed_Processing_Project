function ViewModel() {
    var self = this;     
    this.files=  ko.observableArray([]);
    this.imageExists = ko.observable(false);
    this.imageSave = ko.observable(true);

	this.yourName = ko.observable("erol");
    this.yourSurname = ko.observable("çıtak");
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


    this.gray_convert = function() {
    // remove latest image in array
    $.ajax({
            url: '/gray_convert',
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

    this.get_gray_convert = function() {
    // get grayscale image
    $.ajax({
            url: '/get_gray_convert',
            type: 'GET',
            contentType: false,
            processData: false,

            success: function(data) {
                alert("Getting Gray is OK")
                self.imageExists(true);
                self.imageSave(true);

            },
            error: function() {
                alert("Getting Gray is NOT OK")
                self.imageExists(true);
                self.imageSave(false);

            }
        })
    
    }

//////////////////////////////////////////////////////////////////////////////////

this.sharp = function() {
    // remove latest image in array
    $.ajax({
            url: '/sharp',
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

    this.get_sharp_convert = function() {
    // get sharpening image
    $.ajax({
            url: '/get_sharp_convert',
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

this.blur = function() {
    // remove latest image in array
    $.ajax({
            url: '/blur',
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

    this.get_blur_convert = function() {
    // get blur image
    $.ajax({
            url: '/get_blur_convert',
            type: 'GET',
            contentType: false,
            processData: false,

            success: function(data) {
                alert("Getting Blur is OK")
                self.imageExists(true);
                self.imageSave(true);

            },
            error: function() {
                alert("Getting Blur is NOT OK")
                self.imageExists(true);
                self.imageSave(false);

            }
        })
    
    }

//////////////////////////////////////////////////////////////////////////////////

this.edge = function() {
    // remove latest image in array
    $.ajax({
            url: '/edge',
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

    this.get_edge_convert = function() {
    // get edge image
    $.ajax({
            url: '/get_edge_convert',
            type: 'GET',
            contentType: false,
            processData: false,

            success: function(data) {
                alert("Getting Edge is OK")
                self.imageExists(true);
                self.imageSave(true);

            },
            error: function() {
                alert("Getting Edge is NOT OK")
                self.imageExists(true);
                self.imageSave(false);

            }
        })
    
    }

//////////////////////////////////////////////////////////////////////////////////

this.saliency = function() {
    // remove latest image in array
    $.ajax({
            url: '/saliency',
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

    this.get_saliency_convert = function() {
    // get saliency image
    $.ajax({
            url: '/get_saliency_convert',
            type: 'GET',
            contentType: false,
            processData: false,

            success: function(data) {
                alert("Getting saliency is OK")
                self.imageExists(true);
                self.imageSave(true);

            },
            error: function() {
                alert("Getting saliency is NOT OK")
                self.imageExists(true);
                self.imageSave(false);

            }
        })
    
    }



//////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////

	this.saveInfo = function(formElement){

	    var inf = ko.toJSON({"yourName":this.yourName, "yourSurname":this.yourSurname});
        alert(inf);



		$.ajax({
            url: '/uploader_app',
            contentType: "application/json",
            type: 'POST',
            //data: JSON.stringify({"yourName":"Erol", "yourSurname" : "Çıtlak"}),
            data: inf,
            success: function(data) {
                alert("Success!..")
            },
            error: function() {
                alert("Failed!..")
            }
	    })
	}
 
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

