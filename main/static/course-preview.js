const courseId = document.getElementById('course-id').textContent
const csrf_token = document.querySelector('#csrf-token input').value 

getCourseData()

backdrop.addEventListener('click', event => {
    backdrop.classList.add('invisible')
    document.querySelector('dialog[open]').close()
    player.pause()
    document.getElementById('side-menu').classList.remove('invisible')
})


function getCourseData() {
    fetch(`/courses/${courseId}/`).then(response => response.json()).then(data => initializePage(data))
}

function initializeHeader(data) {
    document.getElementById('course-name').textContent = data.name
    document.getElementById('course-short_description').textContent = data.short_description
    document.getElementById('course-date_updated').textContent = data.date_updated
    document.getElementById('course-language').textContent = data.language
}

function initializeWhatWillLearn(data) {
    data.what_will_learn.forEach(item => {
        const clone = document.getElementById('template-what_will_learn').content.cloneNode(true)
        clone.querySelector('span').textContent = item
        document.getElementById('what_will_learn-items').append(clone)
    })
}


function initizlizeRequirements(data) {
    data.requirements.forEach(requierement => {
        const clone = document.getElementById('template-requirements').content.cloneNode(true)
        clone.querySelector('li').textContent = requierement
        document.querySelector('#course-requirements ul').append(clone)
    })
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}


class SideBar {
    static render(paymentOption, data) {
        this.paymentOption = paymentOption
        this.data = data
        switch (paymentOption) {
            case 'free':
                this.renderNotPaid()
                break
            case 'premium':
                this.renderLast()
                break
            default:
                this.renderOther()
        }
    }
    
    static renderNotPaid() {
        document.getElementById('side-menu-price').textContent = this.data.price + '. руб.'
    }

    static renderOther() {
        document.getElementById('side-menu-paid').classList.remove('invisible')
        document.querySelector('#side-menu-paid span').textContent = `Вы оплатили курс. В рамках опции ${this.paymentOption} вам доступны:`
        document.querySelector('#side-menu-paid > span:last-child').textContent = `Также доступны следующие опции:`
        document.getElementById('side-menu-price').classList.add('invisible')
        document.getElementById('buy-btn').classList.add('invisible')
        document.getElementById('side-menu-upgrade').classList.remove('invisible')
    }

    static renderLast() {
        document.getElementById('side-menu-paid').classList.remove('invisible')
        document.querySelector('#side-menu-paid span').textContent = `Вы оплатили курс. В рамках опции ${this.paymentOption} вам доступны:`
        document.getElementById('side-menu-price').classList.add('invisible')
        document.getElementById('buy-btn').classList.add('invisible')
        document.getElementById('side-menu-options').classList.add('invisible')
    }
}


function initializeSidebar(data, payment) {
    document.getElementById('side-menu-cover').src = data.cover
    SideBar.render(payment.option, data)
    let paidIndex = data.options.findIndex(element => element.option == payment.option)
    const filteredOptions = data.options.slice(paidIndex + 1)
    filteredOptions.forEach(element => {
        spanEl = `<span id="buy-${element.option}" data-option="${element.option}">${capitalizeFirstLetter(element.option)}</span>`
        document.getElementById('side-menu-options-header').innerHTML += spanEl
    })
    if (paidIndex + 1 && paidIndex + 1 < data.options.length) {
        const upgradePrice = filteredOptions[0].price - data.options[paidIndex].price
        document.getElementById('side-menu-upgrade-price').textContent = `${upgradePrice} руб.`
    }
    document.querySelectorAll('#side-menu-options-header span').forEach(option => option.addEventListener('click', event => {
        if (paidIndex + 1 && paidIndex + 1 < data.options.length) {
            const upgradePrice = filteredOptions.find(option => option.option == selectedOption).price - data.options[paidIndex].price
            document.getElementById('side-menu-upgrade-price').textContent = `${upgradePrice} руб.`
        }
    }))

}

let optionPrices 

function initializePage(data) {
    initializeHeader(data)
    initializeWhatWillLearn(data)
    initizlizeRequirements(data)

    document.getElementById('course-full_description').innerHTML = data.full_description
    
    optionPrices = data.options

    initializeSidebar(data, {option: 'basic'})
}


