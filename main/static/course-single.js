let courseData
const csrf_token = document.querySelector('#csrf-token input').value 
const courseId = document.getElementById('course-id').textContent

const formSection = document.forms.namedItem('section-add')
const addSectionForm = document.getElementById('section-add')
const addSectionBtn = document.getElementById('btn-add-section')
addSectionBtn.addEventListener('click', (event) => addSectionForm.classList.remove('invisible'))

const backdrop = document.querySelector('#backdrop')
backdrop.addEventListener('click', event => {
    backdrop.classList.add('invisible')
    document.querySelector('dialog[open]').close()
})


fetch(`http://127.0.0.1:8000/api/courses/${courseId}/`).then(response => response.json()).then(data => initializePage(data))

function initializePage(data) {
    document.getElementById('course-name').textContent = data.name
    data.sections.forEach(section => createSection(section))
}


function expandSection(event) {
    this.classList.toggle('invisible')
}


function deleteSection(event) {
    this.remove()
    const id = this.getAttribute('section-id')
    fetch(`http://127.0.0.1:8000/api/sections/${id}/`, {
        method: 'delete', 
        headers: {
            'X-CSRFToken': csrf_token,
        }
    })
    .then(response => response.json())
    .then(data => {console.log(data)
    })
}

function createSection(section) {
    const clone = document.getElementById('template-course-section').content.cloneNode(true)
    const sectionDiv = clone.querySelector('div.course-section')
    clone.querySelector('span.section-name').textContent = section.name
    sectionDiv.setAttribute('section-id', section.id)
    clone.querySelector('svg.section-header-icon-expand').addEventListener('click', expandSection.bind(clone.querySelector('div.course-section-body')))
    clone.querySelector('span.section-delete').addEventListener('click', deleteSection.bind(sectionDiv))
    
    const dropdownAdd = clone.querySelector('.dropdown-add')
    clone.querySelector('.btn-add-item').addEventListener('click', event => dropdownAdd.classList.toggle('invisible'))
    clone.querySelectorAll('.dropdown-add-item').forEach(dropdownLink => {
        const itemType = dropdownLink.getAttribute('item-type')
        const addForm = clone.querySelector(`.${itemType}-add-form`)
        const allForms = clone.querySelectorAll('.section-forms')
        dropdownLink.addEventListener('click', event => {
            allForms.forEach(sectionForm => sectionForm.classList.add('invisible'))
            addForm.classList.remove('invisible')
        })
        const itemForm = clone.querySelector(`form[name=${itemType}-add]`)
        itemForm.addEventListener('submit', postItem.bind(itemForm, itemType))
    })

    section.items.forEach(item => createItem(clone.querySelector('div.course-section'), item))
    // itemTypes.forEach(itemType => {
    //     const addForm = clone.querySelector(`.${itemType}-add-form`)
    //     clone.querySelector(`.btn-${itemType}-add`).addEventListener('click', event => addForm.classList.remove('invisible'))
    //     const itemForm = clone.querySelector(`form[name=${itemType}-add]`)
    //     itemForm.addEventListener('submit', postItem.bind(itemForm, itemType))
    // })
    document.getElementById('course-sections').append(clone)

}


function createItem(section, item) {
    const lessonTemplate = document.getElementById('template-section-item')
    const clone = lessonTemplate.content.cloneNode(true)
    clone.querySelector('.item-name').textContent = item.name
    clone.querySelector('.section-item').setAttribute('item-id', item.id)
    clone.querySelector('.section-item').setAttribute('item-type', item.type)
    clone.querySelector('svg use').setAttribute('href', `#icon-${item.type}`)
    if (item.type === 'test') {
        clone.querySelector('.item-option').textContent = 'Добавить вопросы'
        clone.querySelector('.item-option').addEventListener('click', event => {
            document.querySelector('#dialog-questions').show()
            backdrop.classList.remove('invisible')
            initializeTestQuestions(item.id)
            const questionForm = document.querySelector('#dialog-questions form')
            questionForm.addEventListener('submit', postQuestion.bind(questionForm, item.id))
        })
    }
    clone.querySelector('.item-delete').addEventListener('click', deleteItem.bind(clone.querySelector('.section-item')))
    section.querySelector('.section-items').append(clone)
}

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
            createQuestion(data)
        }
    })
    event.preventDefault()
}


function createQuestion(data) {
    const clone = document.getElementById('template-test-question').content.cloneNode(true)
    clone.querySelector('.test-question-name').textContent = data.question
    const questionElement = clone.querySelector('.test-question')
    questionElement.setAttribute('item-type', 'question')
    questionElement.setAttribute('item-id', data.id)
    clone.querySelector('.test-question-delete').addEventListener('click', deleteItem.bind(questionElement))
    document.getElementById('test-questions').append(clone)
}

function initializeTestQuestions(testId) {
    fetch(`http://127.0.0.1:8000/api/tests/${testId}`)
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            document.getElementById('test-questions').innerHTML = ''
            data.questions.forEach(question => createQuestion(question))
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
            createSection(data)
        }
        console.log(data)
    })
    event.preventDefault()
})




