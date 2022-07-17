function fetch_user_from_frontend() {
    var user_id = document.getElementById("user_id_frontend").value;
    if (user_id) {
        fetch(`https://reqres.in/api/users/${user_id}`).then(
            response => response.json()
        ).then(
            response => createUsersList(response.data)
        ).catch(
            err => console.log(err)
        )
    }
}

function createUsersList(responseJSON) {

    const frontendUser = document.createElement('div');
    document.getElementById('outerSourceContainer').appendChild(frontendUser);

    const firstName = document.createElement('h2');
    firstName.textContent = "first name: " + responseJSON['first_name'];
    const lastName = document.createElement('h2');
    lastName.textContent = "last name: " + responseJSON['last_name'];
    const user_id = document.createElement('span');
    user_id.textContent = "id: " + responseJSON['id'];
    const user_email = document.createElement('span');
    user_email.textContent = "email: " + responseJSON['email'];
    const image = document.createElement('img');
    image.src = responseJSON['avatar'];

    frontendUser.appendChild(firstName);
    frontendUser.appendChild(lastName);
    frontendUser.appendChild(user_id);
    frontendUser.appendChild(user_email);
    frontendUser.appendChild(document.createElement('br'));
    frontendUser.appendChild(image);
}