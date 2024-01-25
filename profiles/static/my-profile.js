fetch('/api/profiles/has_profile/')
.then(response => response.json())
.then(data => {
    if (!data.profile) {
        showProfileForm()
    } else {
        console.log(data)
        renderProfile(data.content)
        renderCourses(data.courses)
    }
})

function showProfileForm() {
    document.getElementById('profile-create').classList.remove('invisible')
}

function renderProfile(data) {
    document.getElementById('profile-avatar').setAttribute('src', data.avatar)
    document.getElementById('profile-bio').textContent = data.bio
}

function renderCourses(data) {
    data.forEach(course => {
            const clone = document.getElementById('template-course').content.cloneNode(true)
            clone.querySelector('.course-cover').setAttribute('src', course.cover)
            clone.querySelector('.course-title').textContent = course.name
            clone.querySelector('.course-description').textContent = course.short_description
            document.getElementById('my-courses').append(clone)
    });
}


document.querySelector('#profile-create form').addEventListener('submit', event => {
    let formData = new FormData(event.target)
    fetch('/api/profiles/', {
        method: 'post',
        body: formData
    }).then(response => response.json()).then(data => console.log(data))
    event.preventDefault()
})