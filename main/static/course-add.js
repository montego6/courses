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

// function getCookie(name) {
//     const value = `; ${document.cookie}`;
//     const parts = value.split(`; ${name}=`);
//     if (parts.length === 2) return parts.pop().split(';').shift();
//   }

confirmBtn.addEventListener('click', (event) => {
    learnOptions = document.querySelectorAll('.what-will-learn-option')
    const learnList = Array.from(learnOptions, option => option.value)
    requirementsOptions = document.querySelectorAll('.requirements-option')
    const requirementsList = Array.from(requirementsOptions, option => option.value)
    const options = {option: "value"}
    formData.append('what_will_learn', learnList)
    formData.append('requirements', requirementsList)
    formData.append('options', JSON.stringify(options))
    fetch('http://127.0.0.1:8000/api/courses/', {
        // headers: {
        //     "Authorization": "Session " + getCookie('sessionid'),
        // },
        method: 'post',
        body: formData
    }).then(response => response.json()).then(data => console.log(data))

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
    fetch('http://127.0.0.1:8000/api/user/', {
        credentials: "include"
      }).then(response => response.json()).then(data => console.log(data))
    event.preventDefault()
})