const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector('.invalid_feedback')

usernameField.addEventListener('keyup', (e)=>{

    const usernameVal = e.target.value;

    feedBackArea.style.display = 'none'
    usernameField.classList.remove('is-invalid');

    if (usernameVal.length>0){
    fetch('/auth/validate_username', {
        body: JSON.stringify({username:usernameVal}),
        method:'POST',
    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log('data',data);

        if(data.username_error){
            feedBackArea.style.display = 'block'
            usernameField.classList.add('is-invalid');
            feedBackArea.innerHTML=`<p>${data.username_error}</p>`
        }
    });
}

});