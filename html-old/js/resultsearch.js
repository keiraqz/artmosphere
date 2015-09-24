$(document).ready(function(){
	//Hard Coded
		// Model book:
	// designstring = '{"model":"Book","properties":[{"number":0,"property":"ID","type":"handle","type-detail":"Prefix/Random","required":"Yes","max-occurences":1,"internal-name":"id"},{"number":1,"property":"Title","type":"Text","type-detail":"250 characters","required":"Yes","max-occurences":1,"internal-name":"title"},{"number":2,"property":"Genre","type":"controlled","type-detail":"Fictional, Non-fictional","required":"Yes","max-occurences":1,"internal-name":"genre"},{"number":3,"property":"Media","type":"controlled","type-detail":"Printed, Audio, e-book","required":"Yes","max-occurences":1,"internal-name":"media"},{"number":4,"property":"Author","type":"Blank","required":"No","max-occurences":2,"internal-name":"author"}]}';
	// aresult = '{"total-matches":9, "page":1, "per-page":4, "records":[{"ID":"Prefix/123","Title":"book1","Genre":"Fictional", "Media":"Printed","Author":"author1"},{"ID":"Prefix/234","Title":"book2","Genre":"Fictional", "Media":"Printed","Author":"author2"},{"ID":"Prefix/567","Title":"book3","Genre":"Fictional", "Media":"Printed,Audio","Author":"author3"},{"ID":"Prefix/444","Title":"book4","Genre":"Fictional", "Media":"Printed","Author":"author4"},{"ID":"Prefix/555","Title":"book5","Genre":"Fictional", "Media":"Printed","Author":"author5"},{"ID":"Prefix/666","Title":"book6","Genre":"Fictional", "Media":"Printed","Author":"author6"},{"ID":"Prefix/777","Title":"book7","Genre":"Fictional", "Media":"Printed","Author":"author7"},{"ID":"Prefix/888","Title":"book8","Genre":"Fictional", "Media":"Printed","Author":"author8"},{"ID":"Prefix/999","Title":"book9","Genre":"Fictional", "Media":"Printed","Author":"author9"}]}';	

		// Model Movie:
	// designstring = '{"model":"Movie","properties":[{"number":0,"property":"ID","type":"handle","type-detail":"Prefix/Random","required":"Yes","max-occurences":1,"internal-name":"id"},{"number":1,"property":"Title","type":"Text","type-detail":"250 characters","required":"Yes","max-occurences":1,"internal-name":"title"},{"number":2,"property":"Genre","type":"controlled","type-detail":"Action, Fiction, Document","required":"Yes","max-occurences":1,"internal-name":"genre"},{"number":3,"property":"Media","type":"controlled","type-detail":"DVD, online","required":"Yes","max-occurences":1,"internal-name":"media"},{"number":4,"property":"Author","type":"Blank","required":"No","max-occurences":2,"internal-name":"author"},{"number":5,"property":"Year","type":"controlled","type-detail":"1998,1999,2000,2001","required":"Yes","max-occurences":1,"internal-name":"year"}]}';
	records = [];
	result = {};
	theModelHandle = [];
	requestSent = false;
	
	$('#resultbox').on('click','a', function() {
		var self = this;
		theModelHandle = self.text;
		$('#resultbox').prop("hidden", true);
		$('#onerecord').prop("hidden", false);
		$.toDisplay(theModelHandle);
		
		$('#onerecord').on('click','.edit', function() {
			$('.edit').prop("hidden", true);
			$('.update').prop("hidden", false);
			$('.cancel').prop("hidden", false);
			$('.save').prop("hidden", true);
			var selected = $("select#modelselection option:selected").val()	
		 	var	selectdesign = modelstring[selected];
			design = jQuery.parseJSON(selectdesign);
			$.enableAll(theModelHandle);
		});


		$('#onerecord').on('click','.update', function() {
			$('.edit').prop("hidden", false);
			$('.update').prop("hidden", true);
			$('.cancel').prop("hidden", true);
			$('.save').prop("hidden", true);
			$.updateModel();
		});

		$('#onerecord').on('click','.cancel', function() {
			$('.edit').prop("hidden", false);
			$('.update').prop("hidden", true);
			$('.cancel').prop("hidden", true);
			$('.save').prop("hidden", true);
			$.reperformSearch(theModelHandle);
		});
	});
	
	$('[name="go-back"]').on('click', function() {
		$('.edit').prop("hidden", false);
		$('.update').prop("hidden", true);
		$('.cancel').prop("hidden", true);
		$('.save').prop("hidden", true);
		$('#resultbox').prop("hidden", false);
		var selected = $("select#modelselection option:selected").val()	
	 	var	selectdesign = modelstring[selected];
		design = jQuery.parseJSON(selectdesign);
		$.loadPage(design);
		var queryToProcess = "http://...:8080/do?query=objatt_model:" + selected;
		$.performInitialSearch(queryToProcess);
		$('#onerecord').prop("hidden", true);
	});
	
	$('[name="create-new-rec"]').on('click', function() {
		$('#resultbox').prop("hidden", true);
		$('#onerecord').prop("hidden", false);
		$('.edit').prop("hidden", true);
		$('.update').prop("hidden", true);
		$('.cancel').prop("hidden", true);
		$('.save').prop("hidden", false);
		var selected = $("select#modelselection option:selected").val();	
		if (typeof selected === "undefined") {
			$("#dialog2").html("");
			$("#dialog2").html("Please select a model first");
			$("#dialog2").dialog();	
			$('#resultbox').prop("hidden", false);
			$('#onerecord').prop("hidden", true);
			$('.edit').prop("hidden", false);
			$('.update').prop("hidden", false);
			$('.cancel').prop("hidden", false);
			$('.save').prop("hidden", false);	
		} else {
			$.newModelForm();
		}
		
		$('#onerecord').on('click','.save', function() {
			if (!requestSent) {
			$('.edit').prop("hidden", false);
			$('.update').prop("hidden", true);
			$('.cancel').prop("hidden", true);
			$('.save').prop("hidden", true);
			$.createModel();
			}
		});
	});

})

$.toLoadResult = function (aresult) {
	records = [];
	result = {};
	result = jQuery.parseJSON(aresult);
	records = $.toType(result.records);	
	$.toPagination();
}


// Create a new model in the repository
$.createModel = function () {
	var newModel = {};
	var theNew = "";
	var theID = "";
	requestSent = true;
	$.each(design.properties, function () {
		var self = this;
		
		if (self["type"] == "controlled") {
			var controlString = "";
			var selector = "input[name='" + self.property + "Display']:checked";
			$(selector).each(function () {
				controlString += this.value + ",";						
			});			
			var num = controlString.length - 1;
			controlString = controlString.substring(0,num);
			newModel[self.property] = controlString;
		} else {
			newModel[self.property] = $("#" + self.property).val();
		}
	
	});

	theNew = JSON.stringify(newModel);
	
	var queryToProcess = "http://.../set/";
	
		$.ajax({
	        url:queryToProcess,
	        type:"POST",
			data:{ "att.model":design.model, "att.json":theNew, template:"test.html"},
			complete: function (data) {
				var theid = jQuery.parseJSON(data.responseText);
				theModelHandle = theid['id'];
				$.reperformSearch(theModelHandle);
				//alert("ID For Your New Record: " + theModelHandle);
				requestSent = false;
			}
	    });

}

$.updateModel = function () {
	var updateModel = {};
	var theUpdate = "";
	
	// Update the model
	$.each(design.properties, function () {
		var self = this;
		
		if (self.property != "ID") {
			if (self["type"] == "controlled") {
				var controlString = "";
				var selector = "input[name='" + self.property + "Display']:checked";
				$(selector).each(function () {
					controlString += this.value + ",";						
				});			
				var num = controlString.length - 1;
				controlString = controlString.substring(0,num);
				updateModel[self.property] = controlString;
			} else {
				updateModel[self.property] = $("#"+ self.property + "Display").val();
			}
		}
	});

	theUpdate = JSON.stringify(updateModel);
	
	var queryToProcess = "http://...:8080/set/" + theModelHandle;
	
		$.ajax({
	        url:queryToProcess,
	        type:"POST",
			data:{"att.json":theUpdate},
			complete: function () {
				$.reperformSearch(theModelHandle);
			}
	    });
}


$.newModelForm = function () {
	$('#therecord').html("");
	var theTable = "";
	
	theTable += "<br><br><table id='newForm'>"; 
	$.each(design.properties, function () {
		var self = this;
	if (self.property != "ID") {
		if (self.required == "Yes") {
				theTable += "<tr><td>" + self.property + "*</td>";
			} else {
				theTable += "<tr><td>" + self.property + "</td>";			
			}
			
			if (self["type"] == "Text") {
				theTable += "<td><input id='" + self.property + "'></input>  (" + self["type-detail"] + ")</td></tr>";
			} else if (self["type"] == "controlled") {
				theTable += "<td>";
				var options = self["type-detail"].split(",");										
				$.each(options, function(){
					var thisoption = this; 
					theTable += "<input type='checkbox' name='" + self.property + "Display' value='" + thisoption +"'>" + thisoption +"</input>";						
				});
			} else if (self["type"] == "datetime") {
				theTable += "<td><input id='" + self.property + "'></input>  (mm/dd/yyyy)</td></tr>";
			} else {
				theTable += "<td><input id='" + self.property + "'></input></td></tr>";
			}	
		}	
	});
	theTable += "</table>";
	$('#therecord').html(theTable);
	
}



$.toPagination = function () {
	//empty page
	$('#therecord').html("");
	$('#result-summary').html("");
	$('#result-list').html("");
	$('#page-select').html("");
	
	var summary = result["total-matches"] + " Results Matched from y Records";	
	$('#result-summary').html("<p><i>" + summary + "</i></p>");	
	$.putToPage();	
	$('#result-list').children().css('display','none');	
    $('#page-select').pagination({
        items: result["total-matches"],
        itemsOnPage: result["per-page"],
        cssStyle: 'compact-theme'
    });
}


// Only for test purpose, update Hardcode Models
$.toUpdate = function (self) {
	$.each(records, function () {
		var inner = this;
		if (inner[0]["value"] == self) {
			$.each(inner, function () {
				var innerTwo = this;
				if (innerTwo.property != "ID") {
						if (innerTwo["type"] == "controlled") {
							var controlString = "";
							var selector = "input[name='" + innerTwo.property + "Display']:checked";
							$(selector).each(function () {
								controlString += this.value + ",";						
							});	
							var num = controlString.length - 1;
							controlString = controlString.substring(0,num);
							innerTwo["value"] = controlString;
						} else if (innerTwo["type"] == "handle") {
							innerTwo["value"] = $("#"+ innerTwo.property + "Display").text;
						} else {
							innerTwo["value"] = $("#"+ innerTwo.property + "Display").val();
						}
				}
			});
		}			
	});
}



$.enableAll = function (self) {
	$('#therecord').html("");
	$.each(records, function () {
		var inner = this;
		if (inner[0]["value"] == self) {
			var display = "<div><br>ID: " + self + "</div><br><div><table id=oneRecord>";
			
			$.each(inner, function () {
				var innerTwo = this;
				if (innerTwo.property != "ID") {
					if (innerTwo.required == "yes") {
						display += "<tr><td>" + innerTwo.property + "*</td><td>";
					} else {
						display += "<tr><td>" + innerTwo.property + "</td><td>";						
					}
										
					if (innerTwo["type"] == "handle") {
						display += "<a id='" + innerTwo.property + "Display' href=#>"+ innerTwo["value"] +"</a></td></tr>";
					} else if (innerTwo["type"] == "controlled") {						
						var options = innerTwo["type-detail"].split(",");							
						
						$.each(options, function(){
							var thisoption = this; 
							var init = 0;
							
							if (innerTwo["value"] != "undefined") {
							var selected = innerTwo["value"].split(",");
							$.each(selected, function () {
								if (this.trim().toString() == thisoption.trim().toString()) {init = 1;}
							});
							}	
								
							if (init == 1) {
								display += "<input type='checkbox' name='" + innerTwo.property + "Display' value='" + thisoption +"' checked>" + thisoption +"</input>";
							} else {
								display += "<input type='checkbox' name='" + innerTwo.property + "Display' value='" + thisoption +"'>" + thisoption +"</input>";
							}						
						});
						 
						display += "</td></tr>";
					} else if (innerTwo["type"] == "text") {
						display += "<input id='" + innerTwo.property + "Display' value='" + innerTwo["value"] +"'></input>" + innerTwo["type-detail"] + "</td></tr>";
					} else if (innerTwo["type"] == "datetime") {
						display += "<input id='" + innerTwo.property + "Display' value='" + innerTwo["value"] +"'></input>(mm/dd/yyyy)</td></tr>";
					} else {
						display += "<input id='" + innerTwo.property + "Display' value='" + innerTwo["value"] +"'></input></td></tr>";
					}
				}
			});
			display += "</table></div>";
			$("#therecord").html(display);
		}
	});
}


$.toDisplay = function (self) {	
		$('#therecord').html("");
		
		$.each(records, function () {
			var inner = this;
			if (inner[0]["value"] == self) {
				$.displayCurrent(inner, self);
			}
		});
}


// Display the model by current selected handle
$.displayCurrent = function (inner, self) {
	var display = "<div><br>ID: " + self + "</div><br><div><table id=oneRecord>";
	$.each(inner, function () {
		var innerTwo = this;
		if (innerTwo.property != "ID") {
			if (innerTwo["type"] == "handle") {
				display += "<tr><td>" + innerTwo.property + "</td><td><a id='" + innerTwo.property + "Display' href=#>"+ innerTwo["value"] +"</a></td></tr>";
			} else if (innerTwo["type"] == "controlled") {
			//	display += "<tr><td>" + innerTwo.property + "</td><td><select id='" + innerTwo.property + "Display' disabled>";
				display += "<tr><td>" + innerTwo.property + "</td><td>";
				
				var options = innerTwo["type-detail"].split(",");
											
				$.each(options, function(){
					var thisoption = this; 
					var init = 0;
					
					if (innerTwo["value"] != "undefined") {
					var selected = innerTwo["value"].split(",");
					$.each(selected, function () {
						if (this.trim().toString() == thisoption.trim().toString()) {init = 1;}});
					}	
						
					if (init == 1) {
						display += "<input type='checkbox' name='" + innerTwo.property + "Display' value='" + thisoption +"' checked disabled>" + thisoption +"</input>";
					} else {
						display += "<input type='checkbox' name='" + innerTwo.property + "Display' value='" + thisoption +"' disabled>" + thisoption +"</input>";
					}						
				});
				 
				display += "</td></tr>";
			} else {
				display += "<tr><td>" + this.property + "</td><td><input id='" + this.property + "Display' value='" + this["value"] +"' disabled></input></td></tr>";
			}
		}
	});
	display += "</table></div>";
	$("#therecord").html(display);
}


//Map a record to the selected type (unnessary once stored into repository)
$.toType = function (obj) 
{
	var allrecords = [];

	
	$.each(obj, function() 
	{
	var self = this;
	var thisModel = [];
	var oneModel = design;
	
		$.each(oneModel.properties, function () {
			var thisproperty = {};
			thisproperty.property = this.property;
			thisproperty["type"] = this["type"];
			thisproperty["type-detail"] = this["type-detail"];
			thisproperty.required = this.required;
			thisproperty["max-occurences"] = this["max-occurences"];
			thisproperty["structural-parent"] = this["structural-parent"];
						
			if (this.property in self) {
				thisproperty["value"] = self[this.property];
			} else {
				thisproperty["value"] = "undefined";
			}
			thisModel.push(thisproperty);
		});
		
		allrecords.push(thisModel);
	})

	return allrecords;
}


$.putToPage = function () 
{
	var perpage = result["per-page"];
	var count = 0;
	$.each(records, function()
	{
		var pagenumber = Math.floor( count / perpage + 1);
		$('#result-list').append("<br><div class='onentry page-" + pagenumber + "'>" + $.oneEntry(this) + "</div><br>");
		count++;
	});
	
}


$.oneEntry = function (obj) 
{
	var html = "";
	
	$.each(obj, function() {
		if (this["type"] == "handle") {
			html += "<div class='entry" + this.property.toLowerCase() +"'>" + this.property + ": <a href='#'>" + this["value"] + "</a></div>";	
		} else {
			html += "<div class='entry" + this.property.toLowerCase() +"'>" + this.property + ": " + this["value"] + "</div>";	
		}		
	});
	
	
	
	return html;
}