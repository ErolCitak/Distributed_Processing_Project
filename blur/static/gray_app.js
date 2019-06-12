function AppViewModel() {
	// Declaration
this.yourName = ko.observable("");
this.numberOfClicks = ko.observable(0);
this.current_number = ko.observable(0);

this.incrementClickCounter = function() {
	// read value
    var previousCount = this.numberOfClicks();
	// assign value
    this.numberOfClicks(previousCount + 1);
	
	}

this.result = ko.computed(function(){


		if(typeof(this.yourName()) !== "number" )
		{

			current_number = Number(this.yourName());

			return current_number + 10
		}

		else{
			return 0
		}	

	},this);


this.fileData = ko.observable({
    dataURL: ko.observable(),
    // base64String: ko.observable(),
  });

this.onClear = function(fileData){
    if(confirm('Are you sure?')){
      fileData.clear && fileData.clear();
    }                            
  };

}

// Activates knockout.js
ko.applyBindings(new AppViewModel());
