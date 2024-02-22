const form = document.forms.namedItem('form-cover')
let formData = null
let courseChanges = {}
let categoriesData
let wwlIsChanged = false
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

const csrf_token = document.querySelector('#csrf-token input').value 
const slug = document.querySelector('#course-slug').textContent

fetch(`/api/courses/${slug}/`).then(response => response.json()).then(data => {
    console.log('DATA', data)
    initializeInputs(data)
})

document.querySelectorAll('.input-change').forEach(changeSpan => {
    changeSpan.addEventListener('click', event => {
        event.target.previousElementSibling.disabled = false
        event.target.classList.toggle('invisible')
        event.target.nextElementSibling.classList.toggle('invisible')
    })
})

document.querySelector('#cover-change').addEventListener('click', event => {
    document.querySelector('#course-cover').classList.add('invisible')
    event.target.previousElementSibling.querySelector('input[name=cover]').classList.remove('invisible')
    event.target.previousElementSibling.querySelector('input[name=cover]').disabled = false
    event.target.classList.toggle('invisible')
    event.target.nextElementSibling.classList.toggle('invisible')
})

document.querySelectorAll('.save-changes').forEach(saveSpan => {
    saveSpan.addEventListener('click', event => {
        const input = event.target.previousElementSibling.previousElementSibling
        input.disabled = true
        event.target.classList.toggle('invisible')
        event.target.previousElementSibling.classList.toggle('invisible')
        const field = input.getAttribute('name')
        courseChanges[field] = input.value
        console.log(courseChanges)
    })
})

document.querySelector('.save-changes-cover').addEventListener('click', event => {
    event.target.classList.toggle('invisible')
    event.target.previousElementSibling.classList.toggle('invisible')
    formData = new FormData(form)
    console.log(formData)
    event.target.previousElementSibling.previousElementSibling.querySelector('input[name=cover]').disabled = true
})

function initializeLanguages(courseData) {
    fetch('/static/langmap.json').then(response => response.json()).then(data => {
        for (const key in data) {
            let selectEL = document.createElement('option')
            selectEL.setAttribute('value', key)
            selectEL.textContent = data[key]
            if (key === courseData.language) {
                selectEL.setAttribute('selected', true)
            }
            document.querySelector('#select-language').append(selectEL)
        }
    })
}

function initializeReqs(courseData) {
    courseData.what_will_learn.forEach(learnOption => {
        const clone = document.querySelector('#template-what-will-learn').content.cloneNode(true)
        clone.querySelector('input').value = learnOption
        document.querySelector('#what-will-learn').append(clone)
    })

    courseData.requirements.forEach(reqOption => {
        const clone = document.querySelector('#template-requirements').content.cloneNode(true)
        clone.querySelector('input').value = reqOption
        document.querySelector('#requirements').append(clone)
    })
}

function initializeInputs(courseData) {
    document.querySelector('img#course-cover').setAttribute('src', courseData.cover)
    document.querySelector('input[name=name]').value = courseData.name
    document.querySelector('input[name=short_description]').value = courseData.short_description
    document.querySelector('textarea[name=full_description]').value = courseData.full_description

    initializeLanguages(courseData)

    if (courseData.is_free) {
        document.querySelector('input[name=is_free]').setAttribute('checked', 'true')
    }

    initializeReqs(courseData)

    fetch('/api/categories/').then(response => response.json()).
    then(data => {
    categoriesData = data
    initializeCategories(categoriesData, courseData)
    })

    document.querySelector(`option[value=${courseData.level}]`).setAttribute('selected', true)

    initializePrices(courseData)

    setWWLListeners()

}

function setSecondStepListenerChange(element) {
    element.addEventListener('click', event => {
        event.target.previousElementSibling.disabled = false
        event.target.nextElementSibling.classList.toggle('invisible')
        event.target.classList.toggle('invisible') 
    })
}


function setSecondStepListenerSave(element) {
    element.addEventListener('click', event => {
        wwlIsChanged = true
        event.target.classList.toggle('invisible')
        event.target.previousElementSibling.classList.toggle('invisible')
        event.target.parentNode.querySelector('input').disabled = true
    })
}

function setSecondStepListenerDelete(element) {
    element.addEventListener('click', event => {
        wwlIsChanged = true
        event.target.closest('div').remove()
    })
}

function setWWLListeners() {
    document.querySelectorAll('.wwl-change, .req-change').forEach(wwlChange => setSecondStepListenerChange(wwlChange))
    document.querySelectorAll('.wwl-save, .req-save').forEach(wwlSave => setSecondStepListenerSave(wwlSave))
    document.querySelectorAll('.wwl-delete, .req-delete').forEach(wwlDelete => setSecondStepListenerDelete(wwlDelete))
}

function initializePrices(courseData) {
    courseData.options.forEach(option => {
        document.querySelector(`input[name=${option.option}-price]`).value = option.amount
        document.querySelector(`input[name=${option.option}-price]`).setAttribute('price-id', option.id)
        document.querySelector(`#price-${option.option}`).classList.remove('hidden')
        document.querySelector(`input[name=${option.option}]`).setAttribute('checked', true)
    })
}

function initializeCategories(data, courseData) {
    for (category of data) {
        for (subcategory of category.subcategories) {
            for (subject of subcategory.subjects) {
                if (subject.id == courseData.subject) {
                    initializeCategoriesValues(data, category, subcategory, subject)
                    return
                }
            }
        }
    }
}

function initializeCategoriesValues(data, category, subcategory, subject) {
    initializeCategoriesSelect('category', data, category)
    initializeCategoriesSelect('subcategory', category.subcategories, subcategory)
    initializeCategoriesSelect('subject', subcategory.subjects, subject)
}

function initializeCategoriesSelect(mode, data, selected) {
    const select = document.querySelector(`#select-${mode}`)
    select.querySelectorAll('option:not(:disabled)').forEach(option => option.remove())
    select.value = ''
    data.forEach(category => {
        let categoryEl = document.createElement('option')
        categoryEl.setAttribute('value', category.id)
        categoryEl.textContent = category.name
        if (category == selected) {
            categoryEl.setAttribute('selected', true)
        }
        select.append(categoryEl)
    })
}

document.querySelector('#select-category').addEventListener('change', event => {
    document.querySelector('#div-subcategory').classList.remove('invisible')
    document.querySelector('#div-subject').classList.add('invisible')
    const chosenCategory = categoriesData.find(category => category.id == event.target.value)
    initializeCategoriesSelect('subcategory', chosenCategory.subcategories)
})

document.querySelector('#select-subcategory').addEventListener('change', event => {
    document.querySelector('#div-subject').classList.remove('invisible')
    const chosenCategoryId = document.querySelector('#div-category select').value
    const chosenCategory = categoriesData.find(category => category.id == chosenCategoryId)
    const chosenSubCategory = chosenCategory.subcategories.find(subcategory => subcategory.id == event.target.value)
    initializeCategoriesSelect('subject', chosenSubCategory.subjects)
})


// fetch('/api/categories/').then(response => response.json()).
// then(data => {
//     console.log('CATEGORIES', data)
//     categoriesData = data
//     // initializeCategoriesSelect('category', categoriesData)
//     initializeCategories(categoriesData)
// })

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

// document.querySelector('#is_free-checkbox').addEventListener('change', event => {
//     if (event.target.checked) {
//         document.querySelector('input[name=price]').value = 0
//         document.querySelector('input[name=price]').disabled = true
//     } else {
//         document.querySelector('input[name=price]').disabled = false
//     }
// })


whatWillLearnBtn.addEventListener('click', (event) => {
    const clone = document.getElementById('template-what-will-learn').content.cloneNode(true)
    setSecondStepListenerChange(clone.querySelector('.wwl-change'))
    setSecondStepListenerSave(clone.querySelector('.wwl-save'))
    setSecondStepListenerDelete(clone.querySelector('.wwl-delete'))
    document.getElementById('what-will-learn').append(clone)
})

requirementsBtn.addEventListener('click', (event) => {
    const clone = document.getElementById('template-requirements').content.cloneNode(true)
    setSecondStepListenerChange(clone.querySelector('.req-change'))
    setSecondStepListenerSave(clone.querySelector('.req-save'))
    setSecondStepListenerDelete(clone.querySelector('.req-delete'))
    document.getElementById('requirements').append(clone)
})

backwardsBtn.addEventListener('click', (event) => {
    courseAddFirstStep.classList.remove('invisible')
    courseAddSecondStep.classList.add('invisible')
})

confirmBtn.addEventListener('click', (event) => {
    formData.set('is_free', document.querySelector('input[name=is_free]').checked)
    learnOptions = document.querySelectorAll('.what-will-learn-option')
    const learnList = Array.from(learnOptions, option => option.value).filter(value => value != '')
    requirementsOptions = document.querySelectorAll('.requirements-option')
    const requirementsList = Array.from(requirementsOptions, option => option.value).filter(value => value != '')
    learnList.forEach(learn => formData.append('what_will_learn', learn))
    requirementsList.forEach(requirement => formData.append('requirements', requirement))
    const subject = document.querySelector('#select-subject').value
    formData.append('subject', subject)
    const level = document.getElementById('select-level').value
    formData.append('level', level)
    let optionsArr = []
    document.querySelectorAll('.options-row input:checked').forEach(optionCheckbox => {
        const option = optionCheckbox.getAttribute('name')
        const price = Number(document.querySelector(`input[name=${option}-price]`).value)
        const optionData = {
            option: option,
            price: price
        }
        optionsArr.push(optionData)
    })
    // formData.append('options', JSON.stringify(optionsArr))
    console.log(formData)
    fetch('/api/courses/', {
        method: 'post',
        body: formData
    }).then(response => response.json()).then(data => {
        if (data.id) {
            let pricesPromises = []
            optionsArr.forEach(optionEl => {
                priceData = {
                    'course': data.id,
                    'option': optionEl.option,
                    'amount': optionEl.price
                }
                pricesPromises.push(postPrice(priceData))
            })
            Promise.all(pricesPromises).then(([data1, data2, data3]) => {
                console.log(data)
                window.location.replace(`/mycourses/`)
            })
            
        }
    })

})

function postPrice(priceObj) {
    return fetch('/api/courses/prices/', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify(priceObj)
    }).then(response => response.json()).then(data => console.log(data))
}

document.querySelector('#course-third-step-btn').addEventListener('click', event => {
    courseAddSecondStep.classList.add('invisible')
    courseAddThirdStep.classList.remove('invisible')
})


   
// form.addEventListener('submit', (event) => 
// {
//     formData = new FormData(form)
//     courseAddFirstStep.classList.add('invisible')
//     courseAddSecondStep.classList.remove('invisible')
//     event.preventDefault()
// })



