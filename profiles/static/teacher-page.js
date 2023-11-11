const id = document.querySelector('#author-id').textContent

fetch(`http://127.0.0.1:8000/api/profiles/${id}/`)
.then(response => response.json())
.then(data => {
    initializeBio(data)
    initializeCourses(data.courses)
})


function initializeBio(data) {
    console.log(data)
    document.querySelector('#teacher-avatar').setAttribute('src', data.avatar)
    document.querySelector('#teacher-bio').textContent = data.bio
    document.querySelector('#teacher-name').textContent = data.name
    document.querySelector('#teacher-rating').textContent = data.rating
    document.querySelectorAll(`svg.review-star-small:nth-child(-n+${Math.round(data.rating)})`).forEach(star => star.classList.add('star-selected'))
    document.querySelector('#teacher-students').textContent = data.students
}

function initializeCourses(data) {
    console.log(data)
    data.forEach(course => {
        const clone = document.querySelector('#template-course').content.cloneNode(true)
        clone.querySelector('.course-cover img').setAttribute('src', course.cover)
        clone.querySelector('.course-name').textContent = course.name
        clone.querySelector('.course-description').textContent = course.short_description
        clone.querySelector('.course-price').textContent = course.price + ' руб.'
        clone.querySelector('.course-student-count').textContent = course.students
        clone.querySelectorAll(`svg.review-star-small:nth-child(-n+${Math.round(course.rating)})`).forEach(star => star.classList.add('star-selected'))
        clone.querySelector('.course-rating-number').textContent = course.rating
        clone.querySelector('.course-subject span').textContent = course.subject
        clone.querySelector('a').setAttribute('href', `http://127.0.0.1:8000/course/${id}`)
        document.querySelector('#courses').append(clone)
    })
}