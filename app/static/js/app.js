const images = document.querySelectorAll('.show-image')
const body = document.querySelector('body')
const grid = document.querySelector('.grid')
const search  = document.querySelector('.search')
const suggestion  = document.querySelector('.suggestion')

images.forEach((item, i) => {
  item.addEventListener('click', (item)=>{
    var image_viewer = document.createElement('div')
    image_viewer.classList.add('image_viewer')

    var img = document.createElement('img')
    img.src = item.target.currentSrc

    image_viewer.appendChild(img)
    body.appendChild(image_viewer)

    image_viewer.addEventListener('click', ()=>{
      body.removeChild(image_viewer)
    })
  })
});

seen = {}

search.addEventListener('input', (e) => {
  if(e.target.value.length == 0){
    suggestion.innerHTML = '';
    console.log('remoing')
  }
  keyword = e.target.value
  if (keyword){
    suggestion.innerHTML = '';
    // check if keyword already searched
    if(keyword in seen ){
      keywordList = seen[keyword]
      keywordList.forEach((kw) => {
        create_suggestion(kw)
      })
    }else{
      suggestion.innerHTML = '';
      get_keywords(keyword)
    }
  console.log(seen)
  }
})

function get_keywords(keyword){
  fetch('/keyword', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({keyword: keyword})
  })
  .then(res => res.json())
  .then((data) => {
    keywords = data.data.keywords
    keywords.forEach((elm) => {
      // check keyword already search
      if (!(elm in seen)){
        // if keyword is not seen then
        seen[keyword] = keywords
        create_suggestion(elm)
      }
    })
  })
}

function create_suggestion(keyword){
  li = document.createElement('li')
  li.classList.add('flex', 'column', 'margin')
        
  a = document.createElement('a')
  a.textContent = keyword
  a.classList.add('f-black', 'link')
  a.href = `/search/${keyword}`
        
  li.appendChild(a)
  suggestion.appendChild(li)
}