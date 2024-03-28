let updateSet = new Set();

function createTable(data, userJson) {
    let divMain = document.getElementById("tableMain");

    // WEEK
    for (let ref in data.week) {

        let divWeek = document.createElement("div");
        divWeek.id = ref;

        // DAY within week
        for (let day in data.week[ref]) {

            let tableDay = document.createElement("table");
            tableDay.id = `${ref}_${day}`;

            // TRAVERSE DOWNWARD; ESTABLISH EACH ROW.
            for (let y = 0; y < data.titleSide.length + 1; y++) {

                let currRow = document.createElement("tr");
                currRow.id = `${ref}_${day}_${ y === 0? 'Head': y-1 }`;

                // TRAVERSE LEFT TO RIGHT; ESTABLISH EACH CELL, WITHIN A ROW
                for (let x = 0; x < data.titleTop.length + 1; x++) {

                    // TO-BE CELL ELEMENT
                    let cell = null;

                    // ROW HEADING
                    if (y === 0) {
                        cell = document.createElement("th");
                        cell.textContent = x === 0? `${day}, Week ${ref}`: data.titleTop[x-1];
                    }
                    // NON-ROW HEADING
                    else {
                        cell = document.createElement(x === 0? "th": "td");
                        cell.textContent = x === 0? data.titleSide[y-1]: data.week[ref][day][y-1][x-1];
                        if (x > 0 && userJson.admin) tableCellEventListener(cell);
                        cell.id = `${ref}_${day}_${y-1}_${x-1}`;
                    }

                    currRow.appendChild(cell);

                }

                tableDay.appendChild(currRow);
            }

            divWeek.appendChild(tableDay);

        }

        divMain.appendChild(divWeek);

    }
}


function tableCellEventListener(cell) {


    cell.addEventListener('mouseover', function() {
        cell.classList.add('hover');
    });

    cell.addEventListener('click', function() {
        if (cell.classList.contains('mouseDown')) {
            cell.classList.remove('mouseDown');
            updateSet.delete(cell.id);
        }
        else {
            cell.classList.add('mouseDown');
            updateSet.add(cell.id);
        }
    });

    cell.addEventListener('mouseout', function() {
        cell.classList.remove('hover');
    });

}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setUserTitle(userJson) {
    let titleElement = document.getElementById("userDuties");
    titleElement.textContent = `${userJson.name}'s Duties`;
}

document.addEventListener('DOMContentLoaded', function() {

    let updateBtn = document.getElementById('updateBtn');

    // fetch for userJson data;
    fetch('/get_username/')
    .then(response => response.json())
    .then(userJson => {

        // fetch for data.json
        fetch('/load_json/')
        .then(response => response.json())
        .then(dataJson => {
            setUserTitle(userJson);
            createTable(dataJson, userJson);
        })
        .catch(error => {
            console.error('Error fetching JSON:', error);
        });

    })
    .catch(error => {
        console.error('Error fetching username:', error);
    });

    if (updateBtn) {
        updateBtn.addEventListener('click', function() {
            fetch('/update_duty/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({}),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    console.log('Duty updated successfully');
                }
            })
            .catch(error => {
            console.error('Error Logging Staff Time', error);
            });
        });

    }

});
