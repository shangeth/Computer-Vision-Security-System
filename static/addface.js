document.querySelector('#addface').onsubmit = () =>{
    const request = new XMLHttpRequest();
    request.open('POST','/takepic');
    request.onload()=>{
        const data = JSON.parse(request.responseText);

        if(data.success){
            const content = data.msg
            document.querySelector('#here').innerHTML = content;
        }
    }

}