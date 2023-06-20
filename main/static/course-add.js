const form = document.forms.namedItem('course-add')
let formData
const courseAddFirstStep = document.getElementById('course-add-first-step')
const courseAddSecondStep = document.getElementById('course-add-second-step')
const whatWillLearnBtn = document.getElementById('btn-what-will-learn')
const requirementsBtn = document.getElementById('btn-requirements')
const confirmBtn = document.getElementById('course-confirm-btn')

whatWillLearnBtn.addEventListener('click', (event) => {
    const clone = document.getElementById('template-what-will-learn').content.cloneNode(true)
    document.getElementById('what-will-learn').append(clone)
})

requirementsBtn.addEventListener('click', (event) => {
    const clone = document.getElementById('template-requirements').content.cloneNode(true)
    document.getElementById('requirements').append(clone)
})

confirmBtn.addEventListener('click', (event) => {
    learnOptions = document.querySelectorAll('what-will-learn-option')
    const learnOptionsList = 
})

form.addEventListener('submit', (event) => 
{
    formData = new FormData(form)
    // fetch('http://localhost:8000/api/subjects/', {
    //     method: 'post',
    //     body: formData
    // }).then(response => response.json()).then(data => console.log(data))
    courseAddFirstStep.classList.add('invisible')
    courseAddSecondStep.classList.remove('invisible')
    event.preventDefault()
})