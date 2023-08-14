let courseData
let courseOption
const courseOptions = ['basic', 'extra', 'premium']
const csrf_token = document.querySelector('#csrf-token input').value 
const courseId = document.getElementById('course-id').textContent

const formSection = document.forms.namedItem('section-add')
const addSectionForm = document.getElementById('section-add')
const addSectionBtn = document.getElementById('btn-add-section')
addSectionBtn.addEventListener('click', (event) => addSectionForm.classList.remove('invisible'))

backdrop.addEventListener('click', event => {
    backdrop.classList.add('invisible')
    document.querySelector('dialog[open]').close()
})

const optionsTabLinks = document.querySelectorAll('.course-option-link')
optionsTabLinks.forEach(link => link.addEventListener('click', event => {
    optionsTabLinks.forEach(link => link.classList.remove('course-option-link-selected'))
    courseOption = event.target.getAttribute('course-option')
    event.target.classList.add('course-option-link-selected')
    getCourseData()
}))

optionsTabLinks[0].click()

function getCourseData() {
    fetch(`http://127.0.0.1:8000/api/courses/${courseId}/`).then(response => response.json()).then(data => initializePage(data))
}

function initializePage(data) {
    document.getElementById('course-sections').innerHTML = ''
    document.getElementById('course-name').textContent = data.name
    data.sections.forEach(section => {
        // createSection(section)
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
        itemForm.addEventListener('submit', postItem.bind(itemForm, itemType))
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
                    newItem = new Test(this.bodyDiv, item)
                    break
                default:
                    newItem = new Item(this.bodyDiv, item)
                }
            newItem.renderItem()
        })
        document.getElementById('course-sections').append(element)
    }

    expand() {
        document.querySelectorAll('.course-section-body').forEach(sectionBody => {
            if (sectionBody != this.bodyDiv) {
                sectionBody.classList.add('invisible')
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
        fetch(`http://127.0.0.1:8000/api/sections/${id}/`, {
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
        this.section.append(element) 
    }

    delete() {
        this.div.remove()
        fetch(`http://127.0.0.1:8000/api/${this.type}s/${this.id}/`, {
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


// function createItem(section, item) {
//     const lessonTemplate = document.getElementById('template-section-item')
//     const clone = lessonTemplate.content.cloneNode(true)
//     clone.querySelector('.item-name').textContent = item.name
//     clone.querySelector('.section-item').setAttribute('item-id', item.id)
//     clone.querySelector('.section-item').setAttribute('item-type', item.type)
//     clone.querySelector('svg use').setAttribute('href', `#icon-${item.type}`)
//     if (item.type === 'test') {
//         clone.querySelector('.item-option').textContent = 'Добавить вопросы'
//         clone.querySelector('.item-option').addEventListener('click', event => {
//             document.querySelector('#dialog-questions').show()
//             backdrop.classList.remove('invisible')
//             initializeTestQuestions(item.id)
//             const questionForm = document.querySelector('#dialog-questions form')
//             questionForm.addEventListener('submit', postQuestion.bind(questionForm, item.id))
//         })
//     }
//     clone.querySelector('.item-delete').addEventListener('click', deleteItem.bind(clone.querySelector('.section-item')))
//     section.querySelector('.section-items').append(clone)
// }

function deleteItem(event) {
    this.remove()
    const id = this.getAttribute('item-id')
    const type = this.getAttribute('item-type')
    fetch(`http://127.0.0.1:8000/api/${type}s/${id}/`, {
        method: 'delete', 
        headers: {
            'X-CSRFToken': csrf_token,
        }
    })
    .then(response => response.json())
    .then(data => {console.log(data)})
}

function postItem(itemType, event) {
    const formData = new FormData(this)
    const section = this.closest('div.course-section')
    const sectionId = section.getAttribute('section-id')
    formData.append('section', sectionId)
    formData.append('option', courseOption)
    fetch(`http://127.0.0.1:8000/api/${itemType}s/`, {
        method: 'post',
        body: formData
    }).then(response => response.json())
    .then(data => {
        if (data.id) {
            createItem(section, data)
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
    formData.append('options', options)
    fetch(`http://127.0.0.1:8000/api/questions/`, {
        method: 'post',
        body: formData
    }).then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.id) {
            // createQuestion(data)
            let newQuestion = new Question(data)
            newQuestion.renderElement()
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
        fetch(`http://127.0.0.1:8000/api/questions/${this.id}/`, {
            method: 'delete', 
            headers: {
                'X-CSRFToken': csrf_token,
            }
        })
        .then(response => response.json())
        .then(data => {console.log(data)})
    }
}


// function createQuestion(data) {
//     const clone = document.getElementById('template-test-question').content.cloneNode(true)
//     clone.querySelector('.test-question-name').textContent = data.question
//     const questionElement = clone.querySelector('.test-question')
//     questionElement.setAttribute('item-type', 'question')
//     questionElement.setAttribute('item-id', data.id)
//     clone.querySelector('.test-question-delete').addEventListener('click', deleteItem.bind(questionElement))
//     document.getElementById('test-questions').append(clone)
// }

function initializeTestQuestions(testId) {
    fetch(`http://127.0.0.1:8000/api/tests/${testId}`)
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            document.getElementById('test-questions').innerHTML = ''
            data.questions.forEach(question => {
                // createQuestion(question)
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
    formData.append('course', courseId)
    fetch('http://127.0.0.1:8000/api/sections/', {
        method: 'post',
        body: formData
    }).then(response => response.json())
    .then(data => {
        if (data.id) {
            // createSection(data)
            let section = new Section(data)
            section.renderSection()
        }
        console.log(data)
    })
    event.preventDefault()
})




