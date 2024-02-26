fetch('/api/courses/my_courses/').then(response => response.json()).then(data => initializeCourses(data))


function initializeCourses(data) {
    data.forEach(course => {
        const clone = document.getElementById('template-course').content.cloneNode(true)
        clone.querySelector('.course-cover').setAttribute('src', course.cover)
        clone.querySelector('.course-title').textContent = course.name
        clone.querySelector('.course-link').setAttribute('href', course.url)
        clone.querySelector('.course-description').textContent = course.short_description
        clone.querySelector('.course-students').textContent = course.students
        clone.querySelector('.course-rating').textContent = course.rating
        document.querySelector('#my-courses').append(clone)
    });
}

