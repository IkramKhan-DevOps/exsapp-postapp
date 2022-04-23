function countdown_timer_x(from, element, message_time_up) {
    var countDownDate = new Date(from * 1000).getTime();

    // Update the count down every 1 second
    var x = setInterval(function () {

        // Get today's date and time
        var now = new Date().getTime();

        // Find the distance between now and the count down date
        var distance = countDownDate - now;

        // Time calculations for days, hours, minutes and seconds
        let s = '';
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        if (days != 0) {
            if (days == 1) {
                s += days + "Day "
            } else {
                s += days + "Days "
            }
        }
        if (hours != 0) {
            if (hours == 1) {
                s += hours + "Hour "
            } else {
                s += hours + "Hours "
            }
        }
        if (minutes != 0) {
            if (minutes == 1) {
                s += minutes + "Minute "
            } else {
                s += minutes + "Minutes "
            }
        }
        if (seconds != 0) {
            if (seconds == 1) {
                s += seconds + "Second "
            } else {
                s += seconds + "Seconds "
            }
        }


        // Output the result in an element with id="demo"
        document.getElementById(element).innerHTML = s;

        // If the count down is over, write some text
        if (distance < 0) {
            clearInterval(x);
            document.getElementById(element).innerHTML = message_time_up;
        }
    }, 1000);
}