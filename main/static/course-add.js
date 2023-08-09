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
    'basic': [],
    'extra': ['basic'],
    'premium': ['basic', 'extra']
}

const optionRreverseDependencies = {
    'basic': ['extra', 'premium'],
    'extra': ['premium'],
    'premium': []
}


document.querySelectorAll('#options-checkboxes input[type=checkbox]').forEach(checkBox => checkBox.addEventListener('change', event => {
    const option = event.target.getAttribute('name')
    if (event.target.checked) {
        if (optionDependencies[option] != [] && !optionDependencies[option].every(dependency => document.querySelector(`#checkbox-${dependency}`).checked)) {
            event.target.closest('div.options-row').querySelector('.options-error').classList.remove('hidden')
            event.target.checked = false
        } else {
            document.getElementById(`price-${option}`).classList.remove('hidden')
            document.querySelectorAll('.options-error').forEach(errorElement => errorElement.classList.add('hidden'))
        }
    } else {
        document.getElementById(`price-${option}`).classList.add('hidden')
        optionRreverseDependencies[option].forEach(dependant => {
            if (document.querySelector(`#checkbox-${dependant}`).checked) {
                document.getElementById(`price-${dependant}`).classList.add('hidden')
                document.querySelector(`#options-${dependant} .options-error`).classList.remove('hidden')
                document.querySelector(`#checkbox-${dependant}`).checked = false
            }
        })

    }
}))

document.querySelector('#course-back-to-2step-btn').addEventListener('click', event => {
    courseAddSecondStep.classList.remove('invisible')
    courseAddThirdStep.classList.add('invisible')
})


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
    const level = document.getElementById('select-level').value
    formData.append('level', level)
    let optionsArr = []
    document.querySelectorAll('.options-row input:checked').forEach(optionCheckbox => {
        const option = optionCheckbox.getAttribute('name')
        const price = document.querySelector(`input[name=${option}-price]`).value
        const optionData = {
            option: option,
            price: price
        }
        optionsArr.push(optionData)
    })
    formData.append('options', JSON.stringify(optionsArr))
    console.log(formData)
    // fetch('http://127.0.0.1:8000/api/courses/', {
    //     method: 'post',
    //     body: formData
    // }).then(response => response.json()).then(data => console.log(data))

})

document.querySelector('#course-third-step-btn').addEventListener('click', event => {
    courseAddSecondStep.classList.add('invisible')
    courseAddThirdStep.classList.remove('invisible')
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