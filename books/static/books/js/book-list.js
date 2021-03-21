$(document).ready(function () {
    $('.icon-info').on('click', function () {
        let cardBody = $(this).parent()
        let extension = cardBody.parent().find('.card-extension')
        if (extension.css('display') === 'none') {
            extension.show()
            cardBody.css('filter', 'drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25))')
        } else {
            extension.hide()
            cardBody.css('filter', '')
        }
    })
})


/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}