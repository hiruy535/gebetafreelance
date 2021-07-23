console.log('stars')

//console.log(rateState)
/*

const star = document.getElementsByName('starRate')
const forms = document.getElementsByName('starForm')
const pricelink = document.getElementsByName('pricelink')
for (var i=0; i <pricelink.length;i++){
  const pricelinks = Array.from(pricelink[i].children)
  pricelinks.forEach(item=> item.addEventListener('click',(event)=>{
        console.log(event.target)
  }))
}
for (var i=0; i <star.length;i++){
    const stars = Array.from(star[i].children)

    const starHandiler = (size) =>{
      for(let i=0; i < stars.length;i++){
          if(i <= (size-1)){
            stars[i].classList.add("checked")
          }
          else{
            stars[i].classList.remove("checked")
          }

      }
    }
      stars.forEach(item=> item.addEventListener('mouseover',(event)=>{
        starHandiler(event.target.id)
        //console.log(event.target)
        const elem = event.target.parentElement
        elem.value = event.target.id
        console.log(elem.value)
        //console.log(event.target.id)
    }))

    stars.forEach(item=> item.addEventListener('click',(event)=>{
        const elem = event.target.parentElement
        const form = elem.parentElement
        var star_id = event.target.id
        event.preventDefault();
        console.log("form submitted!")


        $.ajax({
          type: 'POST',
          url: '{% url "main:addroom" %}' ,
          data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            'starRate' : star_id
          },
          success: function(response){
            console.log(response.starRate)
          }

        });

        console.log(event.target)
  }))

}
*/
