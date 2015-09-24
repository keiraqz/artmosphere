$(document).ready(function(){

	themodel = [];
	modelinfo = [];
	

// Change Internal Name of every "property" input	
  $("#table-advanced").on('keyup', '[name="property"]', function(){
	var aproperty = $(this).val();
	var aclass = $(this).attr('class').split(" ");
	var rowNo = aclass[1];
	$.changeInternalName(aproperty,rowNo);
	});

// Update type-detailes with Type change	
  $("#table-advanced").on('change', 'select[name="type"]', function () {
	var aclass = $(this).attr('class').split(" ");
	var rowNo = aclass[1];	
	var thisType = $(this).val();

	if (thisType == "handle") {
		$(".entry." + rowNo + "[name='type_detail']").parent().html("<input type='text' class='entry " 
		+ rowNo +"' name='type_detail' value='Prefix' disabled></input>/<select id='suffix' class='entry " 
		+ rowNo +"' name='type_detail'><option value='random'>Random</option><option value='property'>Property</option><option value='hash_property'>Hash of a Property</option></select><input name='suffix_property' class='entry "+ rowNo +"' value='specify property # here' disabled></input>");		
	} else if (thisType == "datetime") { 
		$(".entry." + rowNo + "[name='type_detail']").parent().html("<input type='text' class='entry " + rowNo +"' name='type_detail' id='datepicker' value='mm/dd/yyyy'></input>");	
	} else if (thisType == "text") {
		$(".entry." + rowNo + "[name='type_detail']").parent().html("Specify char. bound here: <input type='text' class='entry " + rowNo +"' name='type_detail' value='Unbounded'></input>");	
	} else {
		$(".entry." + rowNo + "[name='type_detail']").parent().html("<input type='text' class='entry " + rowNo +"' name='type_detail'></input>");
	}
	});
	
// Select the content of bound and datetime
 $("#table-advanced").on('click', 'input[name="type_detail"][value="Unbounded"]' , function () {
	$(this).select();
	});
$("#table-advanced").on('click', 'input[name="type_detail"][value="mm/dd/yyyy"]' , function () {
	$(this).select();
	});
	
// Update suffix
  $("#table-advanced").on('change', 'select[name="type_detail"]' , function () {
	var aclass = $(this).attr('class').split(" ");
	var rowNo = aclass[1];
	var typeDetail = $(this).val();
		if (typeDetail == "property" || typeDetail == "hash_property") {
			$('.entry.' + rowNo +'[name="suffix_property"]').prop("disabled", false);
		} else if (typeDetail == "random") {
			$('.entry.' + rowNo +'[name="suffix_property"]').prop("disabled", true);
			}
	});
	
// Select the content of suffix
  $("#table-advanced").on('click', 'input[name="suffix_property"]' , function () {
	$(this).select();
	});

// Add a row of every row input	
  $("#table-advanced").on('keypress', 'input', function(){
	var aclass = $(this).attr('class').split(" ");
	var rowNo = aclass[1];
	$.addBigRow("table-advanced",checkRow,rowNo);
	$.addSmallRow(checkRow,rowNo);
	checkRow[rowNo] = 1;
	});	


// Update model when Model Name Change	
  $("input[name='modelname']").on('keyup', function(){
	var selected = $("#tabs").tabs('option', 'active');
	if (selected == 0) {
		themodel = $.updateSmallModel();			
	} else {
		themodel = $.updateBigModel();
	}
	$.getJSON();	
	$('legend#modelNameDisplay').text("Model " + $("input[name='modelname']").val());

	});

// Update model of every input	
  $("#table-advanced").on('keyup','input', function(){
	var aclass = $(this).attr('class').split(" ");
	var rowNo = aclass[1];
	themodel = $.updateBigModel();
	$.sycSmallToBig(rowNo);	
	$.getJSON();	
	});

// Update model and add a row of selection change	
 $("#table-advanced").on('change', 'select', function () {
	var aclass = $(this).attr('class').split(" ");
	var rowNo = aclass[1];
	$.addBigRow("table-advanced",checkRow,rowNo);	
	themodel = $.updateBigModel();
	$.addSmallRow(checkRow,rowNo);
	$.sycSmallToBig(rowNo);
	checkRow[rowNo] = 1;
	$.getJSON();
	});
})


// Get the JSON of the model and display on the website
$.getJSON = function ()
{
	var modelName = $("[name='modelname']").val();
	if (modelName == "") {
		$("#dialog").html("");
		$("#dialog").html("Please Input the Model Name");
		$("#dialog").dialog();
		$('#dialog').bind('dialogclose', function(event) {
			$("[name='modelname']").focus();
	 });	
	}
	var modeltemp = [];
	for (i=0; i<(themodel.length-1); i++) {
		modeltemp[i] = themodel[i]
	}
	modelinfo = {
		model: modelName,
		properties: modeltemp		
	};
	
	var see = JSON.stringify(modelinfo);
	theJSON = see;
	
	// For testing
		// $("#divResult").html("");
		// $("#divResult").append("<p>" +see + "</p><br>");
}

$.changeInternalName = function (aproperty,rowNo)
{	var thename = [];
	var intername = "";
	thename = aproperty.split(" ");
	intername = thename[0].toLowerCase();
	
	for(var i=1; i< thename.length ; i++) {
		intername += "_" + thename[i].toLowerCase();
	}
	
	$(".entry." + rowNo + "[name='internal_name']").val(intername);
}


$.updateBigModel = function ()
{	var model = [];
	$('.entry').each(function(){		
		var aclass = $(this).attr('class').split(" ");
		var rowNo = aclass[1];
		var prop = $('.entry.'+ rowNo +'[name="property"]').val();
		var typ = $('.entry.'+ rowNo +'[name="type"]').val();
		var typeD;
		
		if (typ == "handle") {
			var typeDetailSelect = $('select.entry.'+ rowNo +'[name="type_detail"]').val();
			if (typeDetailSelect == "random") {
				typeD = $('input.entry.'+ rowNo +'[name="type_detail"]').val() 
				+ "/" + $('select.entry.'+ rowNo +'[name="type_detail"]').val();				
			} else {
				typeD = $('input.entry.'+ rowNo +'[name="type_detail"]').val() 
				+ "/" + $('input.entry.'+ rowNo + '[name="suffix_property"]').val();
			}
		} else {
			typeD = $('.entry.'+ rowNo +'[name="type_detail"]').val();
		}
		
		var req = $('.entry.'+ rowNo +'[name="required"]').val();
		var maxo = $('.entry.'+ rowNo +'[name="max_occ"]').val();
		var inter = $('.entry.'+ rowNo +'[name="internal_name"]').val();
		var strct = $('.entry.'+ rowNo +'[name="structure"]').val();
			
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



$.sycSmallToBig = function (rowNo) {
	var selectorNameS = ".entry-s." + rowNo + "[name='property']";
	var selectorUseS = ".entry-s." + rowNo + "[name='use']";
	var selectorNameB = ".entry." + rowNo + "[name='property']";
	var selectorUseB = ".entry." + rowNo + "[name='type_detail']";
	
	var a = $(selectorNameB).val();
	var b = $(selectorUseB).val();
	
	$(selectorNameS).val(a);
	$(selectorUseS).val(b);
	
}


$.addBigRow = function (tableID,checkRow,rowNo)
{
	var table = document.getElementById(tableID);
	var rowCount = table.getElementsByTagName('tr').length;
	if (checkRow[rowNo] != 1) {
		var row = table.insertRow(rowCount);
		var colCount = table.rows[0].cells.length;
	    var newcell = row.insertCell(0);
	        newcell.innerHTML = rowCount-1;
		for(var i=1; i<colCount; i++) {
		var newcell = row.insertCell(i);
		if (i == 1) {
				newcell.innerHTML = ("<td><input type='text' class='entry " + (rowCount-1) 
				+ "' name='property'></input></td>");
			} else if (i == 2) {	
				newcell.innerHTML = ("<td><select class='entry " + (rowCount-1) 
				+ "' name='type'><option value='text'>Text</option><option value='handle'>Handle</option><option value='handle_reference'>Handle-Reference</option><option value='blank''>Blank</option><option value='controlled'>Controlled</option><option value='datetime'>DateTime</option><option value='number'>Number</option></select></td>");
			} else if (i == 3) {	
				newcell.innerHTML = ("<td>Specify char. bound here: <input type='text' class='entry " + (rowCount-1) +"' name='type_detail' value='Unbounded'></input></td>");
			} else if (i == 4) {	
				newcell.innerHTML = ("<td><select class='entry " + (rowCount-1) 
				+ "' name='required'><option value='yes'>Yes</option><option value='no'>No</option></select></td>");
			} else if (i == 5) {	
				newcell.innerHTML = ("<td><input type='text' class='entry " + (rowCount-1) 
				+ "' name='max_occ' value='1'></input></td>");
			} else if (i == 6) {	
				newcell.innerHTML = ("<td><input type='text' class='entry " + (rowCount-1) 
				+ "' name='internal_name' value=''></input></td>");
			} 	else {	
				newcell.innerHTML = ("<td><input type='text' class='entry " + (rowCount-1) 
				+ "' name='structure'></input></td>");
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