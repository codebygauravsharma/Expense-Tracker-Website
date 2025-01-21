const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tbody = document.querySelector(".table-body");
const url = new URL(window.location.href)
const showAllContant = document.querySelector(".show-all-contant")

if (url.searchParams.get("page") == 'all'){
    showAllContant.style.display = "none"; // Hide the element
}

tableOutput.style.display="none";

searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        paginationContainer.style.display = 'none';

        tbody.innerHTML = "";
        fetch("/userincome/search-income",{
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            body: JSON.stringify({searchText: searchValue})
            
    })
    .then((res) => res.json())
    .then((data) => {
        console.log("data", data);
        appTable.style.display="none";
        tableOutput.style.display="block";

        console.log("data.length", data.length);

        if(data.length === 0){
            tableOutput.innerHTML = "No Results Found";
        }else{
            data.forEach((item) => {
            tbody.innerHTML += `
            <tr>
            <td>${item.amount}</td>
            <td>${item.source}</td>
            <td>${item.description}</td>
            <td>${item.date}</td>
            </tr>`;

            });
        }
    });
    } else{
        tableOutput.style.display = "none";
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
    }
});
