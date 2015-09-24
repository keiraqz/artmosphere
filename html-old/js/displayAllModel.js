$(document).ready(function(){
  allModel = {};
	currentOldModel = "";
	typeName = "";
	called = 1;
	
  $(document).on('click', '[name="button_add"]', function(){
	$('#accordion').empty();		
	var queryToProcess = "http://...";
	$.ajax({
		url:queryToProcess,
		type:"GET",
		complete: $.toModels
	});
  });


	$(document).on('click', '#accordion', function() {
		if ($("#accordion").accordion("option","active") !== false) {
			var active = $("#accordion").accordion("option","active");
			var theModelName = $("#accordion h3").eq(active).text().split(" ");
			currentOldModel = theModelName[1];
			typeName = currentOldModel.replace('-', ' ');
			
			var editButton = "[name='" + currentOldModel + "_edit']";
			var saveButton = "[name='" + currentOldModel + "_save']";
			var cancelButton = "[name='" + currentOldModel + "_cancel']";
			
			$("#accordion").on('click', editButton, function () {
				$("#" + currentOldModel + "-advanced :input").attr("disabled", false);
				$("#" + currentOldModel + "-advanced[name='model"+ currentOldModel +"']").attr("disabled", true);
				$(editButton).prop("hidden",true);
				$(saveButton).prop("hidden",false);
				$(cancelButton).prop("hidden",false);								
			});
			
			$("#accordion").on('click', cancelButton, function () {
				var tableString = "<table id='" + currentOldModel + "-advanced' align='center' width='1050'><tr><th>Number</th><th>Property</th><th>Type</th><th>Type-Details</th><th>Required</th><th>Max. Occurrences</th><th>Internal Name</th><th>Structural Parent</th></tr></table><br><br>";
				var designstring = jQuery.parseJSON(allModel[currentOldModel].toString());	
				var properties = designstring.properties;
				var numAtt = properties.length;
				$("#model-" + currentOldModel).html("");
				$.toTableFunction(currentOldModel, tableString, properties, numAtt);

				// Disable all input
				$("#" + currentOldModel + "-advanced :input").attr("disabled", true);
				$(editButton).prop("hidden",false);
				$(saveButton).prop("hidden",true);
				$(cancelButton).prop("hidden",true);	
			});
			
			// Keypress add row
			tableSelector = currentOldModel + "-advanced";
			checkRowToo = [];
			var designstring = jQuery.parseJSON(allModel[currentOldModel].toString());				
			var numAtt = designstring.properties.length;

			for (var rowCount = 0; rowCount < numAtt; rowCount++) {
			checkRowToo[rowCount] = 1;
			}
			
			$("#" + tableSelector).on('keyup', 'input[name="property"]', function(){
			var aclass = $(this).attr('class').split(" ");
			var rowNo = aclass[2];
			themodel = $.updateOldModel();
			$.addBigRow(tableSelector,checkRowToo,rowNo);
			checkRowToo[rowNo] = 1;
			$.getJSON();
			});
			
			// Selection Change
			$("#" + tableSelector).on('change', 'select', function () {
			var aclass = $(this).attr('class').split(" ");
			var rowNo = aclass[2];
			themodel = $.updateOldModel();
			$.getJSON();
			});
						
			$("#accordion").on('click', saveButton, function () {
				$("#" + currentOldModel + "-advanced :input").attr("disabled", false);
				$("#" + currentOldModel + "-advanced[name='model"+ currentOldModel +"']").attr("disabled", true);
				
				var queryToProcess = "http://...";
				attName = "att." + currentOldModel;
				var updateOne = {};
				themodel = $.updateOldModel();
				
				var modeltemp = [];
				for (i=0; i<(themodel.length-1); i++) {
					modeltemp[i] = themodel[i]
				}
				modelinfo = {
					model: currentOldModel,
					properties: modeltemp		
				};
				theJSON = JSON.stringify(modelinfo);
				updateOne[attName] = theJSON;

					$.ajax({
				        url:queryToProcess,
				        type:"POST",
						data:updateOne,
						username:"11156/repo",
						password:"1234",
				        success:function () {
							called = 0;
							allModel = {};
							var queryToProcess = "http://...";
							if (called == 0) {
							$.ajax({
								url:queryToProcess,
								type:"GET",
								complete: $.onUpdateComplete
							});
							}
						}
					});	
			});
		}
	});	
})

$.onUpdateComplete = function (data) {
	//$('#accordion').html("");
	$.getAllModels(data);
	
	var designstring = jQuery.parseJSON(allModel[currentOldModel].toString());	
	var properties = designstring.properties;
	$.each(properties, function () {
		var self = this;
		$.toTableRow(self, currentOldModel);
	});
		
	var editButton = "[name='" + currentOldModel + "_edit']";
	var saveButton = "[name='" + currentOldModel + "_save']";
	var cancelButton = "[name='" + currentOldModel + "_cancel']";

	$("#" + currentOldModel + "-advanced :input").attr("disabled", true);
	$(editButton).prop("hidden",false);
	$(saveButton).prop("hidden",true);
	$(cancelButton).prop("hidden",true);
	called = 1;

}


$.toModels = function (data) {
	$.getAllModels(data);
	
	$.each(allModel, function () {
		var self = this;
		designstring = jQuery.parseJSON(self.toString());		
		$.toTable(designstring);
	});
	
	$( "#accordion" ).accordion("refresh");
}

$.getAllModels = function (data) {
	var respXML = $(data.responseText).find("att");
	var name="";
	var value="";
	var i=1;
	$.each(respXML, function () {
		if (i > 2) {
		var self = this;
		var childNode = $.parseXML(self.outerHTML).childNodes[0];
		name = childNode.getAttribute("name");
		value = childNode.getAttribute("value");
		allModel[name]=value;
		}
		i++;
	});
}

$.toTable = function (designstring) {
	var modelName = designstring.model;
	modelName = modelName.replace(/\s+/g, '-');
	var tableString = "<table id='" + modelName + "-advanced' align='center' width='1050'><tr><th>Number</th><th>Property*</th><th>Type</th><th>Type-Details</th><th>Required</th><th>Max. Occurrences</th><th>Internal Name</th><th>Structural Parent</th></tr></table><br><br>";
	var properties = designstring.properties;
	var numAtt = properties.length;
	
	$("#accordion").append("<h3 id='"+ modelName +"'>Model "+modelName+"</h3><div id='model-" + modelName + "'></div>");
	
	$.toTableFunction(modelName, tableString, properties, numAtt);

}

$.toTableFunction = function (modelName, tableString, properties, numAtt) {
	$("#model-" + modelName ).html("<fieldset><legend>Model "+ modelName +"</legend><div><p style='text-align: center;'><font size='2'>Model for <input type='text' name='model" 
	+ modelName + "' value='" + modelName + "' disabled></font></p></div><br><div>" + tableString + "</div><div style='text-align: right;'><button id='button' name='" 
	+ modelName + "_save' hidden>Save Model</button><button id='button' name='" 
	+ modelName + "_edit'>Edit Model</button><button id='button' name='" 
	+ modelName + "_cancel' hidden>Cancel</button><button id='button' name='" 
	+ modelName + "_delete'>Delete Model</button></div></fieldset>");
	
	
	var table = document.getElementById(modelName + "-advanced");
	
	for (var rowCount = 1; rowCount <= numAtt + 1; rowCount++) {
		var row = table.insertRow(rowCount);
		var colCount = 8;
	    var newcell = row.insertCell(0);
	        newcell.innerHTML = rowCount-1;
		for(var i=1; i<colCount; i++) {
		var newcell = row.insertCell(i);
		if (i == 1) {
				newcell.innerHTML = ("<td><input type='text' class='" + modelName +" entry-old " + (rowCount-1) 
				+ "' name='property'></input></td>");
			} else if (i == 2) {	
				newcell.innerHTML = ("<td><select class='" + modelName +" entry-old " + (rowCount-1) 
				+ "' name='type'><option value='text'>Text</option><option value='handle'>Handle</option><option value='handle_reference'>Handle-Reference</option><option value='blank'>Blank</option><option value='controlled'>Controlled</option><option value='datetime'>DateTime</option><option value='number'>Number</option></select></td>");
			} else if (i == 3) {	
				newcell.innerHTML = ("<td>Specify char. bound here: <input type='text' class='" + modelName +" entry-old " + (rowCount-1) +"' name='type_detail' value='Unbounded'></input></td>");
			} else if (i == 4) {	
				newcell.innerHTML = ("<td><select class='" + modelName +" entry-old " + (rowCount-1) 
				+ "' name='required'><option value='yes'>Yes</option><option value='no'>No</option></select></td>");
			} else if (i == 5) {	
				newcell.innerHTML = ("<td><input type='text' class='" + modelName +" entry-old " + (rowCount-1) 
				+ "' name='max_occ' value='1'></input></td>");
			} else if (i == 6) {	
				newcell.innerHTML = ("<td><input type='text' class='" + modelName +" entry-old " + (rowCount-1) 
				+ "' name='internal_name' value=''></input></td>");
			} 	else {	
				newcell.innerHTML = ("<td><input type='text' class='" + modelName +" entry-old " + (rowCount-1) 
				+ "' name='structure'></input></td>");
			}
		};
	}
	
	
	
	$.each(properties, function () {
		var self = this;
		$.toTableRow(self, modelName);
	});
		
	// Disable all input
	$("#" + modelName + "-advanced :input").attr("disabled", true);
}

$.toTableRow = function (oneProperty, modelName) {
	var rowSelector = oneProperty.number;
	$("." + modelName + ".entry-old." + rowSelector + "[name='property']").val(oneProperty.property);
	$("." + modelName + ".entry-old." + rowSelector + "[name='type'] option[value='"+ oneProperty["type"] +"']" ).prop('selected', true);
	$("." + modelName + ".entry-old." + rowSelector + "[name='required'] option[value='"+ oneProperty.required +"']").prop('selected', true);
	$("." + modelName + ".entry-old." + rowSelector + "[name='max_occ']").val(oneProperty["max-occurences"]);
	$("." + modelName + ".entry-old." + rowSelector + "[name='internal_name']").val(oneProperty["internal-name"]);
	$("." + modelName + ".entry-old." + rowSelector + "[name='structure']").val(oneProperty["structural-parents"]);
	
	if (oneProperty["type"] == "handle") {
		var inHtml = "<input type='text' class='" + modelName +" entry-old " + rowSelector + "' name='type_detail' value='Prefix' disabled>/</input><select class='" + modelName +" entry-old " + rowSelector + "' name='type_detail'><option value='random'>Random</option><option value='property'>Property</option><option value='hash_property'>Hash of a Property</option></select><input name='suffix_property' class='" + modelName +" entry-old " + rowSelector + "' value='specify property # here' disabled></input>";
		$("." + modelName + ".entry-old." + rowSelector + "[name='type_detail']").parent().html(inHtml);
	} else if (oneProperty["type"] == "text") {
		$("." + modelName + ".entry-old." + rowSelector + "[name='type_detail']").val(oneProperty["type-detail"]);
	} else {
		var inHtml = "<input type='text' class='" + modelName +" entry-old " + rowSelector + "' name='type_detail'></input>";
		$("." + modelName + ".entry-old." + rowSelector + "[name='type_detail']").parent().html(inHtml);
		$("." + modelName + ".entry-old." + rowSelector + "[name='type_detail']").val(oneProperty["type-detail"]);
	}
}


$.updateOldModel = function ()
{	var model = [];
	$('.'+ currentOldModel +'.entry-old').each(function(){		
		var aclass = $(this).attr('class').split(" ");
		var rowNo = aclass[2];
		var prop = $('.'+ currentOldModel +'.entry-old.'+ rowNo +'[name="property"]').val();
		var typ = $('.'+ currentOldModel +'.entry-old.'+ rowNo +'[name="type"]').val();
		var typeD;
		
		if (typ == "handle") {
			var typeDetailSelect = $('select.'+ currentOldModel + '.entry-old.'+ rowNo +'[name="type_detail"]').val();
			if (typeDetailSelect == "random") {
				typeD = $('input.'+ currentOldModel + '.entry-old.'+ rowNo +'[name="type_detail"]').val() 
				+ "/" + $('select.'+ currentOldModel + '.entry-old.'+ rowNo +'[name="type_detail"]').val();				
			} else {
				typeD = $('input.'+ currentOldModel + '.entry-old.'+ rowNo +'[name="type_detail"]').val() 
				+ "/" + $('input.'+ currentOldModel + '.entry-old.'+ rowNo + '[name="suffix_property"]').val();
			}
		} else {
			typeD = $('.'+ currentOldModel +'.entry-old.'+ rowNo +'[name="type_detail"]').val();
		}
		
		var req = $('.'+ currentOldModel +'.entry-old.'+ rowNo +'[name="required"]').val();
		var maxo = $('.'+ currentOldModel +'.entry-old.'+ rowNo +'[name="max_occ"]').val();
		var inter = $('.'+ currentOldModel +'.entry-old.'+ rowNo +'[name="internal_name"]').val();
		var strct = $('.'+ currentOldModel +'.entry-old.'+ rowNo +'[name="structure"]').val();
			
		var updates = { number: rowNo,
						property: prop, 
						type: typ,
						"type-detail": typeD ,
						required: req,
						"max-occurences": maxo,
						"internal-name": inter,
						"structural-parent": strct 
						};
		
		if (rowNo >= model.length) {
			model.push(updates);
		} else {
			model[rowNo].number = rowNo;
			model[rowNo].property = prop;
			model[rowNo]["type"] = typ;
			model[rowNo]["type-detail"] = typeD;
			model[rowNo].required = req;
			model[rowNo]["max-occurences"] = maxo;
			model[rowNo]["internal-name"] = inter;
			model[rowNo]["structural-parent"] = strct;
		}
	});

	return model;
}

