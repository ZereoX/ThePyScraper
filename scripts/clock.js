updateClock();

function updateClock(){
	var today = new Date();
	var DAYNAMES = new Array('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday');
    var dayOfWeek = DAYNAMES[today.getDay()];
    var MONTHNAMES = new Array('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December');
    var curMonth = MONTHNAMES[today.getMonth()];
    var hours = today.getHours();

    if ( hours < 10)
    	hours = "0" + hours;

    var minutes = today.getMinutes();

    if ( minutes < 10)
    	minutes = "0" + minutes;

    var seconds = today.getSeconds();

    if ( seconds < 10)
    	seconds = "0" + seconds;


	document.getElementById("clock").innerHTML = dayOfWeek + ", " + curMonth + " " + today.getDate() + ", " + today.getFullYear() + " " + hours + ":" + minutes + ":" + seconds;
	
	setTimeout(updateClock, 1000);	
}