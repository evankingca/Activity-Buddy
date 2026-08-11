const thing = document.getElementsByClassName("userCardName")
const search = document.getElementById("searchField")
const sc = document.getElementById("searchContainerThing")
const nm = document.createElement("span")
nm.classList.add("text-center", "text-text/50", "italic")
nm.id = "nm"
nm.textContent = "No users found"

const names = []

for (t of thing) {
  names.push({ text: t.textContent, pid: t.parentElement.parentElement.id })
}

function doTheThing(v) {
  const enm = document.getElementById("nm")
  enm !== null && enm.remove()
  names.forEach(j => document.getElementById(j.pid).classList.remove("hidden"))
  const i = names.filter(h => !h.text.toLowerCase().includes(v.toLowerCase()))
  i.forEach(j => document.getElementById(j.pid).classList.add("hidden"))
  if (i.length === names.length) {
    sc.appendChild(nm)
  }
}

search.addEventListener('input', (e) => {
  doTheThing(search.value)
})

