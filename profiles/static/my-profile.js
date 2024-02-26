const csrf_token = document.querySelector('#csrf-token input').value 

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
    // document.getElementById('profile-bio').textContent = data.bio
    document.getElementById('author-name').textContent = data.name
    document.getElementById('courses-rating').textContent = data.rating
    document.getElementById('courses-students').textContent = data.students
    document.getElementById('balance').textContent = data.balance
}

function renderCourses(data) {
    data.forEach(course => {
            const clone = document.getElementById('template-course').content.cloneNode(true)
            clone.querySelector('.course-cover').setAttribute('src', course.cover)
            clone.querySelector('.course-title').textContent = course.name
            clone.querySelector('.course-description').textContent = course.short_description
            clone.querySelector('.course-students').textContent = course.students
            clone.querySelector('.course-rating').textContent = course.rating
            clone.querySelector('.btn-content').addEventListener('click', event => {
                window.location.href = `/mycourses/${course.slug}/`
            })
            clone.querySelector('.btn-edit').addEventListener('click', event => {
                window.location.href = `/mycourses/${course.slug}/edit/`
            })
            if (course.is_published) {
                clone.querySelector('.btn-unpublish').classList.remove('invisible')
            } else {
                clone.querySelector('.btn-publish').classList.remove('invisible')
            }

            clone.querySelector('.btn-unpublish').addEventListener('click', event => {
                obj = {
                    is_published: false
                }
                fetch(`/api/courses/${course.slug}/`,
                {
                    method: 'PATCH',
                    body: JSON.stringify(obj),
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrf_token,
                    },
                }).then(response => {
                    if (response.status == 200) {
                        event.target.closest('div').querySelector('.btn-unpublish').classList.toggle('invisible')
                        event.target.closest('div').querySelector('.btn-publish').classList.toggle('invisible')
                    }
                })
                
            })

            clone.querySelector('.btn-publish').addEventListener('click', event => {
                fetch(`/api/courses/${course.slug}/publish/`).then(response => {
                    if (response.status == 200) {
                        event.target.closest('div').querySelector('.btn-unpublish').classList.toggle('invisible')
                        event.target.closest('div').querySelector('.btn-publish').classList.toggle('invisible')
                    }
                })
            })
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