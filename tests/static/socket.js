$(document).ready(function() {

    namespace = '/test';
    var socket = io(namespace);

    socket.on('connect', function() {
        socket.emit('my_event', {data: 'connected to the SocketServer...'});
    });

    socket.on('my_response', function(msg, cb) {
        $('#log').append('<br>' + $('<div/>').text('logs #' + msg.count + ': ' + msg.data).html());
        if (cb)
            cb();
    });
    $('form#emit').submit(function(event) {
        socket.emit('my_event', {data: $('#emit_data').val()});
        return false;
    });
    $('form#broadcast').submit(function(event) {
        socket.emit('my_broadcast_event', {data: $('#broadcast_data').val()});
        return false;
    });
    $('form#disconnect').submit(function(event) {
        socket.emit('disconnect_request');
        return false;
    });
});

const matchList = document.getElementById('match-list');

// Search food.json and filter it
const searchFood = async searchText => {
    const res = await fetch('food.json');
    const food = await res.json();
    console.log(food);

    // get matches
    let matches = food.filter(state => {
        const regex = new RegExp(`^${searchText}`, 'gi');
        return state.food.match(regex);
    });

    if (searchText.length === 0 || matches.length === 0) {
        matches = [];
        matchList.innerHTML = '';
    }
    console.log(matches);

    outputHTML(matches);
}

// show results in HTML
const outputHTML = matches => {
    if(matches.length > 0) {
        const html = matches.map(match => `
            <div class="card card-body mb-1">
                <h5>${match.food}: calories=${match.calories} 
                    carp=${match.carp} protein=${match.protein} fat=${match.fat}
                </h5>
                <small>${match.refdate}</small>
            </div>
            `
        ).join('');
        console.log(html);
        matchList.innerHTML = html;
    }
}

search.addEventListener('input', () => searchFood(search.value));
