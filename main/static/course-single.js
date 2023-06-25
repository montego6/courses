let courseData
const csrf_token = document.querySelector('#csrf-token input').value 
const courseId = document.getElementById('course-id').textContent

const formSection = document.forms.namedItem('section-add')
const addSectionForm = document.getElementById('section-add')




const addSectionBtn = document.getElementById('btn-add-section')
addSectionBtn.addEventListener('click', (event) => addSectionForm.classList.remove('invisible'))


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
    clone.querySelector('span.section-name').textContent = section.name
    clone.querySelector('div.course-section').setAttribute('section-id', section.id)
    clone.querySelector('svg.section-header-icon-expand').addEventListener('click', expandSection.bind(clone.querySelector('div.course-section-body')))
    clone.querySelector('span.section-delete').addEventListener('click', deleteSection.bind(clone.querySelector('div.course-section')))
    section.lessons.forEach(lesson => createLesson(clone.querySelector('div.course-section'), lesson))
    const addLessonForm = clone.querySelector('.lesson-add-form')
    clone.querySelector('.btn-lesson-add').addEventListener('click', event => addLessonForm.classList.remove('invisible'))
    const formLesson = clone.querySelector('form')
    formLesson.addEventListener('submit', postLesson)
    document.getElementById('course-sections').append(clone)
}

function createLesson(section, lesson) {
    const lessonTemplate = document.getElementById('template-section-lesson')
    const clone = lessonTemplate.content.cloneNode(true)
    clone.querySelector('.lesson-name').textContent = lesson.name
    clone.querySelector('.section-lesson').setAttribute('lesson-id', lesson.id)
    clone.querySelector('.lesson-delete').addEventListener('click', deleteLesson.bind(clone.querySelector('.section-lesson')))
    section.querySelector('.section-lessons').append(clone)
}

function deleteLesson(event) {
    this.remove()
    const id = this.getAttribute('lesson-id')
    fetch(`http://127.0.0.1:8000/api/lessons/${id}/`, {
        method: 'delete', 
        headers: {
            'X-CSRFToken': csrf_token,
        }
    })
    .then(response => response.json())
    .then(data => {console.log(data)
    })
}

function postLesson(event) {
    const formData = new FormData(this)
    const section = this.closest('div.course-section')
    const sectionId = section.getAttribute('section-id')
    formData.append('section', sectionId)
    fetch('http://127.0.0.1:8000/api/lessons/', {
        method: 'post',
        body: formData
    }).then(response => response.json())
    .then(data => {
        if (data.id) {
            createLesson(section, data)
        }
        console.log(data)
    })
    event.preventDefault()
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




