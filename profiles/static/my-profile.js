fetch('http://127.0.0.1:8000/api/profiles/has_profile/')
.then(response => response.json())
.then(data => {
    if (!data.profile) {
        showProfileForm()
    } else {
        console.log(data)
    }
})

function showProfileForm() {
    document.getElementById('profile-create').classList.remove('invisible')
}


document.querySelector('#profile-create form').addEventListener('submit', event => {
    let formData = new FormData(event.target)
    fetch('http://127.0.0.1:8000/api/profiles/', {
        method: 'post',
        body: formData
    }).then(response => response.json()).then(data => console.log(data))
    event.preventDefault()
})