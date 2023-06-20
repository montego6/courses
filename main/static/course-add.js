const form = document.forms.namedItem('course-add')
form.addEventListener('submit', (event) => 
{
    const formData = new FormData(form)
    fetch('http://localhost:8000/api/subjects/', {
        method: 'post',
        body: formData
    }).then(response => response.json()).then(data => console.log(data))
    event.preventDefault()
})