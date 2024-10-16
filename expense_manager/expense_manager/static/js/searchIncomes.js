
const searchQueryField = document.querySelector("#searchQuery")
const appTable = document.querySelector("#app-table")
const tableOutput = document.querySelector("#table-output")
const paginatorContainer = document.querySelector("#paginator-container")
const tbody = document.querySelector(".tbody")
const no_result = document.querySelector("#no-result")

appTable.style.display = 'block';
console.log(appTable);


tableOutput.style.display = "none";
no_result.style.display = 'none';
// tableOutput.innerHTML = "";

searchQueryField.addEventListener("keyup", (e) => {
    const searchQuery = e.target.value;

    if (searchQuery.trim().length > 0) {
        tbody.innerHTML = "";
        paginatorContainer.style.display = "none";
        fetch('search-incomes/', {
            body: JSON.stringify({ searchField: searchQuery }),
            method: "POST"
        })
            .then((res) => res.json())
            .then((data) => {
                appTable.style.display = 'none';
                tableOutput.style.display = 'block';
                no_result.style.display = 'none';
                console.log(data);
                console.log(data.length);

                if (data.length === 0) {
                    tableOutput.style.display = 'none';
                    no_result.style.display = 'block';
                } else {
                    tableOutput.style.display = 'block';
                    no_result.style.display = 'none';
                    console.log(data);

                    data.forEach(inc => {
                        tbody.innerHTML += `
                        <tr>
                            <td>${inc.amount}</td>
                            <td>${inc.category}</td>
                            <td>${inc.description}</td>
                            <td>${inc.date}</td>
                        </tr>
                        `
                    });
                }
            })
    } else {
        tableOutput.style.display = 'none';
        appTable.style.display = 'block';
        paginatorContainer.style.display = 'block';
    }
})
