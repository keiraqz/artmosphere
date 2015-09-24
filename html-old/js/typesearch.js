
$(document).ready(function(){
	// Hard Code
		// Model Book
	// var designstring = '{"model":"Book","properties":[{"number":0,"property":"ID","type":"handle","type-detail":"Prefix/Random","required":"Yes","max-occurences":1,"internal-name":"id"},{"number":1,"property":"Title","type":"Text","type-detail":"250 characters","required":"Yes","max-occurences":1,"internal-name":"title"},{"number":2,"property":"Genre","type":"controlled","type-detail":"Fictional, Non-fictional","required":"Yes","max-occurences":1,"internal-name":"genre"},{"number":3,"property":"Media","type":"controlled","type-detail":"Printed, Audio, e-book","required":"Yes","max-occurences":1,"internal-name":"media"},{"number":4,"property":"Author","type":"Blank","required":"No","max-occurences":2,"internal-name":"author"}]}';
		// Model Movie
	// var designstring = '{"model":"Movie","properties":[{"number":0,"property":"ID","type":"handle","type-detail":"Prefix/Random","required":"Yes","max-occurences":1,"internal-name":"id"},{"number":1,"property":"Title","type":"Text","type-detail":"250 characters","required":"Yes","max-occurences":1,"internal-name":"title"},{"number":2,"property":"Genre","type":"controlled","type-detail":"Action, Fiction, Document","required":"Yes","max-occurences":1,"internal-name":"genre"},{"number":3,"property":"Media","type":"controlled","type-detail":"DVD, online","required":"Yes","max-occurences":1,"internal-name":"media"},{"number":4,"property":"Author","type":"Blank","required":"No","max-occurences":2,"internal-name":"author"},{"number":5,"property":"Year","type":"controlled","type-detail":"1998,1999,2000,2001","required":"Yes","max-occurences":1,"internal-name":"year"}]}';
	
	aresult = ""; 
//	aresult = '{"total-matches":7, "page":1, "per-page":3, "records":[{"ID":"Prefix/123","Title":"movie1","Genre":"Action", "Media":"DVD","Author":"author1","Year":"1998"},{"ID":"Prefix/234","Title":"movie2","Genre":"Fictional", "Media":"DVD","Author":"author2","Year":"1999"},{"ID":"Prefix/567","Title":"movie3","Genre":"Fictional", "Media":"DVD,online","Author":"author3","Year":"1998,1999"},{"ID":"Prefix/444","Title":"movie4","Genre":"Fictional", "Media":"online","Author":"author4","Year":"1999"},{"ID":"Prefix/555","Title":"movie5", "Author":"author5","Year":"1999"},{"ID":"Prefix/666","Title":"movie6","Genre":"Fictional", "Media":"online","Author":"author6","Year":"1999"},{"ID":"Prefix/777","Title":"movie7","Genre":"Fictional", "Media":"DVD","Author":"author7"}]}';	
	modelstring = {};

	designstring = "";
	design = "";
	
	$('#select-model').on('click', function () {
		$('#select-model').prop("hidden", true);
		$.selectModel();
	});
	
	$('#model-selection').on('change','select', function () {		
		var selected = $("select#modelselection option:selected").val();	
	 	var	selectdesign = modelstring[selected];
		design = jQuery.parseJSON(selectdesign);
		$.loadPage(design);
		var queryToProcess = "http://...:8080/do?query=objatt_model:" + selected;
		$.performInitialSearch(queryToProcess);
	});
	
	$('#searcharea').on('keyup','input#perform-search', function () {		
		var selected = $("select#modelselection option:selected").val();	
	 	var	searchValue = $('#perform-search').val();
		var queryToProcess = "";
		if (searchValue != "") {
		queryToProcess = "http://10.27.4.229:8080/do?query=objatt_model:" + selected + " AND objatt_json:" + searchValue;
		} else {
		queryToProcess = "http://10.27.4.229:8080/do?query=objatt_model:" + selected;
		}
		
		$.performInitialSearch(queryToProcess);
	});
	
	$('#filterbox').on('click','select', function () {
		var selected = $("select#modelselection option:selected").val()	
		var queryToProcess = "http://...:8080/do?query=(" ;
		var selections = [];
		
		$.each($("select.filterBox"), function () {
			var innerSelections = [];
			var innerString = "(";
			var theName = this.name;
			var theSelected = $(".filterBox[name='" + theName + "'] option:selected");
			$.each(theSelected, function() {
				var self = this;
				innerSelections.push(self.innerHTML);
			});
			if (innerSelections.length > 1) {
				for (var i = 0; i < selections.length - 1; i++) {
					innerString += "objatt_json:" + innerSelections[i] + " OR ";
				}
			}
			
			if (innerSelections.length != 0) {
			innerString += "objatt_json:" + innerSelections[innerSelections.length - 1] + ")";
			selections.push(innerString);
			}
		});			
		
		if (selections.length != 1) {
			for (var i = 0; i < selections.length - 1; i++) {
				queryToProcess += selections[i] + " AND ";
			}
		}
		
		var searchValue = $('#perform-search').val();
		if (searchValue != "") {
			queryToProcess += selections[selections.length - 1] + ") AND objatt_model:" 
			+ selected + " AND objatt_json:" + searchValue;			
		} else {
			queryToProcess += selections[selections.length - 1] + ") AND objatt_model:" 
			+ selected;			
		}		
		$.performInitialSearch(queryToProcess);
	});

})

$.selectModel = function () {
	$.ajax({
		url:"http://...:8080/do/11156/repo.1-12",
		type:"GET",
		complete: $.onSelectSuccess
	});

}

$.onSelectSuccess = function (data) {
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
		modelstring[name]=value;
		}
		i++;
	});
	
	var models = "<select id='modelselection'>";
	$.each(modelstring, function () {
		designstring = jQuery.parseJSON(this.toString());
		models += "<option value='"+designstring.model+"'>" + designstring.model + "</option>";
	});

	models += "</select>";
	$("#model-selection").html(models + " Registry");	
	
	var selected = $("#modelselection").val()	
 	var selectdesign = modelstring[selected];
	design = jQuery.parseJSON(selectdesign);
	$.loadPage(design);
	var queryToProcess = "http://...:8080/do?query=objatt_model:" + selected;
	$.performInitialSearch(queryToProcess);

}

$.performInitialSearch = function (queryToProcess) {

	$.ajax({
		url:queryToProcess,
		type:"GET",
		complete: function (data) {
			aresult = $.xmlToJSON(data.responseText);			
			$.toLoadResult(aresult);
		}
	});
}

$.reperformSearch = function (theModelHandle) {

	$.ajax({
		url:"http://...:8080/do/" + theModelHandle,
		type:"GET",
		complete: $.onComplete			
	});
}

$.onComplete = function (data) {
	aresult = $.xmlToJSON(data.responseText);			
	records = [];
	result = {};
	result = jQuery.parseJSON(aresult);
	records = $.toType(result.records);
	
	$.toDisplay(theModelHandle);
}

$.xmlToJSON = function (xml) {
	var xml2JSON = {};
	var innerRecords = [];
	
	
	var doxml = $(xml).find("do");
	xml2JSON['total-matches'] = doxml.length;
		
	$.each(doxml, function() {
		var self = this;
		var thisRecord = {};
		
		var doAtts = $.parseXML(self.outerHTML).getElementsByTagName("att");

		$.each(doAtts, function() {
			var oneAtt = this;
			if (oneAtt.getAttribute("name") == "json") {
				thisRecord = jQuery.parseJSON(oneAtt.getAttribute("value"));
			}
		});
		thisRecord.ID = $.parseXML(self.outerHTML).childNodes[0].getAttribute("id");
		innerRecords.push(thisRecord);
	});

	xml2JSON.records = innerRecords;
	xml2JSON.page = 1;
	xml2JSON['per-page'] = 3;
		
	return JSON.stringify(xml2JSON);
}

$.loadPage = function (design) {
	$('#filterbox').html("");
	$.each(design.properties, function (i, n)
	{
		if (n["type"] == "controlled") 
		{
			var oneline = "<tr><td>"+n.property+"</td><td><select style='width: 100px;' class='filterBox' name='" + n.property + "' multiple>";
			var options = n["type-detail"].split(",");
			$.each(options, function(){
				oneline += "<option value='" + this.toLowerCase() +"'>" + this +"</option>";
			});
			oneline += '</select></td></tr>';
			$('#filterbox').append(oneline);
		}
	});
}

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