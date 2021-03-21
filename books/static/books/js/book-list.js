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