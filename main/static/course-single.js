let courseData
const form = document.forms.namedItem('section-add')
const addSectionForm = document.getElementById('section-add')
const courseId = document.getElementById('course-id').textContent

const addSectionBtn = document.getElementById('btn-add-section')
addSectionBtn.addEventListener('click', (event) => addSectionForm.classList.remove('invisible'))

fetch(`http://127.0.0.1:8000/api/courses/${courseId}/`).then(response => response.json()).then(data => initializePage(data))


function initializePage(data) {
    document.getElementById('course-name').textContent = data.name
    data.sections.forEach(section => {
        const clone = document.getElementById('template-course-section').content.cloneNode(true)
        clone.querySelector('span.section-name').textContent = section.name
        clone.querySelector('span.section-description').textContent = section.description
        clone.querySelector('div.course-section').setAttribute('section-id', section.id)
        document.getElementById('course-sections').append(clone)
    })
}

function createSection(data) {
    console.log('Section created')
}


form.addEventListener('submit', (event) => 
{
    formData = new FormData(form)
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

