const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const defaultTable = document.querySelector(".default-table");
const paginationContainer = document.querySelector(".pagination-container");
const tBody = document.querySelector(".table-body");
const noResults = document.querySelector(".no-results");

tableOutput.style.display = "none";

searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    tBody.innerHTML = "";

    fetch("/income/search_income", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        defaultTable.style.display = "none";
        tableOutput.style.display = "block";

        if (data.length === 0) {
          noResults.style.display = "block";
          tableOutput.style.display = "none";
        } else {
          noResults.style.display = "none";
          data.forEach((item) => {
            tBody.innerHTML += `

          <tr>
          
          <td>${item.source}</td>
          <td>${item.description}</td>
          <td>${item.amount}</td>
          <td>${item.date}</td>
          
          </tr>`;
          });
        }
      });
  } else {
    tableOutput.style.display = "none";
    defaultTable.style.display = "block";
    paginationContainer.style.display = "block";
  }
});
