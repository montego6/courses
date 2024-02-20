const form = document.forms.namedItem('course-add')
let categoriesData
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

function initializeInputs(courseData) {
    document.querySelector('input[name=name]').value = courseData.name
    document.querySelector('input[name=short_description]').value = courseData.short_description
    document.querySelector('textarea[name=full_description]').value = courseData.full_description

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

    if (courseData.is_free) {
        document.querySelector('input[name=is_free]').setAttribute('checked', 'true')
    }

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

    fetch('/api/categories/').then(response => response.json()).
    then(data => {
    console.log('CATEGORIES', data)
    categoriesData = data
    initializeCategories(categoriesData, courseData)
})
}

function initializeCategories(data, courseData) {
    console.log('DATA', data)
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

document.querySelector('#is_free-checkbox').addEventListener('change', event => {
    if (event.target.checked) {
        document.querySelector('input[name=price]').value = 0
        document.querySelector('input[name=price]').disabled = true
    } else {
        document.querySelector('input[name=price]').disabled = false
    }
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



