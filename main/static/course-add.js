const form = document.forms.namedItem('course-add')
let formData
const courseAddFirstStep = document.getElementById('course-add-first-step')
const courseAddSecondStep = document.getElementById('course-add-second-step')
const whatWillLearnBtn = document.getElementById('btn-what-will-learn')
const requirementsBtn = document.getElementById('btn-requirements')
const confirmBtn = document.getElementById('course-confirm-btn')
const backwardsBtn = document.getElementById('course-backwards-btn')

whatWillLearnBtn.addEventListener('click', (event) => {
    const clone = document.getElementById('template-what-will-learn').content.cloneNode(true)
    document.getElementById('what-will-learn').append(clone)
})

requirementsBtn.addEventListener('click', (event) => {
    const clone = document.getElementById('template-requirements').content.cloneNode(true)
    document.getElementById('requirements').append(clone)
})

backwardsBtn.addEventListener('click', (event) => {
    courseAddFirstStep.classList.remove('invisible')
    courseAddSecondStep.classList.add('invisible')
})

confirmBtn.addEventListener('click', (event) => {
    learnOptions = document.querySelectorAll('.what-will-learn-option')
    const learnList = Array.from(learnOptions, option => option.value).filter(option => option.value != '')
    requirementsOptions = document.querySelectorAll('.requirements-option')
    const requirementsList = Array.from(requirementsOptions, option => option.value).filter(option => option.value != '')
    const options = {option: "value"}
    learnList.forEach(learn => formData.append('what_will_learn', learn))
    requirementsList.forEach(requirement => formData.append('requirements', requirement))
    // formData.append('requirements', requirementsList)
    formData.append('options', JSON.stringify(options))
    fetch('http://127.0.0.1:8000/api/courses/', {
        method: 'post',
        body: formData
    }).then(response => response.json()).then(data => console.log(data))

})
    
form.addEventListener('submit', (event) => 
{
    formData = new FormData(form)
    courseAddFirstStep.classList.add('invisible')
    courseAddSecondStep.classList.remove('invisible')
    event.preventDefault()
})

fetch('http://127.0.0.1:8000/static/langmap.json').then(response => response.json()).then(data => {
    for (const key in data) {
        let selectEL = document.createElement('option')
        selectEL.setAttribute('value', key)
        selectEL.textContent = data[key]
        if (key === 'en') {
            selectEL.setAttribute('selected', true)
        }
        document.querySelector('#select-language').append(selectEL)
    }
})