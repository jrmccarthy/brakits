/*
brackets.js

created: 6-21-12 by jmccarthy

Javascript functionality for the bracket HTML page.  Uses knockout.js to do all the real work.
We will have a dropdown on the page initially to select the event, and from there all the real magic will happen
*/

// var event_id=null


// $(document).ready(function() {
//     $("")
// });

// getEventDataAjax = function() {
//     var ret = '';
//     $.getJSON('/event', function(data){
//         event_id = data
//         return data
//     })
//     alert(event_id)
// }

// test = function() {}

// var eventData = $.getJSON('/event', function(data){
//         event_id = data
//         return 5
//     });

function eventlistitem(data){
    this._id = ko.observable(data._id)
    this.name = ko.observable(data.name)
    this.timestamp = ko.observable(data.timestamp)
}

function eventlistModel() {
    events = ko.observableArray([])

    $.getJSON("/event", function(allData) {
        var mappedData = $.map(allData, function(item) {return new eventlistitem(item) })
        self.events(mappedData)
    })
}




