function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie != '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue
}

const qItems = document.getElementsByClassName('question-like-section');
const aItems = document.getElementsByClassName('answer-like-section');


for (let item of qItems) {
    const likeButton = item.getElementsByClassName('rate-button')[0]
    const dislikeButton = item.getElementsByClassName('rate-button')[1]
    const likesCounter = item.getElementsByClassName('rating-value')[0]

    likeButton.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('content', 'q');
        formData.append('id', likesCounter.dataset.id)

        const request = new Request('/like', {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                likesCounter.innerText = data.amount;
            })
    })

    dislikeButton.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('content', 'q');
        formData.append('id', likesCounter.dataset.id);

        const request = new Request('/dislike', {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                likesCounter.innerText = data.amount;
            })
    })
}

for (let item of aItems) {
    const likeButton = item.getElementsByClassName('rate-button')[0]
    const dislikeButton = item.getElementsByClassName('rate-button')[1]
    const likesCounter = item.getElementsByClassName('rating-value')[0]
    const correctButton = item.getElementsByClassName('styled-checkbox')[0]

    likeButton.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('content', 'a');
        formData.append('id', likesCounter.dataset.id);

        const request = new Request('/like', {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                likesCounter.innerText = data.amount;
            })
    })

    dislikeButton.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('content', 'a');
        formData.append('id', likesCounter.dataset.id);

        const request = new Request('/dislike', {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                likesCounter.innerText = data.amount;
            })
    })

    correctButton.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('answer_id', likesCounter.dataset.id);
        formData.append('question_id', likesCounter.dataset.questionid);

        const request = new Request('/status', {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                correctButton.checked = data.status;
            })
    })
}

