const id = document.querySelector('#author-id').textContent

fetch(`http://127.0.0.1:8000/api/profiles/${id}/`)
.then(response => response.json())
.then(data => initializeBio(data))


function initializeBio(data) {
    console.log(data)
    document.querySelector('#teacher-avatar').setAttribute('src', data.avatar)
    document.querySelector('#teacher-bio').textContent = data.bio
}