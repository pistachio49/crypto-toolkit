let ob1=document.getElementById("Plaintext");
let ob2=document.getElementById("Ciphertext");
let val1=ob1.value;
let rg1=/^[A-Za-z]+$/;

let k1=document.getElementById("key");
let k2=document.getElementById("key2");

function validate()
{
console.log('hello i am here')
if(ob1!==null && val1!="" && rg1.test(val1)==false)
{   
    e.preventDefault();
    ob1.value="";
    k1.value="";
    k2.value="";
    alert(`The ${ob1.id} can only have alphabets`);
    return false;
}
if(ob2!==null && ob2.value!="" && rg1.test(ob2.value)==false)
{   
    e.preventDefault();
    ob2.value="";
    k1.value="";
    k2.value="";
    alert(`The ${ob2.id} can only have alphabets`);
    return false;
}
return true;
}

