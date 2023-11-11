const id = document.querySelector('#author-id').textContent

fetch(`http://127.0.0.1:8000/api/profiles/${id}/`)
.then(response => response.json())
.then(data => initializeBio(data))


function initializeBio(data) {
    console.log(data)
    document.querySelector('#teacher-avatar').setAttribute('src', data.avatar)
    document.querySelector('#teacher-bio').textContent = data.bio
    document.querySelector('#teacher-name').textContent = data.name
    document.querySelector('#teacher-rating').textContent = data.rating
    document.querySelectorAll(`svg.review-star-small:nth-child(-n+${Math.round(data.rating)})`).forEach(star => star.classList.add('star-selected'))
    document.querySelector('#teacher-students').textContent = data.students
}