const form = document.forms.namedItem('course-add')
let formData
const courseAddFirstStep = document.getElementById('course-add-first-step')
const courseAddSecondStep = document.getElementById('course-add-second-step')
const courseAddThirdStep = document.getElementById('course-add-third-step')
const whatWillLearnBtn = document.getElementById('btn-what-will-learn')
const requirementsBtn = document.getElementById('btn-requirements')
const confirmBtn = document.getElementById('course-confirm-btn')
const backwardsBtn = document.getElementById('course-backwards-btn')

const optionDependencies = {
    'basic': ['basic'],
    'extra': ['basic'],
    'premium': ['basic', 'extra']
}

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
    formData.append('options', JSON.stringify(options))
    fetch('http://127.0.0.1:8000/api/courses/', {
        method: 'post',
        body: formData
    }).then(response => response.json()).then(data => console.log(data))

})

document.querySelector('#course-third-step-btn').addEventListener('click', event => {
    courseAddSecondStep.classList.add('invisible')
    courseAddThirdStep.classList.remove('invisible')
})

document.querySelectorAll('#options-checkboxes input[type=checkbox]').forEach(checkBox => checkBox.addEventListener('change', event => {
    const option = event.target.getAttribute('name')
    console.log(optionDependencies[option])
    if (event.target.checked) {
        // (!document.querySelector(`#checkbox-${optionDependencies[option]}`).checked)
        if (!optionDependencies[option].every(dependency => document.querySelector(`#checkbox-${dependency}`).checked)) {
            console.log('Wrong')
        } else {
            document.getElementById(`price-${option}`).classList.remove('hidden')
        }
    } else {
        document.getElementById(`price-${option}`).classList.add('hidden')
    }
}))
    
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