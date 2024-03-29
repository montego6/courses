let courseData
let courseOption
const courseOptions = ['basic', 'extra', 'premium']
const csrf_token = document.querySelector('#csrf-token input').value 
const slug = document.getElementById('course-slug').textContent

const formSection = document.forms.namedItem('section-add')
const addSectionForm = document.getElementById('section-add')
const addSectionBtn = document.getElementById('btn-add-section')
addSectionBtn.addEventListener('click', (event) => addSectionForm.classList.remove('invisible'))

backdrop.addEventListener('click', event => {
    backdrop.classList.add('invisible')
    document.querySelector('dialog[open]').close()
})


document.querySelector('#btn-publish-course').addEventListener('click', event => {
    fetch(`/api/courses/${slug}/publish/`).then(response => response.json()).then(data => {
        console.log(data)
        window.location.href = `/course/${slug}/`
    })
})

fetch(`/api/courses/${slug}/`).then(response => response.json()).then(data => {
    courseData = data
    console.log(courseData)
    if (data.options.length) {
        initializeOptionsTab(data.options)
    }
    initializePage(courseData)
})


function initializeOptionsTab(data) {
    const tab = document.querySelector('#course-options-tab')
    data.forEach(option => {
        const element = document.createElement('span')
        element.setAttribute('course-option', option.option)
        element.textContent = option.option
        element.classList.add('course-option-link')
        element.addEventListener('click', event => {
            document.querySelector('.course-option-link-selected').classList.remove('course-option-link-selected')
            event.target.classList.add('course-option-link-selected')
            courseOption = event.target.getAttribute('course-option')
            initializePage(courseData)
        })
        tab.append(element)
    })
    tab.querySelector('span').classList.add('course-option-link-selected')
    courseOption = tab.querySelector('span').getAttribute('course-option')
}

function initializePage(data) {
   
    document.getElementById('course-sections').innerHTML = ''
    document.getElementById('course-name').textContent = data.name
    data.sections.forEach(section => {
        let newSection = new Section(section)
        newSection.renderSection()
    })
}


class Section {
    constructor(data) {
        this.id = data.id
        this.name = data.name
        this.items = data.items
        this.div = undefined
        this.bodyDiv = undefined
    }

    createElement() {
        const clone = document.getElementById('template-course-section').content.cloneNode(true)
        this.div = clone.querySelector('div.course-section')
        this.bodyDiv = clone.querySelector('div.course-section-body')
        clone.querySelector('span.section-name').textContent = this.name
        this.div.setAttribute('section-id', this.id)
        return clone
    }

    addListeners(element) {
        element.querySelector('svg.section-header-icon-expand').addEventListener('click', this.expand.bind(this))
        element.querySelector('span.section-delete').addEventListener('click', this.delete.bind(this))
    } 

    addDropdown(element) {
        const dropdownAdd = element.querySelector('.dropdown-add')
        element.querySelector('.btn-add-item').addEventListener('click', event => dropdownAdd.classList.toggle('invisible'))
        element.querySelectorAll('.dropdown-add-item').forEach(dropdownLink => {
        const itemType = dropdownLink.getAttribute('item-type')
        const addForm = element.querySelector(`.${itemType}-add-form`)
        const allForms = element.querySelectorAll('.section-forms')
        dropdownLink.addEventListener('click', event => {
            allForms.forEach(sectionForm => sectionForm.classList.add('invisible'))
            addForm.classList.remove('invisible')
        })
        const itemForm = element.querySelector(`form[name=${itemType}-add]`)
        itemForm.addEventListener('submit', postItem.bind(this, itemForm, itemType))
    })
    }

    renderSection() {
        const filteredItems = this.items.filter(item => {
            const optionIndex = courseOptions.findIndex(el => el === courseOption)
            const slicedArr = courseOptions.slice(0, optionIndex + 1)
            return slicedArr.includes(item.option)
        })
        let element = this.createElement()
        this.addDropdown(element)
        this.addListeners(element)
        filteredItems.forEach(item => {
            let newItem
            switch (item.type) {
                case 'test':
                    newItem = new Test(this, item)
                    break
                default:
                    newItem = new Item(this, item)
                }
            newItem.renderItem()
        })
        document.getElementById('course-sections').append(element)
    }

    expand() {
        document.querySelectorAll('.course-section-body:not(.invisible)').forEach(sectionBody => {
            if (sectionBody != this.bodyDiv) {
                sectionBody.classList.add('invisible')
                sectionBody.closest('.course-section').querySelector('.section-header-icon-expand').classList.toggle('icon-expand-animated')
            }
        })
        this.bodyDiv.classList.toggle('invisible')
        this.div.querySelector('.section-header-icon-expand').classList.toggle('icon-expand-animated')
        this.div.querySelector('.dropdown-add').classList.add('invisible')
        this.div.querySelectorAll('.section-forms:not(.invisible)').forEach(form => form.classList.add('invisible'))
    }

    delete() {
        this.div.remove()
        const id = this.div.getAttribute('section-id')
        fetch(`/api/sections/${id}/`, {
        method: 'delete', 
        headers: {
            'X-CSRFToken': csrf_token,
        }
    })
    .then(response => response.json())
    .then(data => {console.log(data)})
    }
}


class Item {
    constructor(section, data) {
        this.section = section
        this.id = data.id
        this.type = data.type
        this.name = data.name
        this.div = undefined
    }

    createElement() {
        const lessonTemplate = document.getElementById('template-section-item')
        const clone = lessonTemplate.content.cloneNode(true)
        clone.querySelector('.item-name').textContent = this.name
        this.div = clone.querySelector('.section-item')
        this.div.setAttribute('item-id', this.id)
        this.div.setAttribute('item-type', this.type)
        clone.querySelector('svg use').setAttribute('href', `#icon-${this.type}`)
        return clone
    }

    extra(element) {

    }

    addListeners(element) {
        element.querySelector('.item-delete').addEventListener('click', this.delete.bind(this))
    }

    renderItem() {
        let element = this.createElement()
        this.addListeners(element)
        this.extra(element)
        this.section.bodyDiv.append(element) 
    }

    delete() {
        this.div.remove()
        let courseDataSection = courseData.sections.find(section => section.id == this.section.id)
        let index = courseDataSection.items.findIndex(item => item.id = this.id)
        courseDataSection.items.splice(index, 1)
        fetch(`/api/${this.type}s/${this.id}/`, {
            method: 'delete', 
            headers: {
                'X-CSRFToken': csrf_token,
            }
        })
        .then(response => response.json())
        .then(data => {console.log(data)})
    }
}


class Test extends Item {
    extra(element) {
        element.querySelector('.item-option').textContent = 'Добавить вопросы'
        element.querySelector('.item-option').addEventListener('click', event => {
            document.querySelector('#dialog-questions').show()
            backdrop.classList.remove('invisible')
            initializeTestQuestions(this.id)
            const questionForm = document.querySelector('#dialog-questions form')
            questionForm.addEventListener('submit', postQuestion.bind(questionForm, this.id))
        })
    }
}


function deleteItem(event) {
    this.remove()
    const id = this.getAttribute('item-id')
    const type = this.getAttribute('item-type')
    fetch(`/api/${type}s/${id}/`, {
        method: 'delete', 
        headers: {
            'X-CSRFToken': csrf_token,
        }
    })
    .then(response => response.json())
    .then(data => {console.log(data)})
}

function postItem(itemForm, itemType, event) {
    const formData = new FormData(itemForm)
    formData.append('section', this.id)
    formData.append('option', courseOption)
    fetch(`/api/${itemType}s/`, {
        method: 'post',
        body: formData
    }).then(response => response.json())
    .then(data => {
        if (data.id) {
            let newItem
            switch (itemType) {
                case 'test':
                    newItem = new Test(this, data)
                    break
                default:
                    newItem = new Item(this, data)
                }
            newItem.renderItem()
            courseData.sections.find(section => section.id == this.id).items.push(data)
        }
        console.log(data)
    })
    
    event.preventDefault()
}


function postQuestion(testId, event) {
    const checkedRadio = this.querySelector('input[checked]')
    checkedRadio.value = checkedRadio.previousElementSibling.value
    const formData = new FormData(this)
    const options = Array.from(this.querySelectorAll('input[name=option]'), element => element.value)
    formData.append('test', testId)
    options.forEach(option => formData.append('options', option))
    fetch(`/api/questions/`, {
        method: 'post',
        body: formData
    }).then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.id) {
            let newQuestion = new Question(data)
            newQuestion.renderElement()
            document.querySelectorAll('#dialog-questions input[type=text]').forEach(input => input.value = '')
        }
    })
    event.preventDefault()
}

class Question {
    constructor(data) {
        this.id = data.id
        this.div = undefined
        this.name = data.question
    }

    createElement() {
        const clone = document.getElementById('template-test-question').content.cloneNode(true)
        clone.querySelector('.test-question-name').textContent = this.name
        this.div = clone.querySelector('.test-question')
        return clone
    }

    addListeners(element) {
        element.querySelector('.test-question-delete').addEventListener('click', this.delete.bind(this))
    }

    renderElement() {
        let element = this.createElement()
        this.addListeners(element)
        document.getElementById('test-questions').append(element)
    }

    delete() {
        this.div.remove()
        fetch(`/api/questions/${this.id}/`, {
            method: 'delete', 
            headers: {
                'X-CSRFToken': csrf_token,
            }
        })
        .then(response => response.json())
        .then(data => {console.log(data)})
    }
}



function initializeTestQuestions(testId) {
    fetch(`/api/tests/${testId}`)
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            document.getElementById('test-questions').innerHTML = ''
            data.questions.forEach(question => {
                let newQuestion = new Question(question)
                newQuestion.renderElement()
            })
        }
        console.log(data)
    })
}


formSection.addEventListener('submit', (event) => 
{
    formData = new FormData(formSection)
    formData.append('course', slug)
    fetch('/api/sections/', {
        method: 'post',
        body: formData
    }).then(response => response.json())
    .then(data => {
        if (data.id) {
            let section = new Section(data)
            section.renderSection()
        }
        console.log(data)
    })
    event.preventDefault()
})




