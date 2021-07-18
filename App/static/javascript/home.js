function deleteClass(id){
    var	request	= new XMLHttpRequest();
    request.onreadystatechange = function(){
	if (this.readyState === 4 && this.status === 200){
		document.getElementById("result").innerHTML = this.response;}};
    request.open("POST", "/class/class_delete");
    request.setRequestHeader('Content-type', 'application/json;charset=UTF-8');
    let	data =	{'class_id': Number(id)}
    request.send(JSON.stringify(data));
}

function archiveClass(id){
    var	request	= new XMLHttpRequest();
    request.onreadystatechange = function(){
	if (this.readyState === 4 && this.status === 200){
	    console.log(this.response)
		document.getElementById("result").innerHTML = this.response;}};
    request.open("POST", "/class/class_archive");
    request.setRequestHeader('Content-type', 'application/json;charset=UTF-8');
    let	data =	{'class_id': Number(id)}
    request.send(JSON.stringify(data));
}