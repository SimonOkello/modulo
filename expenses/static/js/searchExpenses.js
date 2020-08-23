const searchField = document.querySelector("#searchField");


searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {

    console.log("searchValue", searchValue);
    fetch("/search_expense", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        
      });
   
  } 
});