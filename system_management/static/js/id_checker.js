$(document).ready(function () {
    const id_input = $('#id_number')
    const search_button = $('#search_button')
    const error_message = $('#error_message')
    const form = $('#id_form')

    $(window).on('pageshow', function () {
        $('#id_number').val('') // Clear input on page show
    })

    // Format ID number as user types
    id_input.on('input', function () {
        let value = $(this).val()
        value = value.replace(/\D/g, '') // Remove non-digits
        $(this).val(value)

        validateInput(value)
    })

    function validateInput(value) {
        if (is_valid_id_number(value)) {
            search_button.prop('disabled', false)
            error_message.slideUp()
            id_input.removeClass('is-invalid').addClass('is-valid')
        } else {
            search_button.prop('disabled', true)
            if (value.length > 0) {
                showError('Please enter a valid South African ID Number.')
                id_input.removeClass('is-valid').addClass('is-invalid')
            } else {
                error_message.slideUp()
                id_input.removeClass('is-invalid is-valid')
            }
        }
    }

    function showError(message) {
        error_message.find('.error-text').text(message)
        error_message.slideDown()
    }

    function is_valid_id_number(id_number) {
        if (id_number.length !== 13 || !/^\d+$/.test(id_number)) {
            return false
        }

        const digits = id_number.split('').map(Number)

        let sum_odd = 0
        for (let i = 0; i < 12; i += 2) {
            sum_odd += digits[i]
        }

        let even_digits = ''
        for (let i = 1; i < 12; i += 2) {
            even_digits += digits[i]
        }
        const even_number = parseInt(even_digits) * 2

        let sum_even = 0
        even_number
            .toString()
            .split('')
            .forEach(function (digit) {
                sum_even += parseInt(digit, 10)
            })

        const total_sum = sum_odd + sum_even
        const checksum_digit = (10 - (total_sum % 10)) % 10

        return checksum_digit === digits[12]
    }

    // Handle form submission
    form.on('submit', function (e) {
        const loading = search_button.find('.loading')
        search_button.prop('disabled', true)
        loading.show()
    })
})