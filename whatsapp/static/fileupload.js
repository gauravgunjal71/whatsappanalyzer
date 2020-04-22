function handlefileselect(event) {

    var files = event.target.files;

    if (files!=null){
        document.getElementById('submit').disabled = false;
        document.getElementById('inputlable').innerHTML = files[0].name
    }

}

document.getElementById('file').addEventListener("change", handlefileselect, false)
