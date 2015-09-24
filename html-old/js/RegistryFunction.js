$(document).ready(function(){

	themodel = [];
	checkRow = [];
	checkRow[0] = 1;
	modelinfo = [];
	theJSON = "";
	
  $('#table-simple').on('keyup','input', function(){
	var aclass = $(this).attr('class').split(" ");
	var rowNo = aclass[1];
	$.sycBigToSmall(rowNo);
	themodel = $.updateSmallModel();
	$.getJSON();
	});
	
  $('#table-simple').on('keypress', 'input[name="property"]', function(){
	var aclass = $(this).attr('class').split(" ");
	var rowNo = aclass[1];
	$.addSmallRow(checkRow,rowNo);
	$.addBigRow("table-advanced",checkRow,rowNo);
	checkRow[rowNo] = 1;
	});	
	
  $(document).on('click', '[name="button_save"]', function(){
	//final update before save
	var selected = $("#tabs").tabs('option', 'active');
	if (selected == 0) {
		themodel = $.updateSmallModel();			
	} else {
		themodel = $.updateBigModel();
	}
	$.getJSON();
	
	var name = jQuery.parseJSON(theJSON).model;
	//var model = jQuery.parseJSON(theJSON);
	// modelstring[name] = theJSON;
	$.saveToRepo(name, theJSON);
	});
	
})



// Synchronize Big table to Small table 
$.sycBigToSmall = function (rowNo) {
	var selectorNameS = ".entry-s." + rowNo + "[name='property']";
	var selectorUseS = ".entry-s." + rowNo + "[name='use']";
	var selectorNameB = ".entry." + rowNo + "[name='property']";
	var selectorUseB = ".entry." + rowNo + "[name='type_detail']";
	var selectorIntrB = ".entry." + rowNo + "[name='internal_name']";
	
	var a = $(selectorNameS).val();
	var b = $(selectorUseS).val();
	var c = $.getInternalName(a,rowNo);
	
	
	$(selectorNameB).val(a);
	$(selectorUseB).val(b);
	$(selectorIntrB).val(c);		
}

// Save model string to Repo
$.saveToRepo = function (name, theJSON) {
	var queryToProcess = "http://...";
	attName = "att." + name;
	var newOne = {};
	newOne[attName] = theJSON;
	
		$.ajax({
	        url:queryToProcess,
	        type:"POST",
			data:newOne,
			username:"11156/repo",
			password:"1234",
	        success:$.onSaveComplete
	    });
}

$.onSaveComplete = function (data) {
	$("#dialog").html("");
	$("#dialog").html("Add Model Successfully");
	$("#dialog").dialog();
	$('#accordion').empty();		
	var queryToProcess = "http://...";
	$.ajax({
		url:queryToProcess,
		type:"GET",
		complete: $.toModels
	});
}


// Put property name into lower case and put it into internal name
$.getInternalName = function (aproperty,rowNo)
{	var thename = [];
	var intername = "";
	thename = aproperty.split(" ");
	intername = thename[0].toLowerCase();
	
	for(var i=1; i< thename.length ; i++) {
		intername += "_" + thename[i].toLowerCase();
	}
	
	return intername;
}


// Update small model string. Perform when keyup or selected
$.updateSmallModel = function ()
{	var model = [];
	$('.entry-s').each(function(){		
		var aclass = $(this).attr('class').split(" ");
		var rowNo = aclass[1];
		
		var prop = 	$('.'+ rowNo +'[name="property"]').val();
		var type = "";
		if (prop == "ID") {
			type = "handle";
		} else {
			type = "text";
		}
		
		var typeD = $('.'+ rowNo +'[name="use"]').val();
		
		var inter = $.getInternalName(prop,rowNo);
		
		
		var updates = { number: rowNo,
						property: $('.entry-s.'+ rowNo +'[name="property"]').val(), 
						type: type,
						"type-detail": $('.entry-s.'+ rowNo +'[name="use"]').val(),
						required: "yes",
						"max-occurences": "1",
						"internal-name": inter,
						"structural-parent": ""
						};
		
		if (rowNo >= model.length) {
			model.push(updates);
		} else {
			model[rowNo].number = rowNo;
			model[rowNo].property = prop;
			model[rowNo]["type"] = type;
			model[rowNo]["type-detail"] = typeD;
			model[rowNo].required = "yes";
			model[rowNo]["max-occurences"] = "1";
			model[rowNo]["internal-name"] = inter;
			model[rowNo]["structural-parent"] = "";
		}
	});
	return model;
}


// Add a row to small table when the row before has input
$.addSmallRow = function (checkRow,rowNo)
{
	var table = document.getElementById("table-simple");
	var rowCount = table.getElementsByTagName('tr').length;
	if (checkRow[rowNo] != 1) {
		var row = table.insertRow(rowCount);
		var colCount = table.rows[0].cells.length;
	    var newcell = row.insertCell(0);
	        newcell.innerHTML = rowCount-1;
		for(var i=1; i<colCount; i++) {
		var newcell = row.insertCell(i);
		if (i == 1) {
			newcell.innerHTML = ("<td><input type='text' class='entry-s " + (rowCount-1) 
			+ "' name='property'></input></td>");
		} else {	
			newcell.innerHTML = ("<td><input type='text' class='entry-s " + (rowCount-1) 
			+ "' name='use'></input></td>");
		}
		};
	};
}



$.toObjectString = function (obj)
{
	var result = "{";
	var counter = 0;
	$.each(obj, function (i,n)
	{
		if (counter > 0) { result += ",";}
		result += i.toString() + ":" + n.toString();
		counter++;
	});
	result += "}" ;
	return result;
}