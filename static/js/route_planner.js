const userInput = document.getElementById("userInput");
const srcInput = document.getElementById("srcInput");
const dstInput = document.getElementById("dstInput");
const calBtn = document.getElementById("calBtn");
const ul = document.getElementById("autocomplete")

srcInput.addEventListener('input', ()=>{autocomplete(srcInput)});
dstInput.addEventListener('input', ()=>{autocomplete(dstInput)});

function autocomplete(Input){
    ul.innerHTML=""; //on each input clear ul
    var input = Input.value;
    if(input.length<3) //if input<3 no suggestions
    {
        ul.style.display ='none';
        calBtn.style.display="inline";
    }
    else
    {
        fetch(`https://www.onemap.gov.sg/api/common/elastic/search?searchVal=${input}&returnGeom=Y&getAddrDetails=Y`).then(res =>{
            return res.json();
        }).then(data =>{
            if(data.results.length==0) 
                {
                    return;
                }
            for(var loop=0;loop<5;loop++) //auto-complete 5 addresses
            {
                calBtn.style.display="none";
                var li = document.createElement('li');
                li.classList.add("li-autocomplete");
                li.textContent=data.results[loop].ADDRESS;
                ul.appendChild(li);

                li.addEventListener('click', ()=>{ //add address to input box

                    Input.value = li.textContent;
                    ul.innerHTML ="";
                    ul.style.display ='none';
                    calBtn.style.display="inline";
                    return;

                })

                if(data.results[loop+1]==undefined)
                {
                    break;
                }
            }
            ul.style.display="inline";
            return;
        })

    }
}

function calRoute()
{
    console.log("Do route calculation");
}
