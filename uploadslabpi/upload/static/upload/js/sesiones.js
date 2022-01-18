var data = localStorage.getItem('data');
//localStorage.clear();
var data1 = JSON.parse(data).user;
var data2 = JSON.parse(data).pass;

console.log(data1, data2);
   
var etiqueta = document.getElementById("user1")
etiqueta.innerHTML = data1;


